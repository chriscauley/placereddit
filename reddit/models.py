from django.conf import settings
from django.db import models
from django.http import HttpResponse

from sorl.thumbnail import ImageField
from PIL import Image as _Image

import requests, re, os, StringIO, pycrop

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
  date_added = models.DateTimeField(auto_now_add=True)
  fname = property(lambda self: self.url.split('/')[-1])
  fpath = property(lambda self: os.path.join(settings.PPATH,'tmp',self.fname))
  def delete(self,*args,**kwargs):
    try:
      os.remove(self.fpath)
    except OSError:
      pass
    return super(Image,self).delete(*args,**kwargs)
  def save(self,*args,**kwargs):
    if not self.width or not self.height:
      self.width, self.height = self.get_PIL_object().size
    super(Image,self).save(*args,**kwargs)
  def get_PIL_object(self):
    try:
      f = open(self.fpath,'rb')
    except IOError:
      f = open(self.fpath,'w')
      r = requests.get(self.url,stream=True)
      f.write(r.raw.read())
      f.close()
      return self.get_PIL_object()
    return _Image.open(f)
  def crop_response(self,width,height):
    i = self.get_PIL_object()
    area = pycrop.prepare_image(i,(width,height))
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
