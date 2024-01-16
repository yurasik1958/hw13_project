import os
import django
import json
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw13_project.settings")
django.setup()

from quotes.models import Quote, Tag, Author

def load_json(filename):
    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data

def load_data():
    a_list = {}
    pathname = Path(__file__).resolve().parent
    authors = load_json(pathname.joinpath('data/authors.json'))
    for auth in authors:
        fn = auth.get("fullname")
        bd = auth.get("born_date")
        author, *_ = Author.objects.get_or_create(
                        fullname = fn,
                        born_date = bd,
                        born_location = auth.get("born_location"),
                        description = auth.get("description")
                    )
        a_list.update({fn: author})
    
    quotes = load_json(pathname.joinpath('data/quotes.json'))
    for quot in quotes:
        tags = []
        for tag in quot.get('tags'):
            t, *_ = Tag.objects.get_or_create(name=tag)
            tags.append(t)

        q1 = quot.get("quote")
        exists_quote = bool(len(Quote.objects.filter(quote=q1)))
        if not exists_quote:
            auth = a_list.get(quot.get("author"))
            quote = Quote.objects.create(
                quote = q1,
                author = auth
            )
            for tag in tags:
                quote.tags.add(tag)


if __name__ == '__main__':
    load_data()
