from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # top
    path('', TopAndIndexView.as_view(), name='top'),
    # users
    path('user_detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('user_detail_posts/<int:pk>', UserDetailPostsView.as_view(), name='user_detail_posts'),
    path('user_detail_likes/<int:pk>', UserDetailLikesView.as_view(), name='user_detail_likes'),
    path('user_detail_listened/<int:pk>', UserDetailListenedsView.as_view(), name='user_detail_listened'),
    path('user_update', UserUpdateView.as_view(), name='user_update'),
    # songs
    path('song_index', SongIndexView.as_view(), name='song_index'),
    path('song_index_posted', SongIndexPostedView.as_view(), name='song_index_posted'),
    path('song_index_scened', SongIndexScenedView.as_view(), name='song_index_scened'),
    path('song_index_listened', SongIndexListenedView.as_view(), name='song_index_listened'),
    path('song_search', SongSearchView.as_view(), name='song_search'),
    path('song_detail_post/<int:pk>', SongDetailPostView.as_view(), name='song_detail_post'),
    path('song_detail_listened/<int:pk>', SongDetailListenedView.as_view(), name='song_detail_listened'),
    path('song_detail_scene/<int:pk>', SongDetailSceneView.as_view(), name='song_detail_scene'),
    path('song_create', SongCreateView.as_view(), name='song_create'),
    path('song_update/<int:pk>', SongUpdateView.as_view(), name='song_update'),
    # scene
    path('scene_create/<int:pk>', SceneCreateView.as_view(), name='scene_create'),
    path('scene_delete/<int:pk>', SceneDeleteView.as_view(), name='scene_delete'),
    # posts
    path('post_index', PostIndexView.as_view(), name='post_index'),
    path('post_search', PostSearchView.as_view(), name='post_search'),
    path('post_detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post_create/<int:pk>', PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    # likes
    path('like_create/<int:pk>', LikeCreateView.as_view(), name='like_create'),
    path('like_delete/<int:pk>', LikeDeleteView.as_view(), name='like_delete'),
    # polls
    path('poll_create/<int:pk>', PollCreateView.as_view(), name='poll_create'),
    path('poll_delete/<int:pk>', PollDeleteView.as_view(), name='poll_delete'),
    # Listeneds
    path('listened_index', ListenedIndexView.as_view(), name='listened_index'),
    path('listened_search', ListenedSearchView.as_view(), name='listened_search'),
    path('listened_detail/<int:pk>', ListenedDetailView.as_view(), name='listened_detail'),
    path('listened_create/<int:pk>', ListenedCreateView.as_view(), name='listened_create'),
    path('listened_update/<int:pk>', ListenedUpdateView.as_view(), name='listened_update'),
    path('listened_delete/<int:pk>', ListenedDeleteView.as_view(), name='listened_delete'),
    # errors
    path('error',ErrorView.as_view(), name='error'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
