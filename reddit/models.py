from django.conf import settings
from django.db import models
from django.http import HttpResponse

from sorl.thumbnail import ImageField
from PIL import Image as _Image

from smartcrop import cache_entropies, crop_image, scale_image
import requests, re, os, StringIO,datetime

class SubRedditManager(models.Manager):
  def get_featured(self,*args,**kwargs):
    reddits = self.filter(*args,**kwargs).filter(featured=True)
    try:
      return reddits.filter(last_featured=datetime.date.today())[0]
    except IndexError:
      reddit = reddits.order_by('last_featured')[0]
      reddit.last_featured = datetime.date.today()
      reddit.save()
      return reddit

class SubReddit(models.Model):
  name = models.CharField(max_length=255,unique=True)
  slug = models.CharField(max_length=255,unique=True)
  nsfw = models.BooleanField(default=False)
  get_absolute_url = lambda self: "/r/%s%s/"%(self.slug,"/nsfw" if self.nsfw else "")
  featured = models.BooleanField(default=False)
  last_featured = models.DateField(default=datetime.date.today)
  objects = SubRedditManager()
  def save(self,*args,**kwargs):
    super(SubReddit,self).save(*args,**kwargs)
    self.pull_from_imgur()
  def pull_from_imgur(self):
    url = "http://imgur.com/r/%s"%self.slug
    html = requests.get(url).text
    imgs = re.findall(r'href="/r/[^/]+/([^"]+)"',html)
    new_images = []
    for i,s in enumerate(imgs):
      url = "http://i.imgur.com/%s.jpg"%s
      if s in ["new","top"]:
        continue
      try:
        o,new = Image.objects.get_or_create(url=url,subreddit=self)
        if new:
          new_images.append(unicode(o))
      except IOError,e: #! TODO apparently some images are too large?!
        print "failed to write %s"%e
    if self.image_set.filter(active=True).count() > 60:
      for i in self.image_set.all()[60:]:
        i.mark_inactive()
    return new_images
  __unicode__ = lambda self: self.name
  class Meta:
    ordering = ('name',)

class Image(models.Model):
  subreddit = models.ForeignKey(SubReddit)
  url = models.URLField()
  width = models.IntegerField(default=0)
  height = models.IntegerField(default=0)
  #y_crop_order = models.CharField(max_length=1024,null=True,blank=True)
  #x_crop_order = models.CharField(max_length=1024,null=True,blank=True)
  date_added = models.DateTimeField(auto_now_add=True)
  active = models.BooleanField(default=True)
  fname = property(lambda self: self.url.split('/')[-1])

  fpath = property(lambda self: os.path.join(settings.PPATH,'tmp',self.fname))
  def delete_images(self):
    for path in [self.fpath]+["%s_%sx%s"%(self.fpath,w,h) for w,h in self.sizes_available]:
      try:
        os.remove(path)
      except OSError:
        if self.pk: # unsaved objects shouldn't have anything do delete
          print "failed at deleting: %s"%path
  def delete(self,*args,**kwargs):
    self.delete_images()
    super(Image,self).delete(*args,**kwargs)
  def mark_inactive(self):
    if self.active:
      self.delete_images()
      self.active = False
      self.save()
  def save(self,*args,**kwargs):
    if self.active and not self.width: # or not self.x_crop_order:
      self.pull_from_imgur()
      I = self.get_PIL_object()
      self.width, self.height = I.size
      if self.width < 300 or self.height < 300:
        if self.pk:
          self.delete()
        else:
          self.delete_images()
        return
      #self.x_crop_order,self.y_crop_order = cache_entropies(I)
      self.cache_all_sizes()
    super(Image,self).save(*args,**kwargs)

  @property
  def sizes_available(self):
    w = self.width
    h = self.height
    out = []
    while w > 50 and h > 50:
      out.append((w,h))
      w = int(w*0.8)
      h = int(h*0.8)
    return out[::-1]
  def cache_all_sizes(self):
    image = self.get_PIL_object()
    for size in self.sizes_available[::-1]:
      area = scale_image(image,size)
      area.save("%s_%sx%s"%(self.fpath,size[0],size[1]),format='jpeg')

  def pull_from_imgur(self):
    f = open(self.fpath,'w')
    r = requests.get(self.url,stream=True)
    f.write(r.raw.read())
    f.close()

  def get_PIL_object(self,width=None,height=None):
    path = self.fpath
    if width and height:
      for size in self.sizes_available:
        if size[0]>width and size[1]>height:
          path = "%s_%sx%s"%(self.fpath,size[0],size[1])
          break
    f = open(path,'rb')
    return _Image.open(f)

  def crop_response(self,width,height):
    image = self.get_PIL_object(width=width,height=height)
    #multiplier = 10
    #for i,size in enumerate(self.sizes_available):
    #  if size[0]>width and size[1]>height:
    #    multiplier = i+1
    #    break
    area = crop_image(image,(width,height)) #,self.x_crop_order,self.y_crop_order,multiplier)
    response = HttpResponse(content_type="image/jpeg")
    area.save(response, format='jpeg')
    return response
    
  class Meta:
    ordering = ("-date_added",)
  __unicode__ = lambda self: "%s (%s)"%(self.url,self.subreddit)

class Subject(models.Model):
  name = models.CharField(max_length=255)
  nsfw = models.BooleanField(default=False)
  subreddits = models.ManyToManyField(SubReddit,blank=True)
  __unicode__ = lambda self: self.name
  @classmethod
  def fast_add(clss,name,slugs,nsfw=False):
    """lazy way to add a bunch of subreddits from the command line"""
    subject,new = clss.objects.get_or_create(name=name,nsfw=nsfw)
    if new:
      print "New Subject: %s"%subject
    for slug in slugs:
      reddit,new = SubReddit.objects.get_or_create(name=slug,slug=slug,nsfw=nsfw)
      if new:
        print "New SubReddit: %s"%reddit
      subject.subreddits.add(reddit)
    subject.save()

def test():
  s,new = SubReddit.objects.get_or_create(name='aww',slug='aww')
  if new:
    print "Subreddit created! %s"%s
  s.pull_from_imgur()
  i = Image.objects.all()[0]
  i.crop(100,100)
