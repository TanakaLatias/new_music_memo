import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
from new_music_memo.models import Song
from collections import defaultdict

def add_posts():
    sets = defaultdict(list)
    other_sets = defaultdict(list)
    for i in range(50):
        post_text = str(i) + ": A story is a crafted narrative that unfolds through characters, setting, plot, and theme. Characters drive the plot forward with their actions, while the setting provides context. The plot follows a sequence of events, from exposition to climax and resolution. Themes explore universal truths, conveyed through symbols and motifs. Style and tone shape the mood, enhancing the reader's experience. In essence, a story is a structured journey, inviting readers to explore themes, empathize with characters, and immerse themselves in imaginary worlds, all while conveying meaning and emotion in a concise and engaging format."
        random_song = Song.objects.get(pk=random.randint(1, 100))
        random_user = User.objects.get(pk=random.randint(1,14))
        post_name = "post" + str(i) + ": " + str(random_song.title)
        if random_song.title not in sets[random_user.username]:
            sets[random_user.username].append(random_song.title)
            post = Post.objects.get_or_create(title=post_name, text=post_text, song=random_song, user=random_user)[0]
            print(post_name, random_song.title, random_user.username)
            post.save()
        else:
            other_sets[random_user.username].append(random_song.title)
    print("--")
    for k, v in other_sets.items():
        print(k, v)
    print("--")

if __name__ == "__main__":
    print('adding_posts')
    add_posts()
    print('all_added')