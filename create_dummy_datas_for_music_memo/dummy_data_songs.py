import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

from new_music_memo.models import Song

def add_songs():
    
    for x in range(100):
        song_name = "song" + str(x)
        singer_name = "singer" + str(x)
        song = Song.objects.get_or_create(title=song_name, singer=singer_name)[0]
        print(song_name, singer_name)
        song.save()

if __name__ == "__main__":
    print('adding_songs')
    add_songs()
    print('all_added')