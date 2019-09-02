from django.conf import settings
from django.core.mail import mail_admins
from django.core.management.base import BaseCommand
from reddit.models import SubReddit
import datetime

class Command (BaseCommand):
  def handle(self, *args, **options):
    results = []
    print "UPDATING %s SUBREDDITS"%SubReddit.objects.count(), datetime.datetime.now()
    for s in SubReddit.objects.all():
      images = s.pull_from_imgur()
      if images:
        results.append("%s images %s"%(s,len(images)))
    print "DONE"