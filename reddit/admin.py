from django.contrib import admin
from .models import SubReddit, Image

class SubRedditAdmin(admin.ModelAdmin):
  list_display = ("__unicode__",'featured','nsfw','last_featured')
  list_editable = ('featured','nsfw','last_featured')

class ImageAdmin(admin.ModelAdmin):
  list_display = ("__unicode__","view_imgur","width","height")
  list_filter = ('subreddit',)
  def view_imgur(self,obj):
    return '<a href="%s">%s</a>'%(obj.url,obj.url.split('/')[-1])
  view_imgur.allow_tags = True

admin.site.register(SubReddit,SubRedditAdmin)
admin.site.register(Image,ImageAdmin)
