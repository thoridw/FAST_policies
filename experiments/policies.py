# -*- coding: utf-8 -*-
"""
@author: thoridwagenblast
"""

from src.model import AdaptationModel
import pandas as pd
import numpy as np
from mesa.batchrunner import batch_run

def q1(x):
    return x.quantile(0.25)

def q3(x):
    return x.quantile(0.75)

if __name__ == '__main__':
    parameter_sweep = {'seed': range(12345, 12345+50),
                       'nr_households': [1000],
                       'set_hh_adapted_at_start': [False, 0.3, 0.6],
                       'prop_inc_for_damage_adaptation': [0.05], 
                       'exchange_what': ['threat+coping'], #'threat' or 'coping'
                       'social_norm_calculation': ['all'], #'connections', # 'district', 'all'
                       'per_HH_adapted_to_SN_prob_midpoint': [0.5],
                       'weight_SN_vs_PMT': ['empirical'], #'empirical'
                       
                       'opinion_dynamics_model': ['similarity_biased'], #'assimilative'
                       'weight_opinion_others': [0.5],
                       'threshold_similarity_bias': [0.2],# , 0.5, 0.7],
                       
                       # Grid related
                       # grid_width = 5,
                       # grid_height = 5,
                       'flood_depth_in_m': [[99, 1, 1, 1, 1]], # same length as grid_height, first 99 (water)
                       'flood_time':  [[99],
                                       [10],
                                       [10, 25, 35, 42]],
                       'population_density': [[[0,50,50,50,50],
                                             [0,50,50,50,50],
                                             [0,50,50,50,50],
                                             [0,50,50,50,50],
                                             [0,50,50,50,50]]],

                       'network_structure_file_path': ['../data/processed/network_structures/network_empirical.graphml'],
                       
                       # fraction_neighbors = 0.15,
                       # fraction_homophily = 0.25,
                       # fraction_family_and_friends = 0.55,
                       'proportion_ties_added_per_step': [0], # no network evolution
                       'proportion_ties_removed_per_step': [0], # no network evolution
                       'fraction_ties_added_at_flood': [0], # no network evolution
                       'flood_remembrance_period': [5], # how long the experience of flood leads to more connection in the network

                       'consider_measure_every_x_steps': [1],
                       'minimum_intention_to_consider_measure': [0.05], #, 0.5, 0.7],
                       'worry_increase_with_flood': [0.3],
                       'min_worry_after_flood': [0.1],
                       
                       
                       # flood damage related: from Huizinga, de Moel --> damage factor
                       # in dollar and adjusted for inflation to 2020 value
                       # max_damage_per_sqm = 950,
                       # CCA_costs = {'dry-proofing': 10300, 
                       #              'wet-proofing': 8000},
                       'damage_reduction': [{'dry-proofing': 0.5, 'wet-proofing': 0.4}],
                       'measures_aging': [{'dry-proofing': 20, # 0 if no aging, int for number of years they age
                                    'wet-proofing': 20}],
                        'policies_file_path': ['../data/policies/policies_innovation_high.json',
                                               '../data/policies/policies_innovation_mid.json',
                                               '../data/policies/policies_subsidies_high.json',
                                               '../data/policies/policies_subsidies_mid.json',
                                               '../data/policies/policies_subsidies_low.json',
                                               '../data/policies/policies_comm_high.json',
                                               '../data/policies/policies_comm_mid.json',
                                               '../data/policies/policies_comm_low.json',
                                               '../data/policies/policies_comm_high_cope.json',
                                               '../data/policies/policies_comm_high_norm.json',
                                               '../data/policies/policies_comm_high_threat.json',
                                               '../data/policies/policies_comm_low_cope.json',
                                               '../data/policies/policies_comm_low_norm.json',
                                               '../data/policies/policies_comm_low_threat.json',
                                               '../data/policies/policies_comm_mid_cope.json',
                                               '../data/policies/policies_comm_mid_norm.json',
                                               '../data/policies/policies_comm_mid_threat.json'],
                        'policy_activation': [[11]],
                        # 'transformative_threshold': [0.7],
                        'collect_agent_data': [0]
                       }
    
    num_iterations = 1
    steps = 50
    
    results = batch_run(AdaptationModel,
                        number_processes=None,
                        parameters=parameter_sweep,
                        display_progress=True,
                        iterations = num_iterations,
                        max_steps=steps,
                        data_collection_period=1)
    
    results_df = pd.DataFrame(results)
    
    results_df['flood_time'] = results_df['flood_time'].astype(str)
    results_df['flood_depth_in_m'] = results_df['flood_depth_in_m'].astype(str)
    results_df['measures_aging'] =  results_df['measures_aging'].astype(str)
    results_df['damage_reduction'] = results_df['damage_reduction'].astype(str)
    
    results_df = results_df.drop(columns = ['RunId', 'iteration'])
    # results_df = results_df.drop_duplicates(ignore_index = True)
    
    results_df.to_csv('../results/policies.csv')
    





 