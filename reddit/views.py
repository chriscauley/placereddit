from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

from .models import SubReddit, Image

import random,datetime

def get_subreddit(slug=None,nsfw=None):
  if slug == 'featured':
    subreddits = SubReddit.objects.filter(featured=True)
    r = random.choice(range(0,subreddits.count()))
    subreddit = subreddits[r]
  elif not slug or slug == 'random':
    r = random.randint(0,SubReddit.objects.filter(nsfw=nsfw).count()-1)
    subreddit = SubReddit.objects.filter(nsfw=nsfw)[r]
  else:
    subreddit = SubReddit.objects.get(slug=slug)
  return subreddit

#@cache_page(60 * 15)
def index(request,subreddit=None,nsfw=False):
  nsfw = bool(nsfw)
  subreddit = get_subreddit(subreddit,nsfw)
    
  sizes = (
    (100,100),
    (200,200),
    (100,100),
    (200,200),
    (100,100),
    (200,200),
    )
  srs = SubReddit.objects.all()
  values = {
    'subreddit': subreddit,
    'randint': lambda: random.choice(range(31)),
    'subreddits': SubReddit.objects.filter(nsfw=nsfw),
    'sizes': sizes,
    'nsfw': nsfw,
    }
  return TemplateResponse(request,"reddit.html",values)

#@cache_page(60 * 15)
def image(request,subreddit=None,nsfw=False,width=None,height=None,extension=None,num=None):
  subreddit = get_subreddit(subreddit,nsfw)
  if subreddit.nsfw != nsfw:
    pass # return over_18 image with text
  images = Image.objects.filter(subreddit=subreddit)
  images = images.filter(height__gte=height,width__gte=width)
  image = random.choice(images)
  return image.crop_response(int(width),int(height))

def test_page(request):
  values = {
    'randint': lambda: random.choice(range(31)),
    'widths': range(100,200),
    }
  return TemplateResponse(request,"test_page.html",values)

def random_image(_max=800):
  subreddit = SubReddit.objects.get(slug='aww') #random.choice(SubReddit.objects.all())
  images = Image.objects.filter(subreddit=subreddit)
  height =random.choice(range(100,_max))
  width = random.choice(range(100,_max))
  images = images.filter(height__gte=height,width__gte=width)
  if not images:
    print "no image found: %s %sx%s"%(subreddit,width,height)
    return
  image = random.choice(images)
  return image.crop_response(int(width),int(height))


def test(n=500,f=random_image):
  now = datetime.datetime.now()
  while n>0:
    f()
    n-=1
  t = datetime.datetime.now()-now
  print t.seconds,'\t',t.microseconds
