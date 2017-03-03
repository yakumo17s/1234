#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    # 之前写错成(models.Model)后,view中的Post.published.all()会报错,没有 all 方法
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                                            .filter(status='published')
    # todo get_queryset 函数的原理.


class Post(models.Model):
    class Meta:
        ordering = ('-publish', )

        def __str__(self):
            return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    # slug
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    # related_name的作用,可以使用User的实例 user.blog_posts 获得该表
    # 默认为post_set ,小写的模型名后加上 _set
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    # todo 这个 publish  created 有什么区别?为什么 timezone.now()会报错
    # timezone.now()的话只会在 models.py 读取时执行一次,timezone.now 会在每次创建新实例时执行.
    publish = models.DateTimeField(default=timezone.now)
    # auto_now_add 创建时自动设置为当前时间
    created = models.DateTimeField(auto_now_add=True)
    # auto_now 每次 save()时设置为现在时间
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICE,
                              default='draft')
    objects = models.Manager()  # the default manager
    published = PublishedManager()  # Our custom manager

    tags = TaggableManager()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)






