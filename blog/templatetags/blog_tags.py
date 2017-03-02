from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Post


register = template.Library()


# 返回字符串
@register.simple_tag
def total_posts():
    return Post.published.count()


# 返回渲染过的模板
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# 返回数据,需要设置变量来赋值
@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
