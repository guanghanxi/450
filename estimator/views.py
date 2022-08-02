from django.shortcuts import render
from django.views import View

# import life-cycle carbon emission estimation model

from .carbon_emission_model import life_cycle_emission

# Create your views here.

from .models import Unit, Material, Energy, OtherEnergy, Transportation, Machine, MachinePerformance

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_materials = Material.objects.all().count()

    context = {
        'num_materials': num_materials,
        'num_trans':  Transportation.objects.all().count(),
        'num_energy':  Energy.objects.all().count() + OtherEnergy.objects.all().count(),
        'num_machine':  Machine.objects.all().count(),
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

        # print(request.POST)

        material_cal=[]
        i=1
        material_id_set=set()

        while True:
            if i==1:
                field_name = 'material'
            else:
                field_name = 'material-' + str(i)
            tmp_id =  request.POST.get('id-' + field_name, default=False)
            if tmp_id:
                if tmp_id not in material_id_set:
                    tmp_volume =  float(request.POST.get('volume-' + field_name))
                    material_id_set.add(tmp_id)
                    if  tmp_volume!=0:
                        index = int(tmp_id)
                        tmp_mtr = Material.objects.get(id=index)
                        tmp_dict = {'id':index, 'name': tmp_mtr.name, 'factor': tmp_mtr.carbon_emission_factor, 'mass': tmp_mtr.equivalent_mass, 'volume': tmp_volume}
                        tmp_dict['trans_id'] = request.POST.get('trans-'+ field_name)
                        tmp_trans = Transportation.objects.get(id=tmp_dict['trans_id'])
                        tmp_dict['trans_name'] = tmp_trans.name
                        tmp_dict['trans_factor'] = tmp_trans.carbon_emission_factor
                        material_cal.append(tmp_dict)
                i+=1
            else:
                break

        cons_energy_cal = []
        dml_energy_cal = []
        opt_energy_cal = []
        energy_id_set=set()
        i=1

        while True:
            if i==1:
                field_name = 'energy'
            else:
                field_name = 'energy-' + str(i)
            tmp_id =  request.POST.get('id-'+ field_name, default=False)
            if tmp_id:
                if tmp_id not in energy_id_set:
                    index = int(tmp_id)
                    tmp_eng = Energy.objects.get(id=index)
                    cons_volume =  float(request.POST.get('volume-cons-'+field_name))
                    opt_volume =  float(request.POST.get('volume-opt-'+field_name))
                    dml_volume =  float(request.POST.get('volume-dml-'+field_name))
                    energy_id_set.add(tmp_id)
                    if cons_volume!=0:
                        tmp_cons_dict = {'id':index, 'name': tmp_eng.name, 'factor': tmp_eng.carbon_emission_factor, 'volume': cons_volume}
                        cons_energy_cal.append(tmp_cons_dict)
                    if opt_volume!=0:
                        tmp_opt_dict = {'id':index, 'name': tmp_eng.name, 'factor': tmp_eng.carbon_emission_factor, 'volume': opt_volume}
                        opt_energy_cal.append(tmp_opt_dict)
                    if dml_volume!=0:
                        tmp_dml_dict = {'id':index, 'name': tmp_eng.name, 'factor': tmp_eng.carbon_emission_factor, 'volume': dml_volume}
                        dml_energy_cal.append(tmp_dml_dict)
                i+=1
            else:
                break

        t_emission = life_cycle_emission(material_cal, cons_energy_cal, opt_energy_cal, dml_energy_cal, life, area )

        ctx =  {"total_emission" :t_emission, "mlist": material_cal, "c_energy_list": cons_energy_cal, "o_energy_list": opt_energy_cal, "d_energy_list": dml_energy_cal, "life": life, "area": area }

        return render(request, 'estimator/evaluate_result.html', ctx)

from django.views import generic

from django.db.models import Q

class MaterialListView(generic.ListView):
    model = Material
    paginate_by = 20
    template_name = "estimator/material_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(name__icontains=strval)
            material_list = Material.objects.filter(query).select_related().distinct()
        else :
            material_list = Material.objects.all()
        ctx = {'material_list' : material_list}
        if strval:
            ctx['search'] = strval
        return render(request, self.template_name, ctx)

class TransportationListView(generic.ListView):
    model = Transportation
    paginate_by = 30
    template_name = "estimator/transportation_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(name__icontains=strval)
            transportation_list = Transportation.objects.filter(query).select_related().distinct()
        else :
            transportation_list = Transportation.objects.all()
        ctx = {'transportation_list' : transportation_list}
        if strval:
            ctx['search'] = strval
        return render(request, self.template_name, ctx)

class EnergyListView(View):

    def get(self, request):

        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(name__icontains=strval)
            other_e_list = OtherEnergy.objects.filter(query).select_related().distinct()
            energy_list = Energy.objects.filter(query).select_related().distinct()
        else :
            other_e_list = OtherEnergy.objects.all()
            energy_list = Energy.objects.all()

        ctx = {'other_e_list': other_e_list , 'energy_list': energy_list }

        if strval:
            ctx['search'] = strval

        return render(request, 'estimator/energy_list.html', ctx)

class MachineListView(generic.ListView):
    model = Machine
    paginate_by = 20
    template_name = "estimator/machine_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(name__icontains=strval)
            machine_list = Machine.objects.filter(query).select_related().distinct()
        else :
            machine_list = Machine.objects.all()
        ctx = {'machine_list' : machine_list}
        if strval:
            ctx['search'] = strval
        return render(request, self.template_name, ctx)


class MachineDetailView(generic.ListView):

    def get(self, request, pk):

        machines = Machine.objects.get(id=pk)

        mp_list = MachinePerformance.objects.filter(machine = pk)
        new_mp_list = []
        for mp in mp_list:
            tmp={}
            tmp['energy'] = mp.energy
            tmp['name'] = mp.name
            tmp['energy_volume'] = mp.energy_volume
            tmp["energy_unit"] = mp.energy.unit
            new_mp_list.append(tmp)

        ctx = {'machine': machines.name , 'performance': machines.performance, 'mp_list': new_mp_list}
        return render(request, 'estimator/machine_detail.html', ctx)

# Real Time Test
