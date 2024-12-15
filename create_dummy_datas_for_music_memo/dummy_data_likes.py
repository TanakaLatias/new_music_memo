import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
from new_music_memo.models import Post, Like
from django.contrib.auth.models import User
from collections import defaultdict

def add_likes():
    sets = defaultdict(list)
    other_sets = defaultdict(list)
    for i in range(50):
        random_user = User.objects.get(pk=random.randint(1,14))
        random_post=Post.objects.get(pk=random.randint(1,48))
        if random_post.title not in sets[random_user.username] and random_post.user != random_user:
            sets[random_user.username].append(random_post.title)
            like = Like.objects.get_or_create(post=random_post, user=random_user)[0]
            print(random_user.username, random_post.title)
            like.save()
        else:
            other_sets[random_user.username].append(random_post.title)
    print("--")
    for k, v in other_sets.items():
        print(k, v)
    print("--")

if __name__ == "__main__":
    print('adding_likes')
    add_likes()
    print('all_added')