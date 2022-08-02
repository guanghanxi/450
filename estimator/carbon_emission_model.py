def life_cycle_emission(
    material_cal,
    cons_energy_cal,
    opt_energy_cal,
    dml_energy_cal,
    life,
    area 
):
    result = 0
    c_p = 0
    for material in material_cal:
        result += (material['factor'] + 40*material['mass']*material['trans_factor'])* material['volume']
    for cons_energy in cons_energy_cal:
        result += cons_energy['factor'] * cons_energy['volume']
    for opt_energy in cons_energy_cal:
        result += cons_energy['factor'] * cons_energy['volume']*life
    for dml_energy in dml_energy_cal:
        result += dml_energy['factor'] * dml_energy['volume']
    result -= c_p
    return format(result/area, '.4f')