from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse

from .models import Episode, Series, Tag

# Create your views here.
def index(request, title_slug):
    series = get_object_or_404(Series, slug=title_slug)
    all_tag_counts = []
    lowest_count = Episode.objects.all().count() # upper bound on lowest
    highest_count = 0
    for tag in Tag.objects.all():
        tag_count = Episode.objects.filter(comic=series, tags=tag).count()
        if tag_count:
            slug_name_count = (tag.slug, tag.name, tag_count)
            all_tag_counts.append(slug_name_count)
            if tag_count < lowest_count:
                lowest_count = tag_count
            if highest_count < tag_count:
                highest_count = tag_count
    # rescale counts linearly from 0.75 to 2, for display purposes,
    # unless all tags have the same count, in which case have them all
    # be size 1
    slope = 0
    offset = 1
    if (highest_count != lowest_count):
        slope = 1.25 / (highest_count - lowest_count)
        offset = 2 - 1.25 / (1 - lowest_count / highest_count)
    def rescale(num):
        return round(slope * num + offset, 2)
    all_tag_data = [(slug, name, rescale(count)) for (slug, name, count) in all_tag_counts]
    all_tag_data.sort(key=lambda x: x[0])
    all_episodes = series.episode_set.all().order_by('num')
    first_num = 0
    if all_episodes.count():
        first_num = all_episodes[0].num
    context = {
        'series_title': series.title,
        'series_slug': title_slug,
        'series_blurb': series.blurb,
        'episode_list': all_episodes,
        'all_tag_data': all_tag_data,
        'first_num': first_num
    }
    return render(request, 'comic/index.html', context)

def episode(request, title_slug, episode_num):
    series = get_object_or_404(Series, slug=title_slug)
    this_epi = get_object_or_404(Episode, num=episode_num, comic=series)
    first_epi_num = 0
    prev_epi_num = 0
    next_epi_num = 0
    last_epi_num = 0
    before_epi = Episode.objects.filter(num__lt=episode_num).order_by('num')
    after_epi = Episode.objects.filter(num__gt=episode_num).order_by('num')
    if before_epi:
        first_epi_num = before_epi.first().num
        prev_epi_num = before_epi.last().num
    if after_epi:
        next_epi_num = after_epi.first().num
        last_epi_num = after_epi.last().num
    context = {
        'series_title': series.title,
        'series_slug': title_slug,
        'this_epi_num': episode_num,
        'first_epi_num': first_epi_num,
        'prev_epi_num': prev_epi_num,
        'next_epi_num': next_epi_num,
        'last_epi_num': last_epi_num,
        'episode_notes': this_epi.notes,
        'episode_img_url': this_epi.imgFile.url,
        'tags': this_epi.tags.all(),
        'transcript': this_epi.transcript
    }
    return render(request, 'comic/episode.html', context)

def tag(request, title_slug, tag_slug):
    series = get_object_or_404(Series, slug=title_slug)
    tag = get_object_or_404(Tag, slug=tag_slug)
    episode_list = Episode.objects.filter(comic=series, tags__slug=tag_slug)
    context = {
        'series_title': series.title,
        'series_slug': title_slug,
        'tag': tag,
        'episode_list': episode_list.order_by('num')
    }
    return render(request, 'comic/tag.html', context)
