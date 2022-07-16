from django.contrib import admin

# Register your models here.

from .models import Unit, Material, Energy, OtherEnergy, Transportation, Machine, MachinePerformance

admin.site.register(Unit)
admin.site.register(Material)
admin.site.register(Energy)
admin.site.register(OtherEnergy)
admin.site.register(Transportation)
admin.site.register(Machine)
admin.site.register(MachinePerformance)