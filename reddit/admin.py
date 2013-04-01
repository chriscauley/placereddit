from django.contrib import admin
from .models import SubReddit, Image, Subject

class SubRedditAdmin(admin.ModelAdmin):
  list_display = ("__unicode__",'featured','nsfw','last_featured')
  list_editable = ('featured','nsfw','last_featured')

class ImageAdmin(admin.ModelAdmin):
  list_display = ("__unicode__","view_imgur","width","height")
  list_filter = ('subreddit',)
  search_fields = ['url']
  def view_imgur(self,obj):
    return '<a href="%s">%s</a>'%(obj.url,obj.url.split('/')[-1])
  view_imgur.allow_tags = True

class SubjectAdmin(admin.ModelAdmin):
  filter_horizontal = ['subreddits']

admin.site.register(SubReddit,SubRedditAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Subject,SubjectAdmin)
