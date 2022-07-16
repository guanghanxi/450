import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

from estimator.models import Material


def run():
    fhand = open('estimator/load.csv')
    reader = csv.reader(fhand)
      # Advance past the header


    for row in reader:
        print(row)

        m, created = Material.objects.get_or_create(name=row[0], emission = row[1])
        print(created)