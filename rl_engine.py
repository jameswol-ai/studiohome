import random
from collections import defaultdict

class CityPolicy:
    def __init__(self, lr=0.2, decay=0.99, max_size=1000):
        self.risk_map = defaultdict(float)
        self.lr = lr
        self.decay = decay
        self.max_size = max_size

    def choose_location(self, max_attempts=10):
        for _ in range(max_attempts):
            x, y = random.randint(0, 25), random.randint(0, 25)
            if self.risk_map[(x, y)] <= 2.0:
                return x, y
        return random.randint(0, 25), random.randint(0, 25)

    def update(self, failed_nodes):
        for n in failed_nodes:
            x, y, z = n
            self.risk_map[(x, y)] += self.lr
        for k in list(self.risk_map.keys()):
            self.risk_map[k] *= self.decay
            if self.risk_map[k] < 0.01:
                del self.risk_map[k]
        if len(self.risk_map) > self.max_size:
            sorted_keys = sorted(self.risk_map, key=self.risk_map.get)
            for k in sorted_keys[:len(self.risk_map)-self.max_size]:
                del self.risk_map[k]

class RLBuildingEngine:
    def generate(self, policy):
        buildings = []
        for _ in range(5):
            x, y = policy.choose_location()
            buildings.append({
                "x": x,
                "y": y,
                "floors": random.randint(3, 10),
                "grid": random.choice([6, 8, 10, 12])
            })
        return buildings

class RLPhysics:
    def build_nodes(self, buildings):
        nodes = []
        for b in buildings:
            for z in range(b["floors"]):
                for x in range(0, b["grid"], 2):
                    for y in range(0, b["grid"], 2):
                        nodes.append((x + b["x"], y + b["y"], z))
        return nodes

    def loads(self, nodes):
        load = {n: 0.0 for n in nodes}
        if not nodes:
            return load
        max_z = max(n[2] for n in nodes)
        for n in nodes:
            if n[2] == max_z:
                load[n] += 1.0
        for _ in range(2):
            for (x, y, z), l in list(load.items()):
                below = (x, y, z - 1)
                if below in load:
                    load[below] += l * 0.7
        return load

    def collapse(self, load):
        return {n for n, l in load.items() if l > 2.0}

class RLCityEngine:
    def __init__(self):
        self.policy = CityPolicy()
        self.builder = RLBuildingEngine()
        self.physics = RLPhysics()
        self.history = []

    def step(self):
        buildings = self.builder.generate(self.policy)
        nodes = self.physics.build_nodes(buildings)
        loads = self.physics.loads(nodes)
        failed = self.physics.collapse(loads)
        self.policy.update(failed)
        stability = max(0, 1 - len(failed) / max(1, len(nodes)))
        reward = stability - 0.3 * len(failed)
        self.history.append(reward)
        return buildings, nodes, loads, failed, stability, reward
