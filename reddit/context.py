from .models import SubReddit

import re, random

def get_subreddit(request):
  reg_exp = re.compile(r'^r/([\w\d\_\-]+)/(nsfw/)?')
  slug, nsfw = reg_exp.match(request.path)
  if slug == 'featured':
    subreddit = SubReddit.objects.get_featured()
  elif not slug or slug == 'random':
    r = random.randint(0,SubReddit.objects.filter(nsfw=nsfw).count()-1)
    subreddit = SubReddit.objects.filter(nsfw=nsfw)[r]
  else:
    subreddit = SubReddit.objects.get(slug=slug)
  return {
    'subreddit': subreddit,
    'nsfw': bool(nsfw),
    }
