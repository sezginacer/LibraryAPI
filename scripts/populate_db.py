# can be used in order to populate database initialy..
"""
https://progressbar-2.readthedocs.io/en/latest/usage.html#combining-progressbars-with-print-output
Read above doc for progressbar library
"""

from main.models import Book, Author
from django.db.utils import OperationalError
from datetime import datetime
import progressbar


def run():
    Book.objects.all().delete()
    Author.objects.all().delete()
    file_name = 'random-generator/records.csv'
    f = open(file_name, 'r')
    csv_data = f.read().strip()
    csv_lines = csv_data.split('\n')
    count = 0
    with progressbar.ProgressBar(max_value=len(csv_lines)) as bar:
        try:
            for line in csv_lines:
                infos = line.strip().split(',')
                b, _ = Book.objects.get_or_create(
                    title=infos[0].title(),
                    lc_classification=infos[1]
                )
                index = 2
                while index < len(infos):
                    a, _ = Author.objects.get_or_create(
                        name=infos[index].title(),
                        surname=infos[index + 1].upper(),
                        birth_date=datetime.strptime(infos[index + 2], '%Y-%m-%d')
                    )
                    b.authors.add(a)
                    index += 3
                b.save()
                count += 1
                bar.update(count)
        except IndexError:
            print('csv data improper!')
        except OperationalError:
            print('DB not created yet! run < ./manage.py migrate >')
        except Exception as err:
            print(err)
    print('database populated successfully!')
