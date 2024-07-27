from django.contrib import admin
from .models import Author, Tag, Post, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',),}
    list_display = ('title', 'author', 'publish_time')
    list_filter = ('author', 'tag', 'publish_time')
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post']

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)