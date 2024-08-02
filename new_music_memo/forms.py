from django import forms
from .models import Song, Scene, Post, Listened

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'singer']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'

class SceneForm(forms.ModelForm):
    class Meta:
        model = Scene
        fields = ['title', 'song']
    def __init__(self, *args, **kwargs):
        default_song = kwargs.pop('default_song', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'
        self.fields['song'].initial = default_song

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'song', 'hide']
    def __init__(self, *args, **kwargs):
        default_song = kwargs.pop('default_song', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'
        self.fields['song'].initial = default_song

class ListenedForm(forms.ModelForm):
    class Meta:
        model = Listened
        fields = ['memo', 'song']
    def __init__(self, *args, **kwargs):
        default_song = kwargs.pop('default_song', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['label'] = None
            field.widget.attrs['class'] = 'form'
        self.fields['song'].initial = default_song