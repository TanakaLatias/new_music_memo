from django.shortcuts import reverse, redirect
import datetime
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SongForm, SceneForm, PostForm, ListenedForm
from .models import User, Song, Scene, Poll, Post, Like, Listened
from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError

class UserCheckMixin:
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        object = self.get_object()
        if object.user != self.request.user:
            return redirect('error')
        return super().get(request, *args, **kwargs)

class FormCreateView(LoginRequiredMixin, CreateView):
    template_name = 'htmls/basic_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FormUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'htmls/basic_form.html'
    success_url = reverse_lazy('top')
    
class ErrorView(TemplateView):
    template_name = 'htmls/error.html'

class TopAndIndexView(TemplateView):
    template_name = 'htmls/top.html'

class UserDetailView(DetailView):
    model = User
    template_name = 'htmls/user_detail.html'
    context_object_name = 'the_user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = 'user_detail'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        if self.request.user == the_user:
            context['posts'] = Post.objects.filter(user=the_user).order_by('-pk')[:5]
        else:
            context['posts'] = Post.objects.filter(user=the_user, hide=False).order_by('-pk')[:5]
        context['likes'] = Like.objects.filter(user=the_user).order_by('-pk')[:5]
        context['listeneds'] = Listened.objects.filter(user=the_user).order_by('-pk')[:5]
        context['posts_count'] = Post.objects.filter(user=the_user).count()
        context['likes_count'] = Like.objects.filter(user=the_user).count()
        context['listeneds_count'] = Listened.objects.filter(user=the_user).count()
        return context

class UserDetailPostsView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'htmls/user_detail.html'
    paginate_by = 20
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail_posts'] = 'user_detail_posts'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        context['the_user'] = the_user
        context['recent'] =  datetime.datetime.now() - datetime.timedelta(days=3)
        context['posts_count'] = Post.objects.filter(user=the_user).count()
        return context
    def get_queryset(self):
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        if self.request.user == the_user:
            return Post.objects.filter(user=the_user).order_by('-pk')
        else:
            return Post.objects.filter(user=the_user, hide=False).order_by('-pk')

class UserDetailLikesView(LoginRequiredMixin, ListView):
    model = Like
    context_object_name = 'likes'
    template_name = 'htmls/user_detail.html'
    paginate_by = 20
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail_likes'] = 'user_detail_likes'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        context['the_user'] = the_user
        context['likes_count'] = Like.objects.filter(user=the_user).count()
        return context
    def get_queryset(self):
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        return Like.objects.filter(user=the_user).order_by('-pk')

class UserDetailListenedsView(LoginRequiredMixin, ListView):
    model = Listened
    context_object_name = 'listeneds'
    template_name = 'htmls/user_detail.html'
    paginate_by = 50
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail_listeneds'] = 'user_detail_listeneds'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        context['the_user'] = the_user
        context['listeneds_count'] = Listened.objects.filter(user=the_user).count()
        return context
    def get_queryset(self):
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        return Listened.objects.filter(user=the_user).order_by('-pk')

class UserUpdateView(FormUpdateView):
    model = User
    fields = ['username']
    def get_object(self, queryset=None):
        return self.request.user
    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.request.user.pk})

class BaseSongIndex(ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'htmls/song_index.html'
    paginate_by = 50
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SongIndexView(BaseSongIndex):
    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'index': 'index'}
    def get_queryset(self):
        return super().get_queryset().order_by('singer')

class SongIndexPostedView(BaseSongIndex):
    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'index_posted': 'index_posted'}
    def get_queryset(self):
        return super().get_queryset().annotate(post_count=Count('post')).order_by('-post_count', 'singer')

class SongIndexScenedView(BaseSongIndex):
    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'index_scened': 'index_scened'}
    def get_queryset(self):
        return super().get_queryset().annotate(scened_count=Count('scene')).order_by('-scened_count', 'singer')

class SongIndexListenedView(BaseSongIndex):
    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'index_listened': 'index_listened'}
    def get_queryset(self):
        return super().get_queryset().annotate(listened_count=Count('listened')).order_by('-listened_count', 'singer')

class SongSearchView(ListView):
    model = Song
    context_object_name = 'search_results'
    template_name = 'htmls/song_index.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Song.objects.filter(Q(title__icontains=query) | Q(singer__icontains=query)).order_by('singer', 'title')
        else:
            return Song.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_search'] = 'song_search'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class SongDetailPostView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'htmls/song_detail.html'
    paginate_by = 20
    def get_queryset(self):
        the_song = Song.objects.get(pk=self.kwargs.get('pk'))
        return Post.objects.filter(song=the_song, hide=False).order_by('-pk')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_detail_post'] = 'song_detail_post'
        the_song = Song.objects.get(pk=self.kwargs.get('pk'))
        context['the_song'] = the_song
        context['posts_count'] = Post.objects.filter(song=the_song).count()
        if self.request.user.is_authenticated:
            try:
                query = Post.objects.filter(user=self.request.user, song=the_song)
                if query.exists():
                    context['your_post'] = Post.objects.get(pk=query.first().pk)
            except Post.DoesNotExist:
                pass
        return context

class SongDetailListenedView(ListView):
    model = Listened
    context_object_name = 'listeneds'
    template_name = 'htmls/song_detail.html'
    paginate_by = 20
    def get_queryset(self):
        the_song = Song.objects.get(pk=self.kwargs.get('pk'))
        return Listened.objects.filter(song=the_song).order_by('-pk')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_detail_listened'] = 'song_detail_listened'
        the_song = Song.objects.get(pk=self.kwargs.get('pk'))
        context['the_song'] = the_song
        context['listeneds_count'] = Listened.objects.filter(song=the_song).count()
        if self.request.user.is_authenticated:
            context['your_listeneds'] = Listened.objects.filter(user=self.request.user, song=the_song)
        return context

class SongDetailSceneView(ListView):
    model = Scene
    context_object_name = 'scenes'
    template_name = 'htmls/song_detail.html'
    paginate_by = 20
    def get_queryset(self):
        the_song = Song.objects.get(pk=self.kwargs.get('pk'))
        return Scene.objects.filter(song=the_song).annotate(poll_count=Count('poll')).order_by('-poll_count', '-pk')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_detail_scene'] = 'song_detail_scene'
        the_song = Song.objects.get(pk=self.kwargs.get('pk'))
        context['the_song'] = the_song
        context['scenes_count'] = Scene.objects.filter(song=the_song).count()
        if self.request.user.is_authenticated:
            try:
                polls = Poll.objects.filter(user=self.request.user, scene__song=the_song)
                context['polls_dict'] = {poll.scene.pk: poll.pk for poll in polls}
            except:
                pass
        return context

class SongCreateView(FormCreateView):
    model = Song
    form_class = SongForm
    success_url = reverse_lazy('top')
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('song_detail_post', kwargs={'pk': self.object.pk}))
        except IntegrityError:
            return redirect(reverse('error'))

class SongUpdateView(FormUpdateView):
    model = Song
    form_class = SongForm
    def get_success_url(self):
        return reverse('song_detail_post', kwargs={'pk': self.object.pk})

class SceneCreateView(FormCreateView):
    model = Scene
    form_class = SceneForm
    success_url = reverse_lazy('top')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['default_song'] = Song.objects.get(pk=self.kwargs.get('pk'))
        return kwargs
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('song_detail_scene', kwargs={'pk': self.kwargs.get('pk')}))
        except IntegrityError:
            return redirect(reverse('error'))

class PostIndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'htmls/post_index.html'
    paginate_by = 20
    def get_queryset(self):
        return Post.objects.filter(hide=False).order_by('-pk')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent'] =  datetime.datetime.now() - datetime.timedelta(days=3)
        return context
    
class PostSearchView(ListView):
    model = Post
    context_object_name = 'search_results'
    template_name = 'htmls/post_index.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query)).order_by('-pk')
        else:
            return Post.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_search'] = 'post_search'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'htmls/post_detail.html'
    context_object_name = 'post'
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if post.hide and post.user != self.request.user:
            return redirect('error')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        the_post = Post.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user.is_authenticated:
            try:
                liked = Like.objects.get(user=self.request.user, post=the_post)
                context['liked'] = liked
            except Like.DoesNotExist:
                pass
        context['liked_count'] = Like.objects.filter(post=the_post).count()
        return context

class PostCreateView(FormCreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('top')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['default_song'] = Song.objects.get(pk=self.kwargs.get('pk'))
        return kwargs
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('post_detail', kwargs={'pk': self.object.pk}))
        except IntegrityError:
            return redirect(reverse('error'))

class PostUpdateView(FormUpdateView, UserCheckMixin):
    model = Post
    form_class = PostForm
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('post_detail', kwargs={'pk': self.kwargs.get('pk')}))
        except IntegrityError:
            return reverse('error')

class PostDeleteView(LoginRequiredMixin, UserCheckMixin, DeleteView):
    model = Post
    template_name = 'htmls/basic_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_index')

class ListenedIndexView(ListView):
    model = Listened
    context_object_name = 'listeneds'
    template_name = 'htmls/listened_index.html'
    paginate_by = 50
    def get_queryset(self):
        return Listened.objects.order_by('-pk')

class ListenedSearchView(ListView):
    model = Listened
    context_object_name = 'search_results'
    template_name = 'htmls/listened_index.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Listened.objects.filter(Q(song__title__icontains=query)).order_by('-pk')
        else:
            return Listened.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listened_search'] = 'listened_search'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ListenedDetailView(DetailView):
    model = Listened
    template_name = 'htmls/listened_detail.html'
    context_object_name = 'listened'
    def get(self, request, *args, **kwargs):
        listened = self.get_object()
        return super().get(request, *args, **kwargs)

class ListenedCreateView(FormCreateView):
    model = Listened
    form_class = ListenedForm
    success_url = reverse_lazy('top')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['default_song'] = Song.objects.get(pk=self.kwargs.get('pk'))
        return kwargs
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('listened_detail', kwargs={'pk': self.object.pk}))
        except IntegrityError:
            return redirect(reverse('error'))

class ListenedUpdateView(FormUpdateView, UserCheckMixin):
    model = Listened
    form_class = ListenedForm
    def get_success_url(self):
        return reverse('listened_detail', kwargs={'pk': self.object.pk})

class ListenedDeleteView(LoginRequiredMixin, UserCheckMixin, DeleteView):
    model = Listened
    template_name = 'htmls/basic_delete.html'
    context_object_name = 'listened'
    success_url = reverse_lazy('listened_index')

class ClickCreateView(LoginRequiredMixin, CreateView):
    model = None
    fields = []
    template_name = 'htmls/basic_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            self.handle_additional_fields(form)
            form.save()
            return self.get_redirect_url()
        except IntegrityError:
            return redirect('error')
    def handle_additional_fields(self, form):
        pass
    def get_redirect_url(self):
        pass

class LikeCreateView(ClickCreateView):
    model = Like
    def handle_additional_fields(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
        if form.instance.post.hide:
            return redirect('error')
    def get_redirect_url(self):
        return redirect(reverse('post_detail', kwargs={'pk': self.kwargs.get('pk')}))

class PollCreateView(ClickCreateView):
    model = Poll
    def handle_additional_fields(self, form):
        form.instance.scene = Scene.objects.get(pk=self.kwargs.get('pk'))
    def get_redirect_url(self):
        scene = Scene.objects.get(pk=self.kwargs.get('pk'))
        return redirect(reverse('song_detail_scene', kwargs={'pk': scene.song.pk}))
    
class ClickDeleteView(LoginRequiredMixin, UserCheckMixin, DeleteView):
    template_name = 'htmls/basic_delete.html'
    success_url = reverse_lazy('top')
    model = None
    def get_success_url(self):
        pass
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs.get('pk'))
    
class SceneDeleteView(ClickDeleteView):
    model = Scene
    def get_success_url(self):
        scene = self.get_object()
        return reverse('song_detail_scene', kwargs={'pk': scene.song.pk})

class LikeDeleteView(ClickDeleteView):
    model = Like
    def get_success_url(self):
        like = self.get_object()
        return reverse('post_detail', kwargs={'pk': like.post.pk})

class PollDeleteView(ClickDeleteView):
    model = Poll
    def get_success_url(self):
        poll = self.get_object()
        return reverse('song_detail_scene', kwargs={'pk': poll.scene.song.pk})