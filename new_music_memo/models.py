from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=100)
    singer = models.CharField(max_length=100)
    def scene_count(self):
        return self.scene_set.count()
    def post_count(self):
        return self.post_set.filter(hide=False).count()
    def record_count(self):
        return self.record_set.count()
    def __str__(self):
        return self.title
    class Meta:
        constraints = [UniqueConstraint(fields=['title', 'singer'], name='unique_song')]

class Scene(models.Model):
    title = models.CharField(max_length=500)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    def poll_count(self):
        return self.poll_set.count()

class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'scene'], name='unique_poll')]

class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="media/post_images/")
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    hide = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.song} : {self.user.username}'
    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'song'], name='unique_post')]

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.post
    class Meta:
        constraints = [UniqueConstraint(fields=['user', 'post'], name='unique_like')]

class Listened(models.Model):
    memo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.song