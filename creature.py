import random
import math

class Creature:
    # Possible traits
    possible_vision = ["eyes", "no_eyes", "bioluminescence", "echolocation", "lateral_line", "compound_eyes"]

    possible_food_strategy = ["photosynthesis", "filter", "predator", "scavenger", "parasite",
                             "chemosynthesis", "detritivore", "carnivore", "herbivore", "omnivore"]

    possible_body_type = ["streamlined", "flat", "spherical", "elongated", "gelatinous", "armored"]

    possible_locomotion = ["swimming", "crawling", "floating", "jet_propulsion", "undulating", "sessile"]

    possible_size = ["microscopic", "small", "medium", "large", "giant"]

    possible_pressure_adaptation = ["low", "medium", "high", "extreme"]

    possible_temperature = ["cold", "moderate", "warm", "extremophile"]

    possible_defense = ["camouflage", "spines", "toxins", "speed", "armor", "mimicry", "none"]

    possible_social = ["solitary", "small_groups", "schooling", "colonial", "symbiotic"]

    def __init__(self, depth, traits=None):
        if traits:
            self.traits = traits.copy()
        else:
            self.traits = {
                "vision": random.choice(self.possible_vision),
                "food_strategy": random.choice(self.possible_food_strategy),
                "move_eff": random.uniform(0.3, 2.0),
                "repro_rate": random.uniform(0.2, 2.5),
                "body_type": random.choice(self.possible_body_type),
                "locomotion": random.choice(self.possible_locomotion),
                "size": random.choice(self.possible_size),
                "pressure_adaptation": random.choice(self.possible_pressure_adaptation),
                "temperature": random.choice(self.possible_temperature),
                "defense": random.choice(self.possible_defense),
                "social": random.choice(self.possible_social),
                "metabolic_rate": random.uniform(0.2, 2.0),
                "oxygen_efficiency": random.uniform(0.3, 1.8),
                "light_intensity": random.uniform(0.0, 1.0),
                "pressure_tolerance": random.uniform(0.1, 2.0),
                "salinity_tolerance": random.uniform(0.3, 1.5),
                "aggression": random.uniform(0.0, 1.0),
                "camouflage_ability": random.uniform(0.0, 1.0),
                "migration_tendency": random.uniform(0.0, 1.0),
            }
        self.depth = depth
        self.alive = True
        self.fitness = 0.1  # minimal fitness to avoid zero division
        self.age = 0
        self.energy = 100.0
        self.species_name = self.generate_species_name()

    def generate_species_name(self):
        depth_prefix_map = {
            (0, 200): "Superficie",
            (200, 1000): "Meso",
            (1000, 4000): "Bathy",
            (4000, 6000): "Abysso",
        }

        vision_suffix_map = {
            "eyes": "opticus",
            "no_eyes": "caecus",
            "bioluminescence": "lucidus",
            "echolocation": "sonarus",
            "lateral_line": "lateralis",
            "compound_eyes": "multiopus",
        }

        prefix = "Abysso"
        for (low, high), name in depth_prefix_map.items():
            if low <= self.depth < high:
                prefix = name
                break

        suffix = vision_suffix_map.get(self.traits["vision"], "mysticus")
        return f"{prefix} {suffix}"

    def mutate(self, mutation_rate=0.15):
        new_traits = self.traits.copy()

        categorical_traits = [
            ("vision", self.possible_vision),
            ("food_strategy", self.possible_food_strategy),
            ("body_type", self.possible_body_type),
            ("locomotion", self.possible_locomotion),
            ("size", self.possible_size),
            ("pressure_adaptation", self.possible_pressure_adaptation),
            ("temperature", self.possible_temperature),
            ("defense", self.possible_defense),
            ("social", self.possible_social),
        ]

        for trait, options in categorical_traits:
            if random.random() < mutation_rate:
                new_traits[trait] = random.choice(options)

        numerical_traits = {
            "move_eff": (0.3, 2.0, 0.15),
            "repro_rate": (0.2, 2.5, 0.2),
            "metabolic_rate": (0.2, 2.0, 0.1),
            "oxygen_efficiency": (0.3, 1.8, 0.1),
            "light_intensity": (0.0, 1.0, 0.1),
            "pressure_tolerance": (0.1, 2.0, 0.15),
            "salinity_tolerance": (0.3, 1.5, 0.1),
            "aggression": (0.0, 1.0, 0.1),
            "camouflage_ability": (0.0, 1.0, 0.1),
            "migration_tendency": (0.0, 1.0, 0.1),
        }

        for trait, (low, high, strength) in numerical_traits.items():
            if random.random() < mutation_rate:
                change = random.uniform(-strength, strength)
                new_val = max(low, min(high, new_traits[trait] + change))
                new_traits[trait] = new_val

        offspring = Creature(self.depth, new_traits)
        offspring.species_name = offspring.generate_species_name()
        return offspring

    def calculate_compatibility(self, layer):
        score = 0.0
        depth = self.depth
        vision = self.traits["vision"]
        strategy = self.traits["food_strategy"]

        # Vision compatibility
        if depth < 200:  # Euphotic
            vision_scores = {
                "eyes": 2.0,
                "compound_eyes": 1.8,
                "lateral_line": 0.5,
                "bioluminescence": -0.8,
                "echolocation": 0.2,
                "no_eyes": -1.0,
            }
        elif depth < 1000:  # Dysphotic
            vision_scores = {
                "bioluminescence": 1.5,
                "echolocation": 1.2,
                "lateral_line": 1.0,
                "eyes": 1.2,
                "compound_eyes": 0.8,
                "no_eyes": 0.5,
            }
        else:  # Aphotic
            vision_scores = {
                "bioluminescence": 2.2,
                "echolocation": 2.0,
                "lateral_line": 1.8,
                "no_eyes": 1.5,
                "eyes": -1.5,
                "compound_eyes": -1.2,
            }
        score += vision_scores.get(vision, 0)

        # Pressure adaptation
        pressure_map = {
            (0, 200): "low",
            (200, 1000): "medium",
            (1000, 4000): "high",
            (4000, 6000): "extreme",
        }

        required_pressure = "extreme"
        for (low, high), pres in pressure_map.items():
            if low <= depth < high:
                required_pressure = pres
                break

        if self.traits["pressure_adaptation"] == required_pressure:
            score += 1.5
        else:
            idx_req = list(pressure_map.values()).index(required_pressure)
            idx_trait = list(pressure_map.values()).index(self.traits["pressure_adaptation"])
            diff = abs(idx_req - idx_trait)
            if diff == 1:
                score += 0.5
            else:
                score -= 1.0

        # Food compatibility
        if layer.food_type == "photosynthesis" and strategy in ["photosynthesis", "herbivore"]:
            score += 2.0
        elif layer.food_type == "chemosynthesis" and strategy in ["chemosynthesis", "detritivore", "scavenger"]:
            score += 1.8
        elif layer.food_type == "marine snow" and strategy in ["filter", "detritivore", "scavenger"]:
            score += 1.5
        elif layer.food_type == "organics" and strategy in ["filter", "predator", "carnivore"]:
            score += 1.0

        # Body-locomotion synergy
        synergy_map = {
            "swimming": ["streamlined", "elongated"],
            "floating": ["gelatinous", "spherical"],
            "crawling": ["flat", "armored"],
            "jet_propulsion": ["spherical", "streamlined"],
        }

        if self.traits["body_type"] in synergy_map.get(self.traits["locomotion"], []):
            score += 0.5

        return score

    def __str__(self):
        return f"{self.species_name} (Depth: {int(self.depth)}m, Fitness: {self.fitness:.2f})"

    def description(self):
        size_desc_map = {
            "microscopic": "tiny",
            "small": "small",
            "medium": "medium-sized",
            "large": "large",
            "giant": "gigantic",
        }

        desc = f"{self.species_name} is a {size_desc_map[self.traits['size']]} "
        desc += f"{self.traits['body_type']} creature that moves by {self.traits['locomotion']}. "
        desc += f"It uses {self.traits['vision']} for navigation and feeds via {self.traits['food_strategy']}. "
        desc += f"It lives at depth around {int(self.depth)} meters."
        return desc
