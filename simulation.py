import random
import math
from environment import Environment
from creature import Creature

class Simulation:
    def __init__(self, n_creatures=50, generations=30):
        self.env = Environment()
        self.generations = generations
        self.creatures = [Creature(random.randint(0,6000)) for _ in range(n_creatures)]
        self.generation_count = 0
        self.species_log = []

    def evaluate_fitness(self, creature):
        layer = self.env.get_layer(creature.depth)
        # print(f"Creature depth: {creature.depth}, Layer: {layer.name}, food_type: {layer.food_type}")
        fitness = 0.1  # base fitness
        fitness += creature.calculate_compatibility(layer)
        creature.fitness = max(0.1, fitness)


    def run_generation(self):
        for creature in self.creatures:
            self.evaluate_fitness(creature)

        # Survival criterion
        threshold = 0.5
        for creature in self.creatures:
            creature.alive = creature.fitness >= threshold

        survivors = [c for c in self.creatures if c.alive]

        # Prevent extinction
        if len(survivors) < 5:
            survivors = sorted(self.creatures, key=lambda x: x.fitness, reverse=True)[:5]
            for c in survivors:
                c.alive = True

        # Reproduction till population size
        next_gen = []
        max_population = len(self.creatures)

        while len(next_gen) < max_population:
            parent = random.choice(survivors)
            # offspring count proportional to fitness & repro_rate
            offspring_count = max(1, int(parent.fitness * parent.traits['repro_rate']))

            for _ in range(offspring_count):
                if len(next_gen) >= max_population:
                    break
                child = parent.mutate()
                # Slight depth variation
                child.depth = max(0, min(6000, parent.depth + random.uniform(-200, 200)))
                next_gen.append(child)

        self.creatures = next_gen[:max_population]
        self.generation_count += 1
        self.log_species_diversity()

    def run(self, progress_callback=None):
        # print(f"Starting simulation with {len(self.creatures)} creatures for {self.generations} generations")
        for gen in range(self.generations):
            self.run_generation()
            if progress_callback:
                progress_callback()  # Notify progress externally
            if gen % 5 == 0 or gen == self.generations - 1:
                alive_count = sum(c.alive for c in self.creatures)
                avg_fitness = sum(c.fitness for c in self.creatures) / len(self.creatures)
                # print(f"Generation {gen}: {alive_count} survivors, avg fitness {avg_fitness:.2f}")
        # print("Simulation complete.")

    def log_species_diversity(self):
        species_count = {}
        for c in self.creatures:
            if c.alive:
                sp = c.species_name
                if sp not in species_count:
                    species_count[sp] = {'count': 0, 'fitness': 0.0, 'depths': []}
                species_count[sp]['count'] += 1
                species_count[sp]['fitness'] += c.fitness
                species_count[sp]['depths'].append(c.depth)

        # Compute averages
        for sp in species_count:
            species_count[sp]['fitness'] /= species_count[sp]['count']
            species_count[sp]['depth_range'] = [min(species_count[sp]['depths']), max(species_count[sp]['depths'])]

        self.species_log.append({
            'generation': self.generation_count,
            'species': species_count,
            'total_species': len(species_count),
        })

    def get_species_summary(self):
        summary = {}
        for c in self.creatures:
            if c.alive:
                sp = c.species_name
                if sp not in summary:
                    summary[sp] = {'count': 0, 'fitness': 0, 'depth_range': [c.depth, c.depth]}
                summary[sp]['count'] += 1
                summary[sp]['fitness'] += c.fitness
                summary[sp]['depth_range'][0] = min(summary[sp]['depth_range'], c.depth)
                summary[sp]['depth_range'][1] = max(summary[sp]['depth_range'][1], c.depth)

        for sp in summary:
            summary[sp]['fitness'] /= summary[sp]['count']

        return summary
