from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

from .models import SubReddit, Image

import random,datetime

#@cache_page(60 * 15)
def index(request,subreddit=None,nsfw=False):
  sizes = (
    (100,100),
    (200,200),
    (100,100),
    (200,200),
    (100,100),
    (200,200),
    )
  sizes = sizes*100
  values = {
    'randint': lambda: random.choice(range(31)),
    'sizes': sizes,
    }
  return TemplateResponse(request,"reddit.html",values)

@cache_page(60 * 15)
def image(request,subreddit=None,nsfw=False,width=None,height=None,extension=None,num=None):
  nsfw = nsfw or False
  if subreddit == 'featured':
    subreddits = SubReddit.objects.filter(featured=True)
    r = random.randint(0,subreddits.count()-1)
    subreddit = subreddits[r]
  if not subreddit or subreddit == 'random':
    r = random.randint(0,SubReddit.objects.filter(nsfw=nsfw).count()-1)
    subreddit = SubReddit.objects.filter(nsfw=nsfw)[r]
  else:
    subreddit = SubReddit.objects.get(name=subreddit)
  if subreddit.nsfw != nsfw:
    pass # return over_18 image with text
  images = Image.objects.filter(subreddit=subreddit)
  images = images.filter(height__gte=height,width__gte=width)
  image = random.choice(images)
  return image.crop_response(int(width),int(height))

def random_image():
  subreddit = random.choice(SubReddit.objects.all())
  images = Image.objects.filter(subreddit=subreddit)
  height =random.choice(range(100,1000))
  width = random.choice(range(100,1000))
  images = images.filter(height__gte=height,width__gte=width)
  if not images:
    print "no image found: %s %sx%s"%(subreddit,width,height)
    return
  image = random.choice(images)
  return image.crop_response(int(width),int(height))

def test(n=50,f=random_image):
  now = datetime.datetime.now()
  while n>0:
    f()
    n-=1
  print (datetime.datetime.now()-now).seconds
