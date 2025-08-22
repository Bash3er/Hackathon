from simulation import Simulation
from utils import aggregate_species_by_depth, average_aggregations
from visualize import plot_four_configs, EnhancedVisualizer
from tqdm import tqdm

def get_avg_depth_aggs(n_runs, n_creatures=50, generations=30, max_depth=6000, step=50):
    depths = list(range(0, max_depth + 1, step))
    species_types = ["eyes", "bioluminescence", "plants", "no_eyes_animal"]
    all_aggs = []

    total_gens = n_runs * generations
    pbar = tqdm(total=total_gens, desc=f"{n_runs} generations", unit="gen")

    def progress_callback():
        pbar.update(1)

    for i in range(n_runs):
        sim = Simulation(n_creatures=n_creatures, generations=generations)
        sim.run(progress_callback=progress_callback)
        agg = aggregate_species_by_depth(sim.creatures, max_depth, step)
        all_aggs.append(agg)

    pbar.close()
    avg_agg = average_aggregations(all_aggs, depths, species_types)

    return avg_agg, depths, species_types

def run_static_analysis():
    print("Running static analysis with four different configurations...")

    step = 50
    max_depth = 6000
    # configs = [50, 100, 500, 1000]
    configs = [50, 100, 200, 300]
    avg_aggs = []

    for avg_agg in tqdm((get_avg_depth_aggs(n_runs, step=step, max_depth=max_depth) for n_runs in configs),
                        desc="Processing configurations", total=len(configs), unit="config", disable=True):
        avg_aggs.append(avg_agg[0])  # avg_agg returned is tuple (avg_agg, depths, species_types)

    print("Generating static analysis plots...")
    plot_four_configs(avg_aggs, avg_agg[1], avg_agg[2], configs)

def main():
    print("=" * 60)
    print("          OCEAN ECOSYSTEM EVOLUTION SIMULATOR")
    print("               NASA Space Apps Challenge")
    print("=" * 60)
    print()
    print("Static Analysis (four comparison charts)")
    print()
    
    print("\n" + "="*50)
    print("RUNNING STATIC ANALYSIS")
    print("="*50)
    run_static_analysis()

def quick_test():
    """Quick test function for development"""
    print("Running quick test...")
    sim = Simulation(n_creatures=20, generations=10)
    sim.run()
    
    visualizer = EnhancedVisualizer()
    visualizer.plot_detailed_species_evolution(sim)
    
    return sim

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Running quick test instead...")
        quick_test()
