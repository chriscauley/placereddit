from django.test import TestCase
from .models import SubReddit

class SimpleTest(TestCase):
  def test_imgur(self):
    s = SubReddit(name="aww",slug="aww")
    s.save()
    s.pull_from_imgur()
