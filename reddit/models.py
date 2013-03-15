from django.conf import settings
from django.db import models
from django.http import HttpResponse

from sorl.thumbnail import ImageField
from PIL import Image as _Image

from smartcrop import cache_entropies, prepare_image
import requests, re, os, StringIO

class SubReddit(models.Model):
  name = models.CharField(max_length=255,unique=True)
  slug = models.CharField(max_length=255,unique=True)
  nsfw = models.BooleanField(default=False)
  get_absolute_url = lambda self: "/r/%s%s/"%(self.slug,"/nsfw" if self.nsfw else "")
  featured = models.BooleanField(default=False)
  def pull_from_imgur(self):
    url = "http://imgur.com/r/%s/rss"%self.slug
    html = requests.get(url).text
    imgs = re.findall(r'img src=&quot;(http://i.imgur.com/[\w\d]+\.jpg)&quot;',html)
    if self.image_set.count() > 60:
      for i in self.image_set.all()[60:]:
        i.delete()
    for i,url in enumerate(imgs):
      o,new = Image.objects.get_or_create(url=url,subreddit=self)
      if new:
        print "Image created! %s"%o
  __unicode__ = lambda self: self.name

class Image(models.Model):
  subreddit = models.ForeignKey(SubReddit)
  url = models.URLField(verify_exists=False)
  width = models.IntegerField(default=0)
  height = models.IntegerField(default=0)
  y_crop_order = models.CharField(max_length=256,null=True,blank=True)
  x_crop_order = models.CharField(max_length=256,null=True,blank=True)
  date_added = models.DateTimeField(auto_now_add=True)
  active = models.BooleanField(default=True)
  fname = property(lambda self: self.url.split('/')[-1])
  fpath = property(lambda self: os.path.join(settings.PPATH,'tmp',self.fname))

  def save(self,*args,**kwargs):
    if not self.active:
      for path in [self.fpath]+["%s_%s"%(self.fpath,i) for i in range(1,6)]:
        try:
          os.remove(path)
        except OSError:
          pass
    if active and not self.width or not self.x_crop_order:
      self.pull_from_imgur()
      I = self.get_PIL_object()
      self.width, self.height = I.size
      self.x_crop_order,self.y_crop_order = cache_entropies(I)
    super(Image,self).save(*args,**kwargs)

  @property
  def sizes_available(self):
    w_inc = self.width/5
    h_inc = self.height/5
    return [(w_inc*i,h_inc*i) for i in range(1,6)]

  def cache_all_sizes(self):
    image = self.get_PIL_object()
    for size in enumerate(self.sizes_available):
      area = scale_image(image,size)
      area.save("%s_%sx%s"%(self.fpath,width,height),format='jpeg')

  def pull_from_imgur(self):
    f = open(self.fpath,'w')
    r = requests.get(self.url,stream=True)
    f.write(r.raw.read())
    f.close()

  def get_PIL_object(self,width=None,height=None):
    path = self.fpath
    if width and height:
      for size in enumerate(self.sizes_available):
        if size[0]>width and size[1]>height:
          path = "%s_%sx%s"%(self.fpath,size[0],size[1])

    f = open(fpath,'rb')
    return _Image.open(f)

  def crop_response(self,width,height):
    i = get_PIL_object()
    area = crop_image(i,(width,height),self.x_crop_order,self.y_crop_order)
    response = HttpResponse(mimetype="image/jpeg")
    area.save(response, format='jpeg')
    return response
    
  class Meta:
    ordering = ("-date_added",)
  __unicode__ = lambda self: "%s (%s)"%(self.url,self.subreddit)

def test():
  s,new = SubReddit.objects.get_or_create(name='aww',slug='aww')
  if new:
    print "Subreddit created! %s"%s
  s.pull_from_imgur()
  i = Image.objects.all()[0]
  i.crop(100,100)
