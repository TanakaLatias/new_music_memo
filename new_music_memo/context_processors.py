from .models import Post, Song, Poll, Listened

def side_songs(request):
    side_songs = Song.objects.order_by('-pk')[:10]
    return {'side_songs': side_songs}

def side_polls(request):
    side_polls = Poll.objects.all().order_by('-pk')[:10]
    return {'side_polls': side_polls}

def side_posts(request):
    side_posts = Post.objects.filter(hide=False).order_by('-pk')[:10]
    return {'side_posts': side_posts}

def side_listeneds(request):
    side_listeneds = Listened.objects.all().order_by('-pk')[:10]
    return {'side_listeneds': side_listeneds}