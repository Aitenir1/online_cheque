import csv
import urllib.parse
import requests
from PIL import Image
import io

from django.core.management.base import BaseCommand
from api.models import Category, Dish

class Command(BaseCommand):
    help = 'Import data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options.get('file_path')
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            response_status_codes = {}
            for row in reader:
                name = row['name'].strip()
                description = row['description'].strip()
                price = int(row['price']) if row['price'] else None
                gram = row['gram'].strip()
                category = row['category'].strip()
                image_url = row['image']

                print(f"{name=}")
                print(f"{image_url=}")
                print("=============================")

                img_parsed_url = urllib.parse.urlparse(image_url)
                img_path = img_parsed_url.path.split('/')[-1]

                if "." not in img_path:
                    img_path += '.jpg'

                headers = requests.utils.default_headers()

                headers.update(
                    {
                        'User-Agent': 'My User Agent 1.0',
                    }
                )

                response = requests.get(image_url, headers=headers)
                status_code = response.status_code

                if status_code in response_status_codes:
                    response_status_codes[status_code] += 1
                else:
                    print(status_code)
                    response_status_codes[status_code] = 1

                category, created = Category.objects.get_or_create(
                    name=category
                )

                dish, created = Dish.objects.get_or_create(
                    name_en=name,
                    name_ru=name,
                    name_kg=name,
                    description_en=description,
                    description_ru=description,
                    description_kg=description,
                    price=price,
                    gram=gram,
                    category=category,
                )

                dish.image.save(
                    img_path,
                    io.BytesIO(response.content),
                    save=True
                )

                dish.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

