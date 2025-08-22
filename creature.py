import random
import math

class Creature:
    # Vision adaptations
    possible_vision = ["eyes", "no_eyes", "bioluminescence", "echolocation", "lateral_line", "compound_eyes"]
    
    # Feeding strategies
    possible_food_strategy = ["photosynthesis", "filter", "predator", "scavenger", "parasite", 
                            "chemosynthesis", "detritivore", "carnivore", "herbivore", "omnivore"]
    
    # Body types and adaptations
    possible_body_type = ["streamlined", "flat", "spherical", "elongated", "gelatinous", "armored"]
    possible_locomotion = ["swimming", "crawling", "floating", "jet_propulsion", "undulating", "sessile"]
    possible_size = ["microscopic", "small", "medium", "large", "giant"]
    
    # Physiological adaptations
    possible_pressure_adaptation = ["low", "medium", "high", "extreme"]
    possible_temperature_tolerance = ["cold", "moderate", "warm", "extremophile"]
    
    # Defensive mechanisms
    possible_defense = ["camouflage", "spines", "toxins", "speed", "armor", "mimicry", "none"]
    
    # Social behavior
    possible_social_behavior = ["solitary", "small_groups", "schooling", "colonial", "symbiotic"]

    def __init__(self, depth, traits=None):
        if traits:
            self.traits = traits.copy()
        else:
            self.traits = {
                # Basic traits
                "vision": random.choice(self.possible_vision),
                "food_strategy": random.choice(self.possible_food_strategy),
                "move_eff": random.uniform(0.3, 2.0),
                "repro_rate": random.uniform(0.2, 2.5),
                
                # Physical characteristics
                "body_type": random.choice(self.possible_body_type),
                "locomotion": random.choice(self.possible_locomotion),
                "size": random.choice(self.possible_size),
                
                # Environmental adaptations
                "pressure_adaptation": random.choice(self.possible_pressure_adaptation),
                "temperature_tolerance": random.choice(self.possible_temperature_tolerance),
                
                # Survival traits
                "defense_mechanism": random.choice(self.possible_defense),
                "social_behavior": random.choice(self.possible_social_behavior),
                
                # Metabolic traits
                "metabolic_rate": random.uniform(0.2, 2.0),  # Energy consumption
                "oxygen_efficiency": random.uniform(0.3, 1.8),  # Oxygen use efficiency
                
                # Specialized adaptations
                "light_production": random.uniform(0.0, 1.0),  # Bioluminescence intensity
                "pressure_tolerance": random.uniform(0.1, 2.0),  # Deep sea adaptation
                "salinity_tolerance": random.uniform(0.3, 1.5),  # Salt tolerance
                
                # Behavioral traits  
                "aggression": random.uniform(0.0, 1.0),
                "camouflage_ability": random.uniform(0.0, 1.0),
                "migration_tendency": random.uniform(0.0, 1.0),
            }
        
        self.depth = depth
        self.alive = True
        self.fitness = 0
        self.age = 0
        self.energy = 100.0
        self.species_name = self.generate_species_name()

    def generate_species_name(self):
        """Generate a scientific-sounding species name based on traits"""
        depth_prefixes = {
            (0, 200): "Superficie",
            (200, 1000): "Meso", 
            (1000, 4000): "Bathy",
            (4000, 6000): "Abysso"
        }
        
        vision_suffixes = {
            "eyes": "opticus",
            "no_eyes": "caecus", 
            "bioluminescence": "lucidus",
            "echolocation": "sonarus",
            "lateral_line": "lateralis",
            "compound_eyes": "multiopus"
        }
        
        for depth_range, prefix in depth_prefixes.items():
            if depth_range[0] <= self.depth < depth_range[1]:
                depth_prefix = prefix
                break
        else:
            depth_prefix = "Abysso"
            
        vision_suffix = vision_suffixes.get(self.traits["vision"], "mysticus")
        return f"{depth_prefix} {vision_suffix}"

    def mutate(self, mutation_rate=0.15):
        """Enhanced mutation with realistic constraints"""
        new_traits = self.traits.copy()
        
        # Mutate categorical traits
        categorical_traits = [
            ("vision", self.possible_vision),
            ("food_strategy", self.possible_food_strategy), 
            ("body_type", self.possible_body_type),
            ("locomotion", self.possible_locomotion),
            ("size", self.possible_size),
            ("pressure_adaptation", self.possible_pressure_adaptation),
            ("temperature_tolerance", self.possible_temperature_tolerance),
            ("defense_mechanism", self.possible_defense),
            ("social_behavior", self.possible_social_behavior)
        ]
        
        for trait_name, possible_values in categorical_traits:
            if random.random() < mutation_rate:
                new_traits[trait_name] = random.choice(possible_values)
        
        # Mutate numerical traits with constraints
        numerical_traits = {
            "move_eff": (0.3, 2.0, 0.15),
            "repro_rate": (0.2, 2.5, 0.2), 
            "metabolic_rate": (0.2, 2.0, 0.1),
            "oxygen_efficiency": (0.3, 1.8, 0.1),
            "light_production": (0.0, 1.0, 0.1),
            "pressure_tolerance": (0.1, 2.0, 0.15),
            "salinity_tolerance": (0.3, 1.5, 0.1),
            "aggression": (0.0, 1.0, 0.1),
            "camouflage_ability": (0.0, 1.0, 0.1),
            "migration_tendency": (0.0, 1.0, 0.1)
        }
        
        for trait_name, (min_val, max_val, mutation_strength) in numerical_traits.items():
            if random.random() < mutation_rate:
                change = random.uniform(-mutation_strength, mutation_strength)
                new_traits[trait_name] = max(min_val, min(max_val, new_traits[trait_name] + change))
        
        # Create new creature with mutated traits
        offspring = Creature(self.depth, new_traits)
        offspring.species_name = offspring.generate_species_name()
        return offspring

    def calculate_trait_compatibility(self, environment_layer):
        """Calculate how well traits match the environment"""
        compatibility_score = 0.0
        
        # Vision adaptation scoring
        if self.depth < 200:  # Sunlight zone
            if self.traits["vision"] in ["eyes", "compound_eyes"]:
                compatibility_score += 2.0
            elif self.traits["vision"] == "bioluminescence":
                compatibility_score -= 0.5  # Wasteful in light
        elif self.depth < 1000:  # Twilight zone  
            if self.traits["vision"] in ["eyes", "bioluminescence"]:
                compatibility_score += 1.5
        else:  # Deep zones
            if self.traits["vision"] in ["bioluminescence", "echolocation", "lateral_line", "no_eyes"]:
                compatibility_score += 2.0
            elif self.traits["vision"] == "eyes":
                compatibility_score -= 1.0
        
        # Pressure adaptation
        pressure_zones = {
            (0, 200): "low",
            (200, 1000): "medium", 
            (1000, 4000): "high",
            (4000, 6000): "extreme"
        }
        
        required_pressure = "low"
        for depth_range, pressure in pressure_zones.items():
            if depth_range[0] <= self.depth < depth_range[1]:
                required_pressure = pressure
                break
        
        if self.traits["pressure_adaptation"] == required_pressure:
            compatibility_score += 1.5
        elif abs(list(pressure_zones.values()).index(self.traits["pressure_adaptation"]) - 
                list(pressure_zones.values()).index(required_pressure)) == 1:
            compatibility_score += 0.5
        else:
            compatibility_score -= 1.0
            
        # Food strategy compatibility
        if environment_layer.food_type == "photosynthesis":
            if self.traits["food_strategy"] in ["photosynthesis", "herbivore"]:
                compatibility_score += 2.0
        elif environment_layer.food_type == "chemosynthesis":
            if self.traits["food_strategy"] in ["chemosynthesis", "scavenger", "detritivore"]:
                compatibility_score += 1.8
        elif environment_layer.food_type == "marine snow":
            if self.traits["food_strategy"] in ["filter", "detritivore", "scavenger"]:
                compatibility_score += 1.5
        
        # Body type and locomotion synergy
        efficient_combinations = {
            "swimming": ["streamlined", "elongated"],
            "floating": ["gelatinous", "spherical"],
            "crawling": ["flat", "armored"],
            "jet_propulsion": ["spherical", "streamlined"]
        }
        
        if self.traits["body_type"] in efficient_combinations.get(self.traits["locomotion"], []):
            compatibility_score += 0.5
            
        return compatibility_score

    def get_description(self):
        """Get a detailed description of the creature"""
        size_desc = {
            "microscopic": "tiny microscopic",
            "small": "small", 
            "medium": "medium-sized",
            "large": "large",
            "giant": "gigantic"
        }
        
        return (f"{self.species_name}: A {size_desc[self.traits['size']]} "
                f"{self.traits['body_type']} creature that moves by {self.traits['locomotion']}. "
                f"It uses {self.traits['vision']} for navigation and feeds through "
                f"{self.traits['food_strategy']}. Lives at {self.depth}m depth.")

    def __str__(self):
        return f"{self.species_name} (Depth: {self.depth}m, Fitness: {self.fitness:.2f})"
