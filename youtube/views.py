from __future__ import unicode_literals
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render
import youtube_dl
from .forms import DownloadForm
import re


def download_video(request):
    global context
    form = DownloadForm(request.POST or None)

    if form.is_valid():
        video_url = form.cleaned_data.get("url")
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
        print(video_url)
        if not re.match(regex, video_url):
            print('Incorrect')
            return HttpResponse('Enter correct url.')

        ydl_opts = {
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                video_url, download=False)
        video_streams = []
        for m in meta['formats']:
            file_size = m['filesize']
            if file_size is not None:
                file_size = f'{round(int(file_size) / 1000000,2)} mb'

            resolution = 'Audio'
            if m['height'] is not None:
                resolution = f"{m['height']}p"
                if m['ext'] != 'webm':
                    video_streams.append({
                        'resolution': resolution,
                        'extension': m['ext'],
                        'file_size': file_size,
                        'video_url': m['url']
                    })
        video_streams = video_streams[::-1]

        audio_streams = []
        for m in meta['formats']:
            file_size = m['filesize']
            if file_size is not None:
                file_size = f'{round((file_size) / 1000000,2)} mb'

            resolution = 'Audio'

            if m['height'] is None and m['ext'] == 'm4a':
                audio_streams.append({
                    'resolution': resolution,
                    'extension': m['ext'],
                    'file_size': file_size,
                    'video_url': m['url']
                })
        audio_streams = audio_streams[::-1]

        context = {
            'form': form,
            'title': meta['title'], 'video_streams': video_streams, 'audio_streams': audio_streams,
            'description': meta['description'], 'likes': meta['like_count'],
            'dislikes': meta['dislike_count'], 'thumb': meta['thumbnails'][3]['url'],
            'duration': round(int(meta['duration'])/60, 2), 'views': f'{int(meta["view_count"]):,}'
        }
        return render(request, 'home.html', context)
    return render(request, 'home.html', {'form': form})
