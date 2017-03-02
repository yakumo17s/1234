from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count

from taggit.models import Tag

from .models import Post, Comment
from .form import EmailPostForm, CommentForm


class PostListView(ListView):
    # default is Post.objects.all()
    queryset = Post.published.all()
    # default is 'object_list'
    context_object_name = 'posts'
    # ListView 把 paginate 对象放在page_obj
    paginate_by = 3
    # default is 'blog/post_list.html'
    template_name = 'blog/post/list.html'


# 使用了 class PostListView(ListView)来代替
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = ''

    if request.method == 'POST':
        # A comment was posted
        # 将字典赋给data会自动转换成表单数据
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment object but don't save to database yet
            #  创建 modle 实例,但不写入数据库
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            # todo new_comment无法传到 template 中,{% if new_comment %} 无法为 True
            # view 中添加了 new_comment=''并将其传入 template 中,这样就可以解决问题,但书上错了?还是有什么没注意到的地方
            new_comment.save()
    else:
        #  现在是非 POST 方法时会生成 CommentForm 的实例,那么当提交了 POST 后呢?
        #  生成了之后就会一直保存在页面内
        comment_form = CommentForm()

        # List of similar posts
        # 当前 post的所有 tag的 id
        # flat=True : [1, 2, 3] ; flat=False: [(1,), (2, ), (3, )]
    post_tags_ids = post.tags.values_list('id', flat=True)
    # print(post_tags_ids)
    # todo tags__in
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    # annotate 相对于 all,多给返回的 queryset 加了一个Count 方法,可以使用 post.same_tags
    # Count 计算 该post有多少 tags,赋值起别名same_tags = tags__count
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'new_comment': new_comment,
                   'similar_posts': similar_posts})


def post_share(request, post_id):

    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            # a dictionary of valid value
            cd = form.cleaned_data
            # send email
            # post.get_absolute_url()得到页面的地址/blog/2016/10/18/one-more-post/
            # request.build_absolute_uri 加上HTTP scheme 和 hostname
            # <http://>HTTP scheme   <myweb.site>hostname
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            # format中的每一个值会对应的替换一个{}
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'wo409697458@163.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
