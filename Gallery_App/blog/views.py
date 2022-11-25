from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

from django.db.models import Q
from django.http import Http404


 

# @method_decorator(login_required, name='dispatch')
class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_queryset(self):
        try:
            user = self.request.user
            return Post.objects.filter(author=user).order_by('-date_posted')
        except:
            user = 0
            return Post.objects.filter(author=user).order_by('-date_posted')

# @method_decorator(login_required, name='dispatch')
class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        
        if self.request.user==user:
            return Post.objects.filter(author=user).order_by('-date_posted')
        else:
            raise Http404






class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class Search(ListView):
    model = Post
    template_name = 'blog/home.html'  
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        query=self.request.GET.get('q')
        q1 = Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
        try:
            q2 = Post.objects.filter(author=user).order_by('-date_posted')
            return q2 & q1
        except:
            return q1

