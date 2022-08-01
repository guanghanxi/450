import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

from estimator.models import Material, Unit, Energy, OtherEnergy, Transportation, Machine, MachinePerformance


def run():
    mthand = open('estimator/data/Material.csv')
    mtreader = csv.reader(mthand)

    ehand = open('estimator/data/Energy.csv')
    ereader = csv.reader(ehand)

    oehand = open('estimator/data/Other_Energy.csv')
    oereader = csv.reader(oehand)

    tphand = open('estimator/data/Transportation.csv')
    tpreader = csv.reader(tphand)

    mchand = open('estimator/data/Machine.csv')
    mcreader = csv.reader(mchand)

    Material.objects.all().delete()
    Transportation.objects.all().delete()
    OtherEnergy.objects.all().delete()
    MachinePerformance.objects.all().delete()
    Machine.objects.all().delete()
    Energy.objects.all().delete()
    Unit.objects.all().delete()

    for row in mtreader:
        print(row)
        u, created = Unit.objects.get_or_create(name=row[2])
        mt, created = Material.objects.get_or_create(name=row[0], unit = u, carbon_emission_factor = float(row[1]))

    for row in ereader:
        print(row)
        u, created = Unit.objects.get_or_create(name=row[4])
        e, created = Energy.objects.get_or_create(name=row[0], carbon_oxidation_rate = float(row[1]), carbon_per_carlorific = float(row[2]), carbon_emission_factor = float(row[3]), unit = u)

    for row in oereader:
        print(row)
        oe, created = OtherEnergy.objects.get_or_create(name=row[0], default_carbon_content = float(row[1]))

    for row in tpreader:
        print(row)
        u, created = Unit.objects.get_or_create(name=row[2])
        tp, created = Transportation.objects.get_or_create(name=row[0], volume = float(row[1]), carbon_emission_factor = float(row[3]), unit = u)

    for row in mcreader:
        print(row)
        m, created = Machine.objects.get_or_create(name=row[0], performance = row[1])
        e, created = Energy.objects.get_or_create(name=row[3])
        mp, created = MachinePerformance.objects.get_or_create(name=row[2], machine=m, energy = e, energy_volume = float(row[4]))

