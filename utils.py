from collections import defaultdict
import numpy as np

def aggregate_species_by_depth(creatures, max_depth=6000, step=50):
    agg = defaultdict(lambda: defaultdict(int))
    for c in creatures:
        if not c.alive:
            continue

        depth_key = int(step * round(float(c.depth) / step))
        vision = c.traits['vision']

        if vision == 'eyes':
            agg[depth_key]['eyes'] += 1
        elif vision == 'bioluminescence':
            agg[depth_key]['bioluminescence'] += 1
        elif vision == 'no_eyes':
            if c.traits['food_strategy'] == 'photosynthesis':
                agg[depth_key]['plants'] += 1
            else:
                agg[depth_key]['no_eyes_animal'] += 1
        elif vision == 'echolocation':
            agg[depth_key]['echolocation'] += 1
        elif vision == 'lateral_line':
            agg[depth_key]['lateral_line'] += 1
        elif vision == 'compound_eyes':
            agg[depth_key]['compound_eyes'] += 1
    return agg

def average_aggregations(all_aggs, depths, species):
    avg = defaultdict(lambda: defaultdict(float))
    runs = len(all_aggs)
    for agg in all_aggs:
        for d in depths:
            for s in species:
                avg[d][s] += agg[d][s]

    for d in depths:
        for s in species:
            avg[d][s] /= runs

    return avg
