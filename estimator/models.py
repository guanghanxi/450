from django.db import models

# Create your models here.

from django.urls import reverse


class Unit(models.Model):

    name = models.CharField(max_length=15)


    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Material(models.Model):

    name = models.CharField(max_length=255)

    unit = models.ForeignKey('Unit', on_delete=models.RESTRICT, null=True)

    carbon_emission_factor = models.FloatField()

    equivalent_mass = models.FloatField()

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Energy(models.Model):

    name = models.CharField(max_length=200)

    unit = models.ForeignKey('Unit', on_delete=models.RESTRICT, null=True)

    carbon_emission_factor = models.FloatField()

    carbon_oxidation_rate = models.FloatField()

    carbon_per_carlorific = models.FloatField()

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class OtherEnergy(models.Model):

    name = models.CharField(max_length=200)

    default_carbon_content = models.FloatField()

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Transportation(models.Model):

    name = models.CharField(max_length=200)

    volume = models.FloatField()

    unit = models.ForeignKey('Unit', on_delete=models.RESTRICT, null=True)

    carbon_emission_factor = models.FloatField()

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Machine(models.Model):

    name = models.CharField(max_length=200)

    performance = models.CharField(max_length=63)


    def __str__(self):
        """String for representing the Model object."""
        return self.name


class MachinePerformance(models.Model):

    name = models.CharField(max_length=200)

    machine = models.ForeignKey('Machine', on_delete=models.RESTRICT, null=True)

    energy = models.ForeignKey('Energy', on_delete=models.RESTRICT, null=True)

    energy_volume = models.FloatField()

    def __str__(self):
        """String for representing the Model object."""
        return self.name