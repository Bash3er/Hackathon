import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from collections import defaultdict
from simulation import Simulation
import numpy as np
import random

class InteractiveDepthVisualizer:
    def __init__(self, n_runs=15, n_creatures=40, generations=12, step=200):
        self.n_runs = n_runs
        self.n_creatures = n_creatures
        self.generations = generations
        self.step = step
        self.depth_data = {}

        print("Calculating survival data across depths. This may take several minutes.")
        self.calculate_all_depths()

        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(bottom=0.25)

        self.ax_slider = plt.axes([0.1, 0.10, 0.65, 0.03], facecolor='lightgoldenrodyellow')
        self.depth_slider = Slider(self.ax_slider, "Ocean Depth (m)", 0, 6000, valinit=0, valstep=step)
        self.depth_slider.on_changed(self.update_plot)

        self.update_plot(0)

    def calculate_all_depths(self):
        depths = list(range(0, 6001, self.step))
        for idx, depth in enumerate(depths):
            print(f"Processing depth {depth}m ({idx + 1}/{len(depths)})")
            counts = defaultdict(int)
            total_survivors = 0

            for _ in range(self.n_runs):
                sim = Simulation(n_creatures=self.n_creatures, generations=self.generations)
                # set all to depth
                for c in sim.creatures:
                    c.depth = depth

                sim.run()

                for c in sim.creatures:
                    if c.fitness > 1.0:
                        total_survivors += 1
                        vis = c.traits["vision"]
                        food = c.traits["food_strategy"]

                        if vis == "eyes":
                            counts["Animals (Eyes)"] += 1
                        elif vis == "bioluminescence":
                            counts["Bioluminescent"] += 1
                        elif vis == "no_eyes":
                            if food == "photosynthesis":
                                counts["Plants (Photosynthetic)"] += 1
                            else:
                                counts["Animals (No Eyes)"] += 1
                        elif vis == "echolocation":
                            counts["Echolocating"] += 1
                        elif vis == "compound_eyes":
                            counts["Compound-eyed"] += 1
                        elif vis == "lateral_line":
                            counts["Lateral-line"] += 1
                        else:
                            counts[vis] += 1

            # Average counts
            for key in counts:
                counts[key] /= self.n_runs

            self.depth_data[depth] = {
                "counts": dict(counts),
                "total_survivors": total_survivors / self.n_runs,
            }

        print("Calculation complete.")

    def update_plot(self, val):
        depth = int(val)
        if depth not in self.depth_data:
            # Find nearest step
            depth = min(self.depth_data.keys(), key=lambda d: abs(d - depth))

        data = self.depth_data[depth]
        self.ax.clear()

        counts = data["counts"]
        species = list(counts.keys())
        vals = list(counts.values())

        colors = {
            "Animals (Eyes)": "blue",
            "Bioluminescent": "yellow",
            "Plants (Photosynthetic)": "green",
            "Animals (No Eyes)": "gray",
            "Echolocating": "purple",
            "Compound-eyed": "cyan",
            "Lateral-line": "orange",
        }

        if species:
            bars = self.ax.bar(species, vals, color=[colors.get(s, "red") for s in species], alpha=0.7, edgecolor='black')
            for bar, val in zip(bars, vals):
                if val > 0:
                    self.ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                                 f"{val:.1f}", ha="center", va="bottom", fontweight="bold")
            self.ax.set_ylim(0, max(vals) * 1.3 + 0.5)
        else:
            self.ax.text(0.5, 0.5, "No survivors at this depth", ha="center", va="center", transform=self.ax.transAxes, fontsize=16, alpha=0.7)
            self.ax.set_ylim(0, 1)

        self.ax.set_title(f"Live Ecosystem at {depth}m Depth (avg. over {self.n_runs} runs)", fontsize=14)
        self.ax.set_ylabel("Average # Survivors per Run")
        self.ax.set_xlabel("Species Type")
        self.ax.tick_params(axis='x', rotation=45)

        layer = self.get_ocean_layer(depth)
        self.ax.text(0.02, 0.97, f"Ocean Layer: {layer}", transform=self.ax.transAxes, fontsize=10,
                     verticalalignment='top', bbox=dict(facecolor='lightblue', alpha=0.5))

        self.fig.canvas.draw_idle()

    def get_ocean_layer(self, depth):
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

def run_interactive():
    print("Launching Interactive Depth Visualizer...")
    visualizer = InteractiveDepthVisualizer()
    visualizer.show()

if __name__ == "__main__":
    run_interactive()
