from django.shortcuts import render
from django.views import View

# Create your views here.

from .models import Unit, Material, Energy, OtherEnergy, Transportation, Machine, MachinePerformance

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_materials = Material.objects.all().count()

    context = {
        'num_materials': num_materials,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class EstimatorView(View):

    def get(self, request):

        material_list = Material.objects.all()
        transportation_list = Transportation.objects.all()
        energy_list = Energy.objects.all()

        ctx = {'material_list': material_list, 'transportation_list': transportation_list, 'energy_list': energy_list}
        return render(request, 'estimator/estimator.html', ctx)

    def post(self, request):

        life = float(request.POST.get('life'))

        area = float(request.POST.get('area'))

        num_materials = Material.objects.all().count()

        num_energy = Energy.objects.all().count()

        material_cal=[]

        for i in range(1, num_materials+1):
            tmp_volume =  float(request.POST.get('volume_'+str(i)))
            if tmp_volume!=0:
                tmp_mtr = Material.objects.get(id=i)
                tmp_dict = {'id':i, 'name': tmp_mtr.name, 'factor': tmp_mtr.carbon_emission_factor, 'unit': tmp_mtr.unit, 'volume': tmp_volume}
                tmp_dict['trans_id'] = request.POST.get('trans_'+str(i))
                tmp_dict['trans_name'] = Transportation.objects.get(id=tmp_dict['trans_id']).name
                material_cal.append(tmp_dict)


        cons_energy_cal = []
        dml_energy_cal = []

        for i in range(1, num_energy+1):
            cons_volume =  float(request.POST.get('cons_volume_'+str(i)))
            dml_volume =  float(request.POST.get('dml_volume_'+str(i)))
            if cons_volume!=0 or dml_volume!=0:
                tmp_eng = Energy.objects.get(id=i)
                if cons_volume!=0:
                    tmp_cons_dict = {'id':i, 'name': tmp_eng.name, 'factor': tmp_eng.carbon_emission_factor, 'volume': cons_volume}
                    cons_energy_cal.append(tmp_cons_dict)
                if dml_volume!=0:
                    tmp_dml_dict = {'id':i, 'name': tmp_eng.name, 'factor': tmp_eng.carbon_emission_factor, 'volume': dml_volume}
                    dml_energy_cal.append(tmp_dml_dict)


        ctx =  {"total_emission" :355, "mlist": material_cal, "c_energy_list": cons_energy_cal, "d_energy_list": dml_energy_cal, "life": life, "area": area }

        return render(request, 'estimator/evaluate_result.html', ctx)

