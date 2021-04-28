import json
import os

from django.core.management.base import BaseCommand
from musics.models import Song
from urllib import request as request
from urllib.parse import urlparse
import requests
from django.core.files.base import ContentFile
from django.core.files import File


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('a2.json', type=str)

    def handle(self, *args, **options):
        with open(options['a2.json']) as f:
            data_list = json.load(f)

        for k, data in enumerate(data_list['songs']):
            print(data)
            # data['pk'] = k
            # Song.objects.get_or_create(pk=data['pk'], defaults=data)
            song= Song(title= data['title'], year= int(data['year']), url=data['web_url'], artist= data['artist'], image_url=data['img_url'])
            # result,_ = request.urlretrieve(song.image_url)
            # print(result)
            # song.image.save(
            #     os.path.basename(song.image_url),
            #     File(open(result))
            # )
            img_url = data['img_url']
            name = urlparse(img_url).path.split('/')[-1]
            response = requests.get(img_url)
            if response.status_code == 200:
                song.image.save(name, ContentFile(response.content), save=True)
            song.save()
