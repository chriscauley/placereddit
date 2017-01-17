from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

from .models import SubReddit, Image

import random,datetime

def redirect(request,url=''):
  return HttpResponseRedirect(url)

def get_subreddit(slug=None,nsfw=None):
  if slug == 'featured':
    subreddit = SubReddit.objects.get_featured()
  elif not slug or slug == 'random':
    r = random.randint(0,SubReddit.objects.filter(nsfw=nsfw).count()-1)
    subreddit = SubReddit.objects.filter(nsfw=nsfw)[r]
  else:
    subreddit = SubReddit.objects.get(slug__iexact=slug)
  return subreddit

def index(request,slug=None,template=None):
  if not template:
    template = "index"
  nsfw = request.path.startswith('nsfw')
  subreddit = get_subreddit(slug,nsfw)
  a = 100*2
  b = 211*2
  c = 322*2
  side_sizes = [
    [(a,a),(b,a),(b,a),(a,a),(a,a),(a,a),(a,a)],
    [(b,b),(a,a),(a,a),(a,a),(a,a),(a,a)],
    [(a,c),(b,a),(a,a),(a,a),(a,a),(a,a)]
  ]
  side_sizes = (side_sizes*2)[random.choice(range(len(side_sizes))):]
  side_sizes = side_sizes[:2]
  randints = range(21)
  random.shuffle(randints)
  values = {
    'subreddit': subreddit,
    'slug': subreddit.slug,
    'randint': (i for i in randints*2),
    'subreddits': [s for s in SubReddit.objects.filter(nsfw=nsfw) if s.image_set.count()>20],
    'side_rows': side_sizes,
    'nsfw': nsfw,
    'r': 'nsfw' if nsfw else 'r',
    }
  return TemplateResponse(request,template+".html",values)

#@cache_page(60 * 15)
def image(request,slug=None,width=None,height=None,extension=None,num=None):
  nsfw = request.path.startswith('nsfw')
  subreddit = get_subreddit(slug,nsfw)
  if subreddit.nsfw != nsfw:
    pass # return over_18 image with text
  images = Image.objects.filter(subreddit=subreddit,active=True)
  images = images.filter(height__gte=height,width__gte=width)
  if not num:
    num = 0
  index = int(num)%images.count()
  image = images[index]
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
