from django.forms import ModelForm, CharField, TextInput, Textarea, DateInput, ChoiceField
from .models import Tag, Quote, Author


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=100, required=True, widget=TextInput())
    born_date = CharField(max_length=30, widget=DateInput())
    born_location = CharField(max_length=120, widget=TextInput())
    description = CharField(widget=Textarea())
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class TagForm(ModelForm):
    name = CharField(min_length=2, max_length=50, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    quote = CharField(required=True, widget=Textarea())
    author = AuthorForm()

    class Meta:
        model = Quote
        fields = ['quote', 'author']
        exclude = ['tags, tag_str']
