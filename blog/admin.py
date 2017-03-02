from django.contrib import admin
from .models import Post, Comment

# admin.site.register(Post)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body', 'post')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)  #修改下拉选择为直接输入 id
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)