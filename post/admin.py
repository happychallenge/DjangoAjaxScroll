from django.contrib import admin

from .models import Post, Comment

class CommentInline(admin.TabularInline):
	model = Comment
	
# Register your models here.
class PostAdmin(admin.ModelAdmin):
	class Meta:
		model = Post
	list_display = ['title', 'updated_date']
	inlines = [ CommentInline, ]

admin.site.register(Post, PostAdmin)