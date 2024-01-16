from django import template
from ..models import Quote, Tag, Author

register = template.Library()


def get_author(author_id):
    author = Author.objects.filter(id=author_id).get()
    return author.fullname

def get_tags(quote):
    tgs = quote.tags.all()
    tags = []
    for tag in tgs:
        tags.append(tag.name)
    return tags

register.filter('author', get_author)
register.filter('tags', get_tags)

