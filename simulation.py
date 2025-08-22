import random
import math
from environment import Environment
from creature import Creature

class Simulation:
    def __init__(self, n_creatures=50, generations=30):
        self.env = Environment()
        self.generations = generations
        self.creatures = [Creature(depth=random.randint(0, 6000)) for _ in range(n_creatures)]
        self.generation_count = 0
        self.species_log = []  # Track species evolution

    def evaluate_fitness(self, creature):
        """Enhanced fitness evaluation using the new creature traits"""
        layer = self.env.get_layer(creature.depth)
        fit = 0
        
        # Use the creature's own trait compatibility calculation
        fit += creature.calculate_trait_compatibility(layer)
        
        # Enhanced food strategy matching with new feeding types
        food_bonuses = {
            ("photosynthesis", "photosynthesis"): 2.5,
            ("photosynthesis", "herbivore"): 2.0,
            ("chemosynthesis", "chemosynthesis"): 2.2,
            ("chemosynthesis", "scavenger"): 1.8,
            ("chemosynthesis", "detritivore"): 1.6,
            ("marine snow", "filter"): 1.8,
            ("marine snow", "detritivore"): 1.6,
            ("marine snow", "scavenger"): 1.4,
            ("organics", "filter"): 1.5,
            ("organics", "predator"): 1.3,
            ("organics", "carnivore"): 1.4,
            ("organics", "omnivore"): 1.2
        }
        
        food_key = (layer.food_type, creature.traits["food_strategy"])
        if food_key in food_bonuses:
            fit += food_bonuses[food_key]
        
        # Advanced vision system fitness
        self._evaluate_vision_fitness(creature, fit)
        
        # Pressure adaptation penalties/bonuses
        self._evaluate_pressure_fitness(creature, fit)
        
        # Body type and locomotion efficiency
        self._evaluate_locomotion_fitness(creature, fit)
        
        # Size-depth relationship (realistic marine biology)
        self._evaluate_size_fitness(creature, fit)
        
        # Defense mechanism effectiveness
        self._evaluate_defense_fitness(creature, fit)
        
        # Social behavior fitness
        self._evaluate_social_fitness(creature, fit)
        
        # Metabolic efficiency
        self._evaluate_metabolic_fitness(creature, fit)
        
        # Environmental tolerance
        self._evaluate_tolerance_fitness(creature, fit)
        
        creature.fitness = max(0, fit)  # Ensure non-negative fitness

    def _evaluate_vision_fitness(self, creature, fit):
        """Detailed vision system evaluation"""
        depth = creature.depth
        vision = creature.traits["vision"]
        
        if depth < 200:  # Euphotic zone
            vision_scores = {
                "eyes": 2.0, "compound_eyes": 1.8, "lateral_line": 0.5,
                "bioluminescence": -0.8, "echolocation": 0.2, "no_eyes": -1.0
            }
        elif depth < 1000:  # Dysphotic zone
            vision_scores = {
                "eyes": 1.2, "bioluminescence": 1.5, "lateral_line": 1.0,
                "compound_eyes": 0.8, "echolocation": 1.2, "no_eyes": 0.5
            }
        else:  # Aphotic zone
            vision_scores = {
                "bioluminescence": 2.2, "echolocation": 2.0, "lateral_line": 1.8,
                "no_eyes": 1.5, "eyes": -1.5, "compound_eyes": -1.2
            }
        
        fit += vision_scores.get(vision, 0)

    def _evaluate_pressure_fitness(self, creature, fit):
        """Pressure adaptation evaluation"""
        depth = creature.depth
        pressure_adapt = creature.traits["pressure_adaptation"]
        
        if depth < 200 and pressure_adapt == "low":
            fit += 1.5
        elif depth < 1000 and pressure_adapt == "medium":
            fit += 1.5
        elif depth < 4000 and pressure_adapt == "high":
            fit += 1.5
        elif depth >= 4000 and pressure_adapt == "extreme":
            fit += 2.0
        else:
            fit -= 1.0  # Wrong pressure adaptation

    def _evaluate_locomotion_fitness(self, creature, fit):
        """Body type and locomotion synergy"""
        body = creature.traits["body_type"]
        locomotion = creature.traits["locomotion"]
        
        # Efficient combinations
        synergies = {
            ("streamlined", "swimming"): 1.5,
            ("elongated", "undulating"): 1.3,
            ("gelatinous", "floating"): 1.2,
            ("spherical", "jet_propulsion"): 1.4,
            ("flat", "crawling"): 1.1,
            ("armored", "crawling"): 0.8,
        }
        
        fit += synergies.get((body, locomotion), 0)
        
        # Sessile creatures get depth-based bonuses
        if locomotion == "sessile":
            if creature.depth > 2000:  # Deep sea sessile advantage
                fit += 1.0
            else:
                fit += 0.5

    def _evaluate_size_fitness(self, creature, fit):
        """Size-depth relationships based on marine biology"""
        size = creature.traits["size"]
        depth = creature.depth
        
        if depth < 200:  # Surface - all sizes viable
            size_bonuses = {"microscopic": 0.8, "small": 1.0, "medium": 1.2, 
                          "large": 1.0, "giant": 0.6}
        elif depth < 1000:  # Mid-depth - medium sizes preferred
            size_bonuses = {"microscopic": 0.6, "small": 1.2, "medium": 1.5, 
                          "large": 1.0, "giant": 0.4}
        else:  # Deep sea - smaller sizes more efficient
            size_bonuses = {"microscopic": 1.0, "small": 1.3, "medium": 1.0, 
                          "large": 0.7, "giant": 0.3}
        
        fit += size_bonuses.get(size, 0)

    def _evaluate_defense_fitness(self, creature, fit):
        """Defense mechanism effectiveness by depth"""
        defense = creature.traits["defense_mechanism"]
        depth = creature.depth
        
        if depth < 1000:  # Shallow water - more predators
            defense_values = {"speed": 1.2, "camouflage": 1.0, "toxins": 1.1, 
                            "spines": 0.8, "armor": 0.6, "mimicry": 1.0, "none": -0.5}
        else:  # Deep water - fewer but specialized predators
            defense_values = {"bioluminescence": 1.3, "camouflage": 0.8, "toxins": 1.0,
                            "armor": 1.0, "spines": 0.7, "speed": 0.6, "none": 0.0}
        
        fit += defense_values.get(defense, 0)

    def _evaluate_social_fitness(self, creature, fit):
        """Social behavior advantages/disadvantages"""
        social = creature.traits["social_behavior"]
        depth = creature.depth
        
        if depth < 1000:  # Shallow - schooling advantages
            social_bonuses = {"schooling": 1.0, "small_groups": 0.8, "colonial": 0.6,
                            "symbiotic": 0.7, "solitary": 0.3}
        else:  # Deep - solitary or symbiotic preferred
            social_bonuses = {"solitary": 1.0, "symbiotic": 1.2, "small_groups": 0.4,
                            "schooling": 0.2, "colonial": 0.8}
        
        fit += social_bonuses.get(social, 0)

    def _evaluate_metabolic_fitness(self, creature, fit):
        """Metabolic efficiency based on environment"""
        metabolic_rate = creature.traits["metabolic_rate"]
        oxygen_eff = creature.traits["oxygen_efficiency"]
        depth = creature.depth
        
        # Deep sea favors low metabolism and high oxygen efficiency
        if depth > 2000:
            if metabolic_rate < 1.0:
                fit += 1.0
            if oxygen_eff > 1.2:
                fit += 0.8
        else:
            # Surface can support higher metabolism
            if 0.8 <= metabolic_rate <= 1.5:
                fit += 0.5

    def _evaluate_tolerance_fitness(self, creature, fit):
        """Environmental tolerance evaluation"""
        temp_tolerance = creature.traits["temperature_tolerance"]
        pressure_tolerance = creature.traits["pressure_tolerance"]
        depth = creature.depth
        
        # Temperature tolerance by depth
        if depth > 3000:  # Cold deep water
            if temp_tolerance in ["cold", "extremophile"]:
                fit += 0.8
        elif depth < 500:  # Variable surface temperatures
            if temp_tolerance in ["moderate", "warm"]:
                fit += 0.6
        
        # Pressure tolerance
        expected_pressure = min(2.0, depth / 3000.0)
        pressure_diff = abs(pressure_tolerance - expected_pressure)
        fit -= pressure_diff * 0.5

    def run_generation(self):
        """Enhanced generation with species tracking"""
        # Evaluate all creatures
        for c in self.creatures:
            self.evaluate_fitness(c)
            c.alive = (c.fitness > 1.0)  # Slightly higher survival threshold
        
        # Track species diversity
        self._log_species_diversity()
        
        # Get survivors
        survivors = [c for c in self.creatures if c.alive]
        if not survivors:
            # Keep the fittest even if below threshold
            survivors = [max(self.creatures, key=lambda c: c.fitness)]
        
        # Reproduction with realistic constraints
        next_gen = []
        population_target = len(self.creatures)
        
        for c in survivors:
            # Reproductive success based on fitness and traits
            base_offspring = int(max(1, c.traits["repro_rate"]))
            fitness_multiplier = min(2.0, c.fitness / 2.0)
            offspring_num = int(base_offspring * fitness_multiplier)
            
            for _ in range(offspring_num):
                if len(next_gen) >= population_target:
                    break
                    
                # Offspring depth influenced by parent but with variation
                depth_variation = random.uniform(-500, 500)
                new_depth = max(0, min(6000, c.depth + depth_variation))
                
                offspring = c.mutate()
                offspring.depth = new_depth
                next_gen.append(offspring)
        
        # Maintain population size
        if len(next_gen) < population_target:
            # Fill remaining slots with mutations of best survivors
            best_survivors = sorted(survivors, key=lambda x: x.fitness, reverse=True)[:5]
            while len(next_gen) < population_target:
                parent = random.choice(best_survivors)
                offspring = parent.mutate()
                offspring.depth = random.randint(0, 6000)
                next_gen.append(offspring)
        
        self.creatures = next_gen[:population_target]
        self.generation_count += 1

    def _log_species_diversity(self):
        """Track species names and traits"""
        species_count = {}
        for c in self.creatures:
            if c.alive:
                species_name = c.species_name
                if species_name not in species_count:
                    species_count[species_name] = {'count': 0, 'avg_fitness': 0, 'depth_range': []}
                species_count[species_name]['count'] += 1
                species_count[species_name]['avg_fitness'] += c.fitness
                species_count[species_name]['depth_range'].append(c.depth)
        
        # Calculate averages
        for species in species_count:
            species_count[species]['avg_fitness'] /= species_count[species]['count']
            depths = species_count[species]['depth_range']
            species_count[species]['depth_range'] = [min(depths), max(depths)]
        
        self.species_log.append({
            'generation': self.generation_count,
            'species': species_count,
            'total_species': len(species_count)
        })

    def run(self):
        """Run the simulation with progress tracking"""
        print(f"Starting simulation: {len(self.creatures)} creatures, {self.generations} generations")
        
        for gen in range(self.generations):
            self.run_generation()
            
            if gen % 10 == 0 or gen == self.generations - 1:
                alive_count = sum(1 for c in self.creatures if c.alive)
                avg_fitness = sum(c.fitness for c in self.creatures) / len(self.creatures)
                print(f"Generation {gen}: {alive_count} survivors, avg fitness: {avg_fitness:.2f}")
        
        print("Simulation complete!")

    def get_species_summary(self):
        """Get a summary of final species"""
        species_summary = {}
        for c in self.creatures:
            if c.alive:
                name = c.species_name
                if name not in species_summary:
                    species_summary[name] = {
                        'count': 0,
                        'example': c,
                        'depth_range': [c.depth, c.depth],
                        'avg_fitness': 0
                    }
                species_summary[name]['count'] += 1
                species_summary[name]['avg_fitness'] += c.fitness
                species_summary[name]['depth_range'][0] = min(species_summary[name]['depth_range'], c.depth)
                species_summary[name]['depth_range'][1] = max(species_summary[name]['depth_range'][1], c.depth)
        
        # Calculate averages
        for species in species_summary:
            species_summary[species]['avg_fitness'] /= species_summary[species]['count']
        
        return species_summary
