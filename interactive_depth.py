import matplotlib
# Use 'Qt5Agg', 'TkAgg', or 'MacOSX' depending on your system. Qt5Agg is more cross-platform.
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from simulation import Simulation
from collections import defaultdict

class InteractiveDepthVisualizer:
    def __init__(self, n_runs=20, n_creatures=50, generations=15, step=200):
        self.n_runs = n_runs
        self.n_creatures = n_creatures
        self.generations = generations
        self.depth_data = {}
        self.current_depth = 0
        self.step = step

        print("Calculating ecosystem data for all depths... (this may take a few minutes)")
        self.calculate_all_depths()
        
        # Create the figure and axis
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(bottom=0.25)
        
        # Create slider
        self.ax_slider = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        self.depth_slider = Slider(
            self.ax_slider, 
            'Ocean Depth (m)', 
            0, 6000, 
            valinit=0, 
            valfmt='%d'
        )
        
        # Connect slider to update function
        self.depth_slider.on_changed(self.update_plot)
        # Initial plot
        self.update_plot(0)

    def calculate_all_depths(self):
        """Pre-calculate survival data for all depths - efficient version."""
        depths = list(range(0, 6001, self.step))
        for i, depth in enumerate(depths):
            survivor_counts = defaultdict(int)
            total_survivors = 0

            print(f"Processing depth {depth}m... ({i+1}/{len(depths)})")
            for _ in range(self.n_runs):
                sim = Simulation(n_creatures=self.n_creatures, generations=self.generations)
                # Set all creatures to this specific depth
                for c in sim.creatures:
                    c.depth = depth

                sim.run()
                for c in sim.creatures:
                    if c.fitness > 1:  # Survived
                        total_survivors += 1
                        vision = c.traits.get("vision", "unknown")
                        feeding = c.traits.get("food_strategy", "unknown")
                        # Enhanced: Support all vision types
                        if vision == "eyes":
                            survivor_counts["Animals (Eyes)"] += 1
                        elif vision == "bioluminescence":
                            survivor_counts["Bioluminescent"] += 1
                        elif vision == "no_eyes":
                            if feeding == "photosynthesis":
                                survivor_counts["Plants (Photosynthetic)"] += 1
                            else:
                                survivor_counts["Animals (No Eyes)"] += 1
                        elif vision == "echolocation":
                            survivor_counts["Echolocating"] += 1
                        elif vision == "compound_eyes":
                            survivor_counts["Compound-eyed"] += 1
                        elif vision == "lateral_line":
                            survivor_counts["Lateral-line"] += 1
                        else:
                            survivor_counts[vision] += 1

            # Average across runs
            for key in survivor_counts:
                survivor_counts[key] /= self.n_runs

            self.depth_data[depth] = {
                'counts': dict(survivor_counts),
                'total_survivors': total_survivors / self.n_runs
            }
        print("Calculation complete.")

    def update_plot(self, val):
        """Update the plot based on slider value"""
        depth = int(round(self.depth_slider.val / self.step) * self.step)
        depth = max(0, min(6000, depth))
        closest_depth = min(self.depth_data.keys(), key=lambda x: abs(x - depth))
        data = self.depth_data[closest_depth]
        
        self.ax.clear()
        species = list(data['counts'].keys()) if data['counts'] else []
        counts = list(data['counts'].values()) if data['counts'] else []

        colors = {
            "Animals (Eyes)": "blue",
            "Bioluminescent": "yellow", 
            "Plants (Photosynthetic)": "green",
            "Animals (No Eyes)": "gray",
            "Echolocating": "purple",
            "Compound-eyed": "cyan",
            "Lateral-line": "orange"
        }
        if species and counts:
            plot_colors = [colors.get(s, "red") for s in species]
            bars = self.ax.bar(species, counts, color=plot_colors, alpha=0.7, edgecolor='black')
            for bar, count in zip(bars, counts):
                if count > 0:
                    self.ax.text(
                        bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                        f'{count:.1f}', ha='center', va='bottom', fontweight='bold')
            self.ax.set_ylim(0, max(counts) * 1.3 + 0.5)
        else:
            self.ax.text(0.5, 0.5, 'No survivors at this depth',
                         ha='center', va='center', transform=self.ax.transAxes,
                         fontsize=16, alpha=0.7)
            self.ax.set_ylim(0, 1)

        self.ax.set_title(
            f'Ecosystem at {closest_depth}m Depth\n(Average of {self.n_runs} simulation runs)', fontsize=14)
        self.ax.set_ylabel('Average Number of Survivors per Run', fontsize=12)
        self.ax.set_xlabel('Species Type', fontsize=12)
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')

        layer_info = self.get_ocean_layer_info(closest_depth)
        self.ax.text(
            0.02, 0.98, f'Ocean Layer: {layer_info}',
            transform=self.ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        self.fig.canvas.draw_idle()

    def get_ocean_layer_info(self, depth):
        if depth < 100:
            return "Surface (Photosynthesis Zone)"
        elif depth < 1000:
            return "Mid-depth (Organics Zone)"
        elif depth < 4000:
            return "Deep Sea (Marine Snow Zone)"
        else:
            return "Abyss (Chemosynthesis Zone)"

    def show(self):
        plt.tight_layout()
        plt.show()

def run_interactive_depth():
    print("Creating interactive depth visualizer...")
    print("This may take a few minutes to calculate all depths...")

    try:
        visualizer = InteractiveDepthVisualizer(n_runs=15, n_creatures=40, generations=12, step=200)
        visualizer.show()
    except Exception as e:
        print(f"Error: {e}")
        print("Try installing PyQt5 or run from a terminal (not an IDE).")

if __name__ == "__main__":
    run_interactive_depth()
