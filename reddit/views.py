from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

from .models import SubReddit, Image

import random

@cache_page(60 * 15)
def index(request,subreddit=None,nsfw=False):
  if not subreddit:
    subreddit = SubReddit.objects.all()[random.randint(0,SubReddit.objects.count()-1)]
  else:
    subreddit = subreddit.objects.get(name=subreddit)
  if subreddit.nsfw != nsfw:
    pass # return error
  values = {'subreddit':subreddit}
  return TemplateResponse(request,"example.html",values)

@cache_page(60 * 15)
def image(request,subreddit=None,nsfw=False,width=None,height=None,extension=None,num=None):
  sr = get_object_or_404(SubReddit,name=subreddit,nsfw=bool(nsfw))
  images = Image.objects.filter(subreddit=sr)
  images = images.filter(height__gte=height,width__gte=width)
  image = random.choice(images)
  return image.crop_response(int(width),int(height))
