import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User

users=["sawasawa", "chomi", "pola", "fin", "kyl", "sam", "gab", "wil", "ben", "jet", "wyatt", "nathan", "nicholas"]
passes=["watashinonamae", "kitakami", "hachiware", "foxhound", "kelpiedog", "sennenhund", "goldenretriever", "waterspaniel", "bolognese", "labradorretriever", "weimaraner", "norfolkterrier", "norwegianelkhound"]

def add_users():
    l=int(len(users))
    for i in range(l):
        user = User.objects.get_or_create(username=users[i], password=passes[i], email=users[i]+"@carter.com")[0]
        print(users[i], passes[i], users[i]+"@carter.com")
        user.save()

if __name__ == "__main__":
    print('adding_users')
    add_users()
    print('all_added')