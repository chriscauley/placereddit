from django.contrib import admin
from .models import SubReddit, Image

class ImageAdmin(admin.ModelAdmin):
  list_display = ("__unicode__","view_imgur","width","height")
  list_filter = ('subreddit',)
  def view_imgur(self,obj):
    return '<a href="%s">%s</a>'%(obj.url,obj.url.split('/')[-1])
  view_imgur.allow_tags = True

admin.site.register(SubReddit)
admin.site.register(Image,ImageAdmin)
