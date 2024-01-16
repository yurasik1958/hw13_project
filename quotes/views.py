from django.contrib import messages
from dateutil.parser import *
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Min, Sum

from .models import Quote, Tag, Author
from .forms import TagForm, QuoteForm, AuthorForm


def _main_(query_set, page):
    per_page = 10
    top_tags = Quote.objects.values('tags__name').annotate(tag_count=Count('tags__name')).order_by('-tag_count')
    top = []
    size = 28
    for tag in top_tags:
        print(f'name: {tag["tags__name"]}, count: {tag["tag_count"]}, tag_size: {size}')
        top.append({'tag_name': tag["tags__name"], 'tag_size': size})
        size -= 2
        if len(top) >= per_page:
            break
    paginator = Paginator(list(query_set), per_page)
    quotes_on_page = paginator.page(page)
    return quotes_on_page, top


def main(request, page=1):
    quotes = Quote.objects.all()
    quotes_on_page, top = _main_(quotes, page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, 'top_tags': top})


def quote(request, quote_id):
    quotes = Quote.objects.filter(id=quote_id).get()
    return render(request, 'quotes/quote.html', context={'quote': quotes})


def author(request, author_id):
    authors = Author.objects.filter(id=author_id).get()
    return render(request, 'quotes/author.html', context={'author': authors})


def quotes_tag(request, tag_name, page=1):
    quotes = Quote.objects.filter(tags__name=tag_name).all()
    quotes_on_page, top = _main_(quotes, page)
    prev_page = '#' if not quotes_on_page.has_previous() else f'/tag/{tag_name}/page/{quotes_on_page.previous_page_number()}'
    next_page = '#' if not quotes_on_page.has_next() else f'/tag/{tag_name}/page/{quotes_on_page.next_page_number()}'
    return render(request, 'quotes/index.html', context={'tag_name': tag_name, 'quotes': quotes_on_page, 'prev_page': prev_page, 'next_page': next_page, 'top_tags': top})


@login_required
def author_add(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.born_date = parse(author.born_date).strftime('%B %d, %Y')
            author.user = request.user
            author.save()
            return redirect(to='quotes:author-view')
        else:
            return render(request, 'quotes/author-add.html', {'form': form})

    return render(request, 'quotes/author-add.html', {'form': AuthorForm()})


@login_required
def author_view(request, page=1):
    authors = Author.objects.filter(user=request.user).all()
    per_page = 10
    paginator = Paginator(list(authors), per_page)
    authors_on_page = paginator.page(page)
    for author in authors_on_page:
        bl = str(author.born_location)
        if not bl.startswith('in '):
            author.born_location = f'in {bl}'
    return render(request, 'quotes/author-view.html', context={'authors': authors_on_page})


@login_required
def quote_add(request):
    tags = Tag.objects.order_by('name').all()
    authors = Author.objects.order_by('fullname').all()

    print(f'quote_add: {request.method}')
    if request.method == 'POST':
        req = request.POST.dict()

        auth = Author.objects.filter(fullname=req['author']).get()
        req['author'] = auth

        form = QuoteForm(req)
        
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.quote = req['quote']
            new_quote.author = auth
            new_quote.save()

            tag_str = str(req['tag_str'])
            if tag_str:
                tag_str = tag_str.replace(' ', '').split(',')
                for tag_name in tag_str:
                    tag, *_ = Tag.objects.get_or_create(name=tag_name)
                    print(tag.name)
                    new_quote.tags.add(tag)

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                print(tag.name)
                new_quote.tags.add(tag)

            return redirect(to='quotes:main')
        else:
            messages.error(request, f'POST error! {form.errors.values()}')
            return render(request, 'quotes/quote-add.html', {"authors": authors, 'tags': tags, 'form': form})

    return render(request, 'quotes/quote-add.html', {"authors": authors, 'tags': tags, 'form': QuoteForm()})


@login_required
def quote_view(request, page=1):
    quotes = Quote.objects.filter(user=request.user).all()
    quotes_on_page, top = _main_(quotes, page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, 'top_tags': top})
