import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button, CheckButtons
import numpy as np
from collections import defaultdict
import pandas as pd

class EnhancedVisualizer:
    def __init__(self):
        self.fig = None
        self.axes = None
        self.animation = None
        self.data_history = []
        self.is_playing = False
        
    def plot_detailed_species_evolution(self, simulation, real_time=False):
        """Enhanced species evolution plot with real-time capability"""
        if real_time:
            self._setup_realtime_plot(simulation)
        else:
            self._plot_final_species_state(simulation)
    
    def _setup_realtime_plot(self, simulation):
        """Setup real-time plotting with controls"""
        # Fix: Handle different seaborn versions
        try:
            plt.style.use('seaborn-v0_8')
        except OSError:
            try:
                plt.style.use('seaborn')
            except OSError:
                plt.style.use('default')
        
        self.fig = plt.figure(figsize=(20, 12))
        
        # Create subplots with proper spacing
        gs = self.fig.add_gridspec(3, 4, height_ratios=[2, 1, 1], width_ratios=[2, 2, 1, 1],
                                   hspace=0.3, wspace=0.3)
        
        # Main evolution plot
        self.ax_main = self.fig.add_subplot(gs[0, :2])
        
        # Species diversity plot
        self.ax_diversity = self.fig.add_subplot(gs[0, 2])
        
        # Fitness distribution
        self.ax_fitness = self.fig.add_subplot(gs[0, 3])
        
        # Trait distribution heatmaps
        self.ax_traits = self.fig.add_subplot(gs[1, :2])
        
        # Population stats
        self.ax_pop = self.fig.add_subplot(gs[1, 2:])
        
        # Environmental zones
        self.ax_zones = self.fig.add_subplot(gs[2, :])
        
        # Add controls with error handling
        try:
            self._add_interactive_controls()
        except Exception as e:
            print(f"Warning: Could not add interactive controls: {e}")
        
        # Set initial playing state
        self.is_playing = True
        
        # Start animation
        self.animation = animation.FuncAnimation(
            self.fig, self._update_realtime_plot, frames=simulation.generations,
            interval=1000, repeat=True, fargs=(simulation,)
        )
        
        plt.tight_layout()
        plt.show()
    
    def _add_interactive_controls(self):
        """Add interactive controls for real-time visualization"""
        try:
            # Play/Pause button
            ax_button = plt.axes([0.85, 0.02, 0.1, 0.04])
            self.button = Button(ax_button, 'Play/Pause')
            self.button.on_clicked(self._toggle_animation)
            
            # Speed slider
            ax_speed = plt.axes([0.2, 0.02, 0.3, 0.03])
            self.speed_slider = Slider(ax_speed, 'Speed', 0.1, 3.0, valinit=1.0)
            
            # Species filter checkboxes
            ax_check = plt.axes([0.02, 0.7, 0.15, 0.25])
            species_labels = ['Photosynthetic', 'Bioluminescent', 'Eyes', 'No Eyes', 
                             'Echolocation', 'Filter Feeders', 'Predators', 'Chemosynthetic']
            self.species_check = CheckButtons(ax_check, species_labels, 
                                            [True] * len(species_labels))
        except Exception as e:
            print(f"Could not create interactive controls: {e}")
    
    def _update_realtime_plot(self, frame, simulation):
        """Update all plots in real-time"""
        if not self.is_playing:
            return
            
        # Clear all axes
        for ax in [self.ax_main, self.ax_diversity, self.ax_fitness, 
                  self.ax_traits, self.ax_pop, self.ax_zones]:
            ax.clear()
        
        # Get current generation data safely
        if hasattr(simulation, 'species_log') and simulation.species_log:
            current_gen = min(frame, len(simulation.species_log) - 1)
            if current_gen < 0:
                return
            gen_data = simulation.species_log[current_gen]
        else:
            gen_data = {'generation': frame, 'species': {}, 'total_species': 0}
            current_gen = frame
        
        # Main evolution plot - species by depth
        self._plot_species_depth_scatter(simulation.creatures, self.ax_main)
        
        # Species diversity over time
        if hasattr(simulation, 'species_log') and simulation.species_log:
            self._plot_species_diversity_timeline(simulation.species_log[:current_gen+1], self.ax_diversity)
        
        # Fitness distribution
        self._plot_fitness_histogram(simulation.creatures, self.ax_fitness)
        
        # Trait distribution heatmap
        self._plot_trait_heatmap(simulation.creatures, self.ax_traits)
        
        # Population statistics
        self._plot_population_stats(gen_data, self.ax_pop)
        
        # Environmental zones with species
        self._plot_environmental_zones(simulation.creatures, self.ax_zones)
        
        self.fig.suptitle(f'Ocean Ecosystem Evolution - Generation {current_gen}', 
                         fontsize=16, fontweight='bold')
        
    def _plot_species_depth_scatter(self, creatures, ax):
        """Enhanced scatter plot showing all traits"""
        # Color mapping for vision types
        vision_colors = {
            "eyes": "blue", "no_eyes": "gray", "bioluminescence": "yellow",
            "echolocation": "purple", "lateral_line": "orange", "compound_eyes": "cyan"
        }
        
        # Size mapping for body size
        size_mapping = {
            "microscopic": 10, "small": 30, "medium": 60, "large": 100, "giant": 150
        }
        
        # Shape mapping for locomotion
        locomotion_markers = {
            "swimming": "o", "crawling": "s", "floating": "^", 
            "jet_propulsion": "D", "undulating": "v", "sessile": "8"
        }
        
        for creature in creatures:
            if creature.alive:
                color = vision_colors.get(creature.traits["vision"], "black")
                size = size_mapping.get(creature.traits["size"], 50)
                marker = locomotion_markers.get(creature.traits["locomotion"], "o")
                
                # Add transparency based on fitness
                alpha = min(1.0, max(0.1, creature.fitness / 5.0))
                
                ax.scatter(creature.depth, creature.fitness, 
                          c=color, s=size, marker=marker, alpha=alpha, 
                          edgecolors='black', linewidth=0.5)
        
        ax.set_xlabel('Depth (m)')
        ax.set_ylabel('Fitness')
        ax.set_title('Species Distribution by Depth & Fitness')
        ax.invert_xaxis()
        
        # Fix: Corrected the Line2D creation - removed extra comma
        vision_legend = [plt.Line2D([0], "", marker='o', color='w', 
                                   markerfacecolor=color, markersize=8, label=vision) 
                         for vision, color in vision_colors.items()]
        ax.legend(handles=vision_legend, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    def _plot_species_diversity_timeline(self, species_log, ax):
        """Plot species diversity over generations"""
        if not species_log:
            ax.text(0.5, 0.5, 'No species data available', 
                   ha='center', va='center', transform=ax.transAxes)
            return
            
        generations = [entry['generation'] for entry in species_log]
        total_species = [entry['total_species'] for entry in species_log]
        
        ax.plot(generations, total_species, 'b-', linewidth=2, marker='o')
        ax.fill_between(generations, total_species, alpha=0.3)
        ax.set_xlabel('Generation')
        ax.set_ylabel('Number of Species')
        ax.set_title('Species Diversity Over Time')
        ax.grid(True, alpha=0.3)
    
    def _plot_fitness_histogram(self, creatures, ax):
        """Fitness distribution histogram"""
        fitness_values = [c.fitness for c in creatures if c.alive]
        if fitness_values:
            ax.hist(fitness_values, bins=20, alpha=0.7, color='green', edgecolor='black')
            ax.axvline(np.mean(fitness_values), color='red', linestyle='--', 
                      label=f'Mean: {np.mean(fitness_values):.2f}')
            ax.set_xlabel('Fitness')
            ax.set_ylabel('Count')
            ax.set_title('Fitness Distribution')
            ax.legend()
        else:
            ax.text(0.5, 0.5, 'No living creatures', 
                   ha='center', va='center', transform=ax.transAxes)
    
    def _plot_trait_heatmap(self, creatures, ax):
        """Trait correlation heatmap"""
        trait_data = defaultdict(list)
        
        for creature in creatures:
            if creature.alive:
                trait_data['depth'].append(creature.depth)
                trait_data['fitness'].append(creature.fitness)
                trait_data['metabolic_rate'].append(creature.traits['metabolic_rate'])
                trait_data['oxygen_efficiency'].append(creature.traits['oxygen_efficiency'])
                trait_data['pressure_tolerance'].append(creature.traits['pressure_tolerance'])
                trait_data['light_production'].append(creature.traits['light_production'])
        
        if trait_data and len(trait_data['depth']) > 1:
            try:
                # Convert to correlation matrix
                df = pd.DataFrame(trait_data)
                corr_matrix = df.corr()
                
                # Plot heatmap
                im = ax.imshow(corr_matrix.values, cmap='RdBu_r', aspect='auto', 
                              vmin=-1, vmax=1)
                ax.set_xticks(range(len(corr_matrix.columns)))
                ax.set_yticks(range(len(corr_matrix.columns)))
                ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
                ax.set_yticklabels(corr_matrix.columns)
                ax.set_title('Trait Correlations')
                
                # Add correlation values
                for i in range(len(corr_matrix.columns)):
                    for j in range(len(corr_matrix.columns)):
                        value = corr_matrix.iloc[i, j]
                        if not pd.isna(value):
                            text_color = "white" if abs(value) > 0.5 else "black"
                            ax.text(j, i, f'{value:.2f}',
                                   ha="center", va="center", color=text_color, fontsize=8)
            except Exception as e:
                ax.text(0.5, 0.5, f'Heatmap error: {str(e)}', 
                       ha='center', va='center', transform=ax.transAxes)
        else:
            ax.text(0.5, 0.5, 'Insufficient data for correlations', 
                   ha='center', va='center', transform=ax.transAxes)
    
    def _plot_population_stats(self, gen_data, ax):
        """Population statistics"""
        if 'species' in gen_data and gen_data['species']:
            species_names = list(gen_data['species'].keys())[:10]  # Top 10 species
            counts = [gen_data['species'][name]['count'] for name in species_names]
            
            if species_names and counts:
                bars = ax.barh(range(len(species_names)), counts, color='skyblue')
                ax.set_yticks(range(len(species_names)))
                ax.set_yticklabels([name.split()[1] if len(name.split()) > 1 else name 
                                   for name in species_names], fontsize=8)
                ax.set_xlabel('Population Count')
                ax.set_title('Top Species by Population')
                
                # Add count labels on bars
                for i, (bar, count) in enumerate(zip(bars, counts)):
                    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                           str(count), va='center', fontsize=8)
        else:
            ax.text(0.5, 0.5, 'No species data available', 
                   ha='center', va='center', transform=ax.transAxes)
    
    def _plot_environmental_zones(self, creatures, ax):
        """Environmental zones with species distribution"""
        zones = [(0, 100, 'Surface', 'lightblue'), 
                (100, 1000, 'Mid-depth', 'blue'),
                (1000, 4000, 'Deep Sea', 'darkblue'), 
                (4000, 6000, 'Abyss', 'black')]
        
        zone_counts = defaultdict(int)
        for creature in creatures:
            if creature.alive:
                for min_d, max_d, zone_name, _ in zones:
                    if min_d <= creature.depth < max_d:
                        zone_counts[zone_name] += 1
                        break
        
        # Plot zones as horizontal bars
        for i, (min_d, max_d, zone_name, color) in enumerate(zones):
            ax.barh(i, max_d - min_d, left=min_d, color=color, alpha=0.3, 
                   height=0.8, edgecolor='black')
            text_color = 'white' if color in ['darkblue', 'black'] else 'black'
            ax.text(min_d + (max_d - min_d)/2, i, 
                   f'{zone_name}\n{zone_counts[zone_name]} creatures',
                   ha='center', va='center', fontweight='bold', color=text_color)
        
        ax.set_xlabel('Depth (m)')
        ax.set_yticks(range(len(zones)))
        ax.set_yticklabels([zone[2] for zone in zones])
        ax.set_title('Environmental Zones & Population')
        ax.invert_yaxis()
    
    def _plot_final_species_state(self, simulation):
        """Plot final state of species (non-real-time)"""
        fig, axs = plt.subplots(2, 3, figsize=(18, 12))
        axs = axs.flatten()
        
        self._plot_species_depth_scatter(simulation.creatures, axs[0])
        self._plot_fitness_histogram(simulation.creatures, axs[1])
        self._plot_trait_heatmap(simulation.creatures, axs[2])
        self._plot_environmental_zones(simulation.creatures, axs[3])
        
        if hasattr(simulation, 'species_log') and simulation.species_log:
            self._plot_species_diversity_timeline(simulation.species_log, axs[4])
            gen_data = simulation.species_log[-1] if simulation.species_log else {'species': {}}
            self._plot_population_stats(gen_data, axs[5])
        
        plt.tight_layout()
        plt.show()
    
    def _toggle_animation(self, event):
        """Toggle play/pause for animation"""
        self.is_playing = not self.is_playing
    
    def export_species_report(self, simulation, filename="species_report.txt"):
        """Export detailed species report"""
        try:
            species_summary = simulation.get_species_summary()
            
            with open(filename, 'w') as f:
                f.write("=== OCEAN ECOSYSTEM EVOLUTION REPORT ===\n\n")
                f.write(f"Simulation completed: {getattr(simulation, 'generation_count', 'Unknown')} generations\n")
                f.write(f"Total species evolved: {len(species_summary)}\n\n")
                
                f.write("SPECIES DETAILS:\n")
                f.write("-" * 50 + "\n")
                
                for species_name, info in sorted(species_summary.items(), 
                                               key=lambda x: x[1]['count'], reverse=True):
                    f.write(f"\n{species_name}:\n")
                    f.write(f"  Population: {info['count']}\n")
                    f.write(f"  Avg Fitness: {info['avg_fitness']:.2f}\n")
                    f.write(f"  Depth Range: {info['depth_range'][0]}m - {info['depth_range'][1]}m\n")
                    
                    if hasattr(info['example'], 'get_description'):
                        f.write(f"  Description: {info['example'].get_description()}\n")
                    
                    # Trait summary
                    traits = info['example'].traits
                    f.write("  Key Traits:\n")
                    f.write(f"    Vision: {traits['vision']}\n")
                    f.write(f"    Feeding: {traits['food_strategy']}\n")
                    f.write(f"    Body: {traits['body_type']}\n")
                    f.write(f"    Locomotion: {traits['locomotion']}\n")
                    f.write(f"    Size: {traits['size']}\n")
                    f.write(f"    Defense: {traits['defense_mechanism']}\n")
            
            print(f"Species report exported to {filename}")
        except Exception as e:
            print(f"Error exporting species report: {e}")

# Enhanced plotting functions for static analysis
def plot_detailed_depth_graph(avg_agg, depths, species_types, n_runs, ax=None):
    """Enhanced depth graph with more visual details"""
    colors = {
        "eyes": "blue", "bioluminescence": "gold", "plants": "green",
        "no_eyes_animal": "gray", "echolocation": "purple", 
        "lateral_line": "orange", "compound_eyes": "cyan"
    }
    
    labels = {
        "eyes": "Animals (Eyes)", "bioluminescence": "Bioluminescent",
        "plants": "Plants (Photosynthetic)", "no_eyes_animal": "Animals (No Eyes)",
        "echolocation": "Echolocating", "lateral_line": "Lateral Line",
        "compound_eyes": "Compound Eyes"
    }
    
    if ax is None:
        plt.figure(figsize=(12, 8))
        ax = plt.gca()
    
    # Plot with enhanced styling
    for sp in species_types:
        if depths and sp in avg_agg.get(depths[0], {}):
            counts = [avg_agg[d][sp] for d in depths]
            ax.plot(depths, counts, color=colors.get(sp, 'black'), 
                   label=labels.get(sp, sp), linewidth=3, marker='o', markersize=4)
            
            # Add fill under curve
            ax.fill_between(depths, counts, alpha=0.2, color=colors.get(sp, 'black'))
    
    # Add environmental zones as background
    zones = [(0, 100, 'Surface', 'lightblue'), (100, 1000, 'Mid-depth', 'lightgreen'),
             (1000, 4000, 'Deep Sea', 'lightcoral'), (4000, 6000, 'Abyss', 'lightgray')]
    
    for min_d, max_d, zone_name, color in zones:
        ax.axvspan(min_d, max_d, alpha=0.1, color=color)
        ax.text((min_d + max_d)/2, ax.get_ylim()[1] * 0.9, zone_name, 
               ha='center', va='top', fontweight='bold', rotation=0)
    
    ax.set_xlabel("Depth (m)", fontsize=12)
    ax.set_ylabel(f"Avg # Creatures (per run, {n_runs} runs)", fontsize=12)
    ax.set_title(f"Species Distribution by Ocean Depth ({n_runs} runs)", fontsize=14)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.invert_xaxis()
    plt.tight_layout()

def plot_four_configs(avg_aggs, depths, species_types, configs):
    """Enhanced four-panel comparison"""
    fig, axs = plt.subplots(2, 2, figsize=(20, 14), sharex=True, sharey=True)
    axs = axs.flatten()
    
    for i, nrun in enumerate(configs):
        try:
            plot_detailed_depth_graph(avg_aggs[i], depths, species_types, nrun, ax=axs[i])
        except Exception as e:
            axs[i].text(0.5, 0.5, f'Plot error: {str(e)}', 
                       ha='center', va='center', transform=axs[i].transAxes)
    
    plt.suptitle("Ocean Ecosystem Evolution Comparison", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

def create_interactive_dashboard(simulation):
    """Create an interactive dashboard for exploration"""
    visualizer = EnhancedVisualizer()
    visualizer.plot_detailed_species_evolution(simulation, real_time=True)
    return visualizer
