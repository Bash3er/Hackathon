from collections import defaultdict
import numpy as np
import json

def aggregate_species_by_depth(creatures, max_depth=6000, step=50):
    """Enhanced aggregation supporting all new creature traits"""
    agg = defaultdict(lambda: defaultdict(int))
    
    for c in creatures:
        depth = int(step * round(float(c.depth)/step))
        
        # Vision-based classification (backward compatible)
        if c.traits["vision"] == "eyes":
            agg[depth]["eyes"] += 1
        elif c.traits["vision"] == "bioluminescence":
            agg[depth]["bioluminescence"] += 1
        elif c.traits["vision"] == "no_eyes":
            if c.traits["food_strategy"] == "photosynthesis":
                agg[depth]["plants"] += 1
            else:
                agg[depth]["no_eyes_animal"] += 1
        # New vision types
        elif c.traits["vision"] == "echolocation":
            agg[depth]["echolocation"] += 1
        elif c.traits["vision"] == "lateral_line":
            agg[depth]["lateral_line"] += 1
        elif c.traits["vision"] == "compound_eyes":
            agg[depth]["compound_eyes"] += 1
    
    return agg

def aggregate_by_trait_combination(creatures, trait1, trait2, max_depth=6000, step=50):
    """Aggregate creatures by any two trait combinations"""
    agg = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    for c in creatures:
        if c.alive:
            depth = int(step * round(float(c.depth)/step))
            trait1_val = c.traits.get(trait1, "unknown")
            trait2_val = c.traits.get(trait2, "unknown")
            agg[depth][trait1_val][trait2_val] += 1
    
    return agg

def aggregate_by_feeding_strategy(creatures, max_depth=6000, step=50):
    """Aggregate creatures by feeding strategy"""
    agg = defaultdict(lambda: defaultdict(int))
    
    for c in creatures:
        if c.alive:
            depth = int(step * round(float(c.depth)/step))
            feeding = c.traits["food_strategy"]
            agg[depth][feeding] += 1
    
    return agg

def aggregate_by_body_type(creatures, max_depth=6000, step=50):
    """Aggregate creatures by body type and locomotion"""
    agg = defaultdict(lambda: defaultdict(int))
    
    for c in creatures:
        if c.alive:
            depth = int(step * round(float(c.depth)/step))
            body_type = c.traits["body_type"]
            locomotion = c.traits["locomotion"]
            key = f"{body_type}_{locomotion}"
            agg[depth][key] += 1
    
    return agg

def aggregate_by_size_class(creatures, max_depth=6000, step=50):
    """Aggregate creatures by size class"""
    agg = defaultdict(lambda: defaultdict(int))
    
    for c in creatures:
        if c.alive:
            depth = int(step * round(float(c.depth)/step))
            size = c.traits["size"]
            agg[depth][size] += 1
    
    return agg

def average_depth_aggs(all_aggs, depths, species_types):
    """Calculate average aggregations across multiple runs"""
    avg_agg = defaultdict(lambda: defaultdict(float))
    total_runs = len(all_aggs)
    
    for agg in all_aggs:
        for d in depths:
            for sp in species_types:
                avg_agg[d][sp] += agg[d][sp]
    
    for d in depths:
        for sp in species_types:
            avg_agg[d][sp] /= total_runs
    
    return avg_agg

def calculate_diversity_metrics(creatures, depth_bins=10):
    """Calculate biodiversity metrics at different depths"""
    max_depth = max(c.depth for c in creatures if c.alive) if creatures else 6000
    bin_size = max_depth / depth_bins
    
    diversity_data = defaultdict(lambda: {
        'species_count': 0,
        'shannon_diversity': 0,
        'simpson_diversity': 0,
        'evenness': 0,
        'total_individuals': 0
    })
    
    # Group creatures by depth bins
    depth_groups = defaultdict(list)
    for c in creatures:
        if c.alive:
            bin_index = int(c.depth / bin_size)
            depth_groups[bin_index].append(c)
    
    # Calculate diversity metrics for each depth bin
    for bin_index, group in depth_groups.items():
        depth = bin_index * bin_size
        
        # Count species (using species names)
        species_counts = defaultdict(int)
        for c in group:
            species_counts[c.species_name] += 1
        
        total_individuals = len(group)
        num_species = len(species_counts)
        
        # Shannon diversity index
        shannon = 0
        for count in species_counts.values():
            if count > 0:
                p = count / total_individuals
                shannon -= p * np.log(p)
        
        # Simpson diversity index
        simpson = 0
        for count in species_counts.values():
            p = count / total_individuals
            simpson += p * p
        simpson = 1 - simpson
        
        # Evenness (Pielou's evenness)
        evenness = shannon / np.log(num_species) if num_species > 1 else 0
        
        diversity_data[depth] = {
            'species_count': num_species,
            'shannon_diversity': shannon,
            'simpson_diversity': simpson,
            'evenness': evenness,
            'total_individuals': total_individuals
        }
    
    return diversity_data

def analyze_trait_correlations(creatures):
    """Analyze correlations between different traits"""
    if not creatures:
        return {}
    
    # Extract numerical traits
    trait_data = defaultdict(list)
    for c in creatures:
        if c.alive:
            trait_data['depth'].append(c.depth)
            trait_data['fitness'].append(c.fitness)
            trait_data['metabolic_rate'].append(c.traits['metabolic_rate'])
            trait_data['oxygen_efficiency'].append(c.traits['oxygen_efficiency'])
            trait_data['pressure_tolerance'].append(c.traits['pressure_tolerance'])
            trait_data['light_production'].append(c.traits['light_production'])
            trait_data['move_eff'].append(c.traits['move_eff'])
            trait_data['repro_rate'].append(c.traits['repro_rate'])
    
    # Calculate correlations
    correlations = {}
    traits = list(trait_data.keys())
    
    for i, trait1 in enumerate(traits):
        for trait2 in traits[i+1:]:
            if len(trait_data[trait1]) > 1 and len(trait_data[trait2]) > 1:
                corr = np.corrcoef(trait_data[trait1], trait_data[trait2])[0, 1]
                correlations[f"{trait1}_vs_{trait2}"] = corr if not np.isnan(corr) else 0
    
    return correlations

def get_depth_zones_summary(creatures):
    """Get summary statistics for each ocean depth zone"""
    zones = {
        'Surface (0-100m)': (0, 100),
        'Mid-depth (100-1000m)': (100, 1000),
        'Deep Sea (1000-4000m)': (1000, 4000),
        'Abyss (4000-6000m)': (4000, 6000)
    }
    
    zone_summary = {}
    
    for zone_name, (min_depth, max_depth) in zones.items():
        zone_creatures = [c for c in creatures 
                         if c.alive and min_depth <= c.depth < max_depth]
        
        if zone_creatures:
            # Basic stats
            total_count = len(zone_creatures)
            avg_fitness = np.mean([c.fitness for c in zone_creatures])
            
            # Most common traits
            vision_counts = defaultdict(int)
            feeding_counts = defaultdict(int)
            body_counts = defaultdict(int)
            
            for c in zone_creatures:
                vision_counts[c.traits['vision']] += 1
                feeding_counts[c.traits['food_strategy']] += 1
                body_counts[c.traits['body_type']] += 1
            
            # Species diversity
            species_counts = defaultdict(int)
            for c in zone_creatures:
                species_counts[c.species_name] += 1
            
            zone_summary[zone_name] = {
                'total_creatures': total_count,
                'average_fitness': avg_fitness,
                'species_diversity': len(species_counts),
                'most_common_vision': max(vision_counts.items(), key=lambda x: x[1])[0] if vision_counts else 'None',
                'most_common_feeding': max(feeding_counts.items(), key=lambda x: x[1]) if feeding_counts else 'None',
                'most_common_body': max(body_counts.items(), key=lambda x: x[1]) if body_counts else 'None',
                'depth_range': f"{min_depth}-{max_depth}m"
            }
        else:
            zone_summary[zone_name] = {
                'total_creatures': 0,
                'average_fitness': 0,
                'species_diversity': 0,
                'most_common_vision': 'None',
                'most_common_feeding': 'None',
                'most_common_body': 'None',
                'depth_range': f"{min_depth}-{max_depth}m"
            }
    
    return zone_summary

def export_simulation_data(creatures, filename="simulation_data.json"):
    """Export detailed simulation data to JSON"""
    export_data = {
        'metadata': {
            'total_creatures': len(creatures),
            'living_creatures': sum(1 for c in creatures if c.alive),
            'generation_timestamp': str(np.datetime64('now'))
        },
        'creatures': [],
        'zone_summary': get_depth_zones_summary(creatures),
        'diversity_metrics': calculate_diversity_metrics(creatures),
        'trait_correlations': analyze_trait_correlations(creatures)
    }
    
    # Export creature data
    for i, c in enumerate(creatures):
        if c.alive:
            creature_data = {
                'id': i,
                'species_name': c.species_name,
                'depth': c.depth,
                'fitness': c.fitness,
                'traits': dict(c.traits),
                'age': getattr(c, 'age', 0),
                'energy': getattr(c, 'energy', 100)
            }
            export_data['creatures'].append(creature_data)
    
    # Save to file
    try:
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        print(f"Simulation data exported to {filename}")
    except Exception as e:
        print(f"Error exporting data: {e}")

def calculate_ecosystem_stability(species_log):
    """Calculate ecosystem stability metrics over time"""
    if not species_log:
        return {}
    
    # Extract time series data
    generations = [entry['generation'] for entry in species_log]
    species_counts = [entry['total_species'] for entry in species_log]
    
    # Calculate stability metrics
    stability_metrics = {
        'species_count_variance': np.var(species_counts) if len(species_counts) > 1 else 0,
        'species_count_trend': np.polyfit(generations, species_counts, 1)[0] if len(generations) > 1 else 0,
        'final_diversity': species_counts[-1] if species_counts else 0,
        'peak_diversity': max(species_counts) if species_counts else 0,
        'diversity_stability_ratio': (min(species_counts) / max(species_counts)) if species_counts and max(species_counts) > 0 else 0
    }
    
    return stability_metrics

def filter_creatures_by_traits(creatures, **trait_filters):
    """Filter creatures by specific trait values"""
    filtered = []
    
    for c in creatures:
        if c.alive:
            match = True
            for trait_name, trait_value in trait_filters.items():
                if trait_name in c.traits:
                    if isinstance(trait_value, list):
                        if c.traits[trait_name] not in trait_value:
                            match = False
                            break
                    else:
                        if c.traits[trait_name] != trait_value:
                            match = False
                            break
                else:
                    match = False
                    break
            
            if match:
                filtered.append(c)
    
    return filtered

def generate_ecosystem_report(creatures, species_log=None):
    """Generate a comprehensive ecosystem analysis report"""
    report = {
        'summary': {
            'total_creatures': len(creatures),
            'living_creatures': sum(1 for c in creatures if c.alive),
            'average_fitness': np.mean([c.fitness for c in creatures if c.alive]) if creatures else 0,
            'depth_range': f"{min(c.depth for c in creatures if c.alive):.0f}-{max(c.depth for c in creatures if c.alive):.0f}m" if creatures else "0-0m"
        },
        'zone_analysis': get_depth_zones_summary(creatures),
        'diversity_metrics': calculate_diversity_metrics(creatures),
        'trait_correlations': analyze_trait_correlations(creatures)
    }
    
    if species_log:
        report['ecosystem_stability'] = calculate_ecosystem_stability(species_log)
    
    return report

def print_ecosystem_summary(creatures):
    """Print a quick ecosystem summary to console"""
    living_creatures = [c for c in creatures if c.alive]
    
    if not living_creatures:
        print("No living creatures in the ecosystem.")
        return
    
    print("\n" + "="*50)
    print("ECOSYSTEM SUMMARY")
    print("="*50)
    
    # Basic stats
    print(f"Total living creatures: {len(living_creatures)}")
    print(f"Average fitness: {np.mean([c.fitness for c in living_creatures]):.2f}")
    print(f"Depth range: {min(c.depth for c in living_creatures):.0f}-{max(c.depth for c in living_creatures):.0f}m")
    
    # Species diversity
    species_counts = defaultdict(int)
    for c in living_creatures:
        species_counts[c.species_name] += 1
    
    print(f"Total species: {len(species_counts)}")
    
    # Top 5 species
    if species_counts:
        print("\nTop 5 species by population:")
        sorted_species = sorted(species_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (species, count) in enumerate(sorted_species, 1):
            print(f"  {i}. {species}: {count} individuals")
    
    # Zone distribution
    zone_summary = get_depth_zones_summary(creatures)
    print("\nDepth zone distribution:")
    for zone_name, data in zone_summary.items():
        print(f"  {zone_name}: {data['total_creatures']} creatures")
    
    print("="*50)
