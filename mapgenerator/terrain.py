import random
from time import time

import numpy as np
import scipy.spatial

from noise import snoise2

BLUE_NOISE_CANDIDATES = 4
OCTAVES = 8
PERSISTENCE = 0.5
LACUNARITY = 2.0


def _sample_blue_noise(P, w=1.0, h=1.0):
    def dist(a,b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2

    candidates = []
    for i in range(BLUE_NOISE_CANDIDATES):
        candidates.append([random.uniform(0.0, w), random.uniform(0.0, h)])
    best = max(candidates, key=lambda p: 0.0 if P.size==0 else dist(p, min(P, key=lambda o: dist(p,o))))
    return np.append(P, [best], axis=0)


def _create_grid( n):
    P = np.empty([0,2])
    for i in range(n):
        P = _sample_blue_noise(P)
    return P


class Terrain:

    def __init__(self, n, relaxations=0, seed=None):
        self.seed = seed if seed is not None else time() % 1000000
        random.seed(self.seed)

        self.heights = []

        self.generate_mesh(n, relaxations)
        self.generate_heightmap()


    def generate_mesh(self, n, relaxations):
        points = _create_grid(n)

        for i in range(relaxations+1):
            mesh = scipy.spatial.Voronoi(points)
            points = []
            for r in mesh.regions:
                if len(r) > 0:
                    valid = filter(lambda x: x >= 0
                            and 0.0 <= mesh.vertices[x][0] <= 1.0
                            and 0.0 <= mesh.vertices[x][1] <= 1.0, r)
                    corners = list(map(lambda x: mesh.vertices[x], valid))
                    mid = sum(corners)/len(corners)
                    points.append(mid)
        self.mesh = mesh


    def generate_heightmap(self):
        for i in range(len(self.mesh.points)):
            p = self.mesh.points[i]
            height = snoise2(p[0], p[1], base=self.seed, octaves=OCTAVES, persistence=PERSISTENCE, lacunarity=LACUNARITY)
            self.heights.append((i, height))

