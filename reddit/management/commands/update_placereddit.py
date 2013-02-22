from django.core.management.base import BaseCommand
from reddit.models import SubReddit

class Command (BaseCommand):
  def handle(self, *args, **options):
    for s in SubReddit.objects.all():
      s.pull_from_imgur()
