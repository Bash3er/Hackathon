from simulation import Simulation
from utils import aggregate_species_by_depth, average_aggregations
from visualize import plot_four_configs, create_interactive_dashboard, EnhancedVisualizer
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
    configs = [50, 100, 500, 1000]
    avg_aggs = []

    for avg_agg in tqdm((get_avg_depth_aggs(n_runs, step=step, max_depth=max_depth) for n_runs in configs),
                        desc="Processing configurations", total=len(configs), unit="config", disable=True):
        avg_aggs.append(avg_agg[0])  # avg_agg returned is tuple (avg_agg, depths, species_types)

    print("Generating static analysis plots...")
    plot_four_configs(avg_aggs, avg_agg[1], avg_agg[2], configs)


def run_interactive_depth_explorer():
    """Run the interactive depth slider"""
    print("Launching interactive depth explorer...")
    try:
        from interactive_depth import run_interactive
        run_interactive()
    except ImportError:
        print("Interactive depth module not found. Please ensure interactive_depth.py is in the same folder.")
    except Exception as e:
        print(f"Error launching interactive depth explorer: {e}")

def run_enhanced_dashboard():
    """Run the enhanced real-time dashboard"""
    print("Creating enhanced ecosystem simulation...")
    print("This will run a simulation with real-time visualization...")
    
    try:
        # Create a longer simulation for the dashboard
        sim = Simulation(n_creatures=60, generations=50)
        
        # Create and launch the enhanced dashboard
        print("Launching enhanced dashboard...")
        dashboard = create_interactive_dashboard(sim)
        
        # Export species report after simulation
        print("Simulation completed. Exporting species report...")
        sim.export_species_report("final_species_report.txt")
        print("Species report saved to 'final_species_report.txt'")
        
        return dashboard
        
    except Exception as e:
        print(f"Error creating enhanced dashboard: {e}")
        print("Falling back to basic simulation...")
        
        # Fallback: run basic simulation and show final state
        sim = Simulation(n_creatures=50, generations=30)
        sim.run()
        
        visualizer = EnhancedVisualizer()
        visualizer.plot_detailed_species_evolution(sim, real_time=False)
        return sim

def run_single_simulation_analysis():
    """Run a single detailed simulation with analysis"""
    print("Running single detailed simulation...")
    
    sim = Simulation(n_creatures=80, generations=40)
    sim.run()
    
    print(f"Simulation completed with {len(sim.creatures)} creatures.")
    print(f"Survivors: {sum(1 for c in sim.creatures if c.alive)}")
    
    # Get species summary
    species_summary = sim.get_species_summary()
    print(f"Total species evolved: {len(species_summary)}")
    
    # Show top species
    if species_summary:
        print("\nTop 5 species by population:")
        sorted_species = sorted(species_summary.items(), key=lambda x: x[1]['count'], reverse=True)
        for i, (name, info) in enumerate(sorted_species[:5], 1):
            print(f"  {i}. {name}: {info['count']} individuals, avg fitness {info['avg_fitness']:.2f}")
    
    # Create visualization
    visualizer = EnhancedVisualizer()
    visualizer.plot_detailed_species_evolution(sim, real_time=False)
    
    # Export report
    visualizer.export_species_report(sim, f"simulation_report_{sim.generation_count}gen.txt")
    
    return sim

def main():
    print("=" * 60)
    print("          OCEAN ECOSYSTEM EVOLUTION SIMULATOR")
    print("               NASA Space Apps Challenge")
    print("=" * 60)
    print()
    print("Choose your analysis type:")
    print("1. Static Analysis (four comparison charts)")
    print("2. Interactive Depth Explorer (slider-based)")
    print("3. Enhanced Real-time Dashboard (advanced visualization)")
    print("4. Single Detailed Simulation (comprehensive analysis)")
    print("5. Run All Analyses")
    print()
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        print("\n" + "="*50)
        print("RUNNING STATIC ANALYSIS")
        print("="*50)
        run_static_analysis()
        
    elif choice == "2":
        print("\n" + "="*50)
        print("LAUNCHING INTERACTIVE DEPTH EXPLORER")
        print("="*50)
        run_interactive_depth_explorer()
        
    elif choice == "3":
        print("\n" + "="*50)
        print("LAUNCHING ENHANCED DASHBOARD")
        print("="*50)
        dashboard = run_enhanced_dashboard()
        
    elif choice == "4":
        print("\n" + "="*50)
        print("RUNNING SINGLE DETAILED SIMULATION")
        print("="*50)
        sim = run_single_simulation_analysis()
        
    elif choice == "5":
        print("\n" + "="*50)
        print("RUNNING ALL ANALYSES")
        print("="*50)
        
        # Run static analysis
        print("\n1/4: Static Analysis...")
        run_static_analysis()
        
        input("\nPress Enter to continue to Interactive Depth Explorer...")
        
        # Run interactive depth explorer
        print("\n2/4: Interactive Depth Explorer...")
        run_interactive_depth_explorer()
        
        input("\nPress Enter to continue to Enhanced Dashboard...")
        
        # Run enhanced dashboard
        print("\n3/4: Enhanced Dashboard...")
        dashboard = run_enhanced_dashboard()
        
        input("\nPress Enter to continue to Detailed Simulation...")
        
        # Run detailed simulation
        print("\n4/4: Detailed Simulation...")
        sim = run_single_simulation_analysis()
        
        print("\n" + "="*50)
        print("ALL ANALYSES COMPLETED!")
        print("Check the generated report files for detailed results.")
        print("="*50)
        
    else:
        print("Invalid choice. Running static analysis by default...")
        run_static_analysis()

def quick_test():
    """Quick test function for development"""
    print("Running quick test...")
    sim = Simulation(n_creatures=20, generations=10)
    sim.run()
    
    visualizer = EnhancedVisualizer()
    visualizer.plot_detailed_species_evolution(sim, real_time=False)
    
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
