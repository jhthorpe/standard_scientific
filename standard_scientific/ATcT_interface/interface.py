# HEAT.py
# 
#   JHT, September 18, 2025 @ ANL. Created
#
# Tests how to get reactions and/or atomization energies for species in the HEAT suite 
"""Testing how to use the ATcT pythonic API to gather reaction data used in comp. thermo"""

import asyncio
import os
import time
import copy
from atct import (
    get_species,
    calculate_reaction_enthalpy,
    get_species_covariance_by_atctid,
    get_species_covariance_matrix,
    create_reaction_calculator,
    healthcheck,
    search_species,
    get_species_by_smiles,
    get_species_by_casrn,
    get_species_by_formula,
    get_species_by_name,
    get_species_by_inchi,
    get_species_by_inchikey,
    get_species_covariance_by_atctid,
    get_species_covariance_matrix,
    as_dataframe
)
from atct import ReactionSpecies, ReactionResult

from species import Elements, Species
from HEAT_species import heat_species
from reaction import Reaction

# Converts kJ/mol to wavenumbers (inverse centimeters)
kJ2cm = 83.59347229110210

async def main():

    # 1. Health check
    print("1. Health Check:")
    if await healthcheck():
        print("   ✅ API is healthy")
    else:
        print("   ❌ API is not responding")
        return
    print()

    # Atom list, used everywhere
    atoms = ['H', 'C', 'N', 'O', 'F']

    ###################################################################################
    #
    # Generate general recovery tasks
    #
    print("Generating Species Recovery Tasks")

    species_tasks = {}
    for spec, data in heat_species.items():
        species_tasks[spec] = {'atct_data' : get_species(data.atct_id, expand_xyz=True)}

    print("Waiting on ATcT recovery data")
    species_atct = {}
    for spec, res in species_tasks.items():

        species_atct[spec] = await asyncio.gather(*res.values(), return_exceptions=True)

        #David trick to map species name to results data 
        species_atct[spec] = dict(zip(res.keys(), species_atct[spec]))

        #Now rip the DfH (0 K) from data
        heat_species[spec].dfh0k = species_atct[spec]['atct_data'].delta_h_0k

    print("After getting species data from atct...")
    for key,val in heat_species.items():
        print(val)

    ###################################################################################
    # 
    # Generate TAE tasks
    #

    tae_refs = {'H' :'H', 'C':'C', 'N':'N', 'O':'O', 'F':'F'}
    tae_species = copy.deepcopy(heat_species) 
    for atom,ref in tae_refs.items():
        tae_species.pop(ref)

    print("Generating TAE tasks")
    tae_tasks = {}
    tae_rxns = {}
    for spec, data in tae_species.items():

        species = heat_species[spec]
        rxn = Reaction(name = spec)

        rxn.stoich[spec] = -1
        for atom,num in species.elements.items():
            rxn.stoich[atom] = num

        tae_rxns[spec] = rxn
        tae_tasks[spec] = rxn.atct_0K_query(heat_species)

    print("Processing TAE tasks")
    tae_res = {}
    for spec, task in tae_tasks.items():
        tae_res[spec] = await asyncio.gather(task['covariance_298K'], task['conventional_0K'], return_exceptions=True)
        tae_rxns[spec].value = tae_res[spec][1].delta_h
        tae_rxns[spec].unc = tae_res[spec][0].uncertainty

#    for name,rxn in tae_rxns.items():
#        print(rxn)
    for name, rxn in tae_rxns.items():
        print(f"TAE of {name:4} : {rxn.value * kJ2cm:.3f} +- {rxn.unc * kJ2cm:.6f}")
#    for spec, data in tae.items():
#        print(f"TAE of {spec:4} : {data['DfH(0K)']*kJ2cm:.3f} +- {data['unc(298K)']*kJ2cm:.6f}")







    
'''
    ###################################################################################
    #
    # Generate TAE reaction tasks 
    #
    #
    tae_species = copy.deepcopy(species)
    for atom in ['H', 'C', 'N', 'O', 'F']:
        tae_species.pop(atom)

    tae_ref = {} 
    for atom in ['H', 'C', 'N', 'O', 'F']:
        tae_species[atom] = species[atom]

    print("Generating TAE tasks")
    tae_tasks = {}
    for spec, data in tae_species.items():
        tae_dict = {data['id'] : -1}
        for atom, num in data['atoms'].items():
            if (num > 0):
                tae_dict[species[atom]['id']] = num
        tae_tasks[spec] = {
            'covariance_298K': calculate_reaction_enthalpy(tae_dict, 'covariance', use_0k = False),
            'conventional_0K': calculate_reaction_enthalpy(tae_dict, 'conventional', use_0k = True)
        }

    print("Awaiting TAE tasks")
    tae = {}
    tae_res = {}
    for spec, task in tae_tasks.items():
        tae_res[spec] = await asyncio.gather(task['covariance_298K'], task['conventional_0K'], return_exceptions=True)
        tae[spec] = {
                'DfH(0K)' : tae_res[spec][1].delta_h,
                'unc(298K)' : tae_res[spec][0].uncertainty
                }

    for spec, data in tae.items():
        print(f"TAE of {spec:4} : {data['DfH(0K)']*kJ2cm:.3f} +- {data['unc(298K)']*kJ2cm:.6f}")

    ###################################################################################
    #
    # Generate ANL scheme reaction tasks 
    #
    # General molecule: HhCcNnOoFf -> (4*c + 3*n + 2*o + 1*f + 2*h)*H2 + c*CH4 + n*NH3 + o*H2O + f*HF 
    #
    # In this case, we will accept fractional H2 values, so that the species of interest always
    # has a factor of 1 in front of it, in keeping with TAE 
    #
    print("Generating ANL tasks")
    anl_tasks = {}

    #elements and their reference species
    anl_ref = {'H' : 'H2', 'C' : 'CH4', 'N' : 'NH3', 'O': 'H2O', 'F' : 'HF'}

    # anl species from all species but without references
    anl_species = [key for key in species]
    for atom, ref in anl_ref.items():
        anl_species.pop(ref)

    # generate task list and reactions list
    #
    # reactions list
    # 
    # key is species name that drives the reaction
    # value is a dict:
    #
    # 
    #
    anl_tasks = {}
    anl_rxns = {}
    for spec in anl_species:

        data = species[spec]

        #ATcT interface task needs dictionary of ATcT IDs with stoich.
        atct_dict = {data['id'] : -1} 
        anl_rxns[spec] = { spec : -1} 
        
        nh = 0
        for atom,num in data['atoms'].items():
            if (num > 0):
                ref_key = anl_ref[atom]
                ref_id = species[ref_key]['id']
                atct_dict[ref_id] = num 
                atct_reactions[ref_key] = num
                nh += num * species[ref_key]['atoms']['H']
        atct_dict[species["H2"]['id'] = nh * 0.5
        atct_reactions[spec]['H2'] = nh * 0.5 
        
        anl_tasks[spec] = {
            'covariance_298K': calculate_reaction_enthalpy(atct_dict, 'covariance', use_0k = False),
            'conventional_0K': calculate_reaction_enthalpy(atct_dict, 'conventional', use_0k = True)
        }

    for rxn,  in anl_rxn
    '''

    ###################################################################################
    #
    # Await tasks
    #

    

if __name__== "__main__":
    asyncio.run(main())

