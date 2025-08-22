class OceanLayer:
    def __init__(self, name, depth_range, light_intensity, food_type):
        self.name = name
        self.depth_range = depth_range
        self.light_intensity = light_intensity
        self.food_type = food_type

class Environment:
    def __init__(self):
        self.layers = [
            OceanLayer("Surface", (0, 100), 1.0, "photosynthesis"),
            OceanLayer("Mid-depth", (100, 1000), 0.3, "organics"),
            OceanLayer("Deep Sea", (1000, 4000), 0.05, "marine snow"),
            OceanLayer("Abyss", (4000, 6000), 0.01, "chemosynthesis"),
        ]

    def get_layer(self, depth):
        for layer in self.layers:
            d_min, d_max = layer.depth_range
            if d_min <= depth < d_max:
                return layer
        return self.layers[-1]
