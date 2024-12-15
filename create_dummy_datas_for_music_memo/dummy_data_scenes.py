import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
from new_music_memo.models import Song, Scene
from django.contrib.auth.models import User
from collections import defaultdict

def add_scenes():
    for i in range(50):
        random_song = Song.objects.get(pk=random.randint(1, 99))
        random_user = User.objects.get(pk=random.randint(1,14))
        scene_name = "scene" + str(i) + ": " + str(random_song.title)
        scene = Scene.objects.get_or_create(title=scene_name, song=random_song, user=random_user)[0]
        print(scene_name, random_user.username, random_song.title)
        scene.save()

if __name__ == "__main__":
    print('adding_scenes')
    add_scenes()
    print('all_added')