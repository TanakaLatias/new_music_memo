import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
from new_music_memo.models import Song, Listened
from django.contrib.auth.models import User

def add_listeneds():
    for i in range(50):
        memo_text = str(i) + ": A memo, short for memorandum, is a concise written message used in business or organizations to communicate information internally. Typically, memos are brief, containing key points or instructions regarding specific topics such as policy changes, meeting agendas, updates, or announcements. They often follow a standardized format with headings like 'To', 'From,' 'Date,' and 'Subject' to ensure clarity and organization. Memos facilitate efficient communication within an organization, allowing for quick dissemination of important information to relevant parties. They serve as a formal means of communication, aiding in coordination, decision-making, and documentation of internal affairs."
        random_song = Song.objects.get(pk=random.randint(1, 98))
        random_user = User.objects.get(pk=random.randint(1,14))
        listened = Listened.objects.get_or_create(memo=memo_text, song=random_song, user=random_user)[0]
        print(random_song, random_user)
        listened.save()

if __name__ == "__main__":
    print('adding_listeneds')
    add_listeneds()
    print('all_added')