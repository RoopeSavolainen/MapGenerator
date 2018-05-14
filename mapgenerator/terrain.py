import random
from datetime import datetime

import numpy as np
import scipy.spatial

import matplotlib.pyplot as plt

BLUE_NOISE_CANDIDATES = 4

def _sample_blue_noise(P, w=1.0, h=1.0):
    def dist(a,b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2

    candidates = []
    for i in range(BLUE_NOISE_CANDIDATES):
        candidates.append([random.uniform(0.0, w), random.uniform(0.0, h)])
    best = max(candidates, key=lambda p: 0.0 if P.size==0 else dist(p, min(P, key=lambda o: dist(p,o))))
    return np.append(P, [best], axis=0)

def _create_grid(n):
    P = np.empty([0,2])
    for i in range(n):
        P = _sample_blue_noise(P)
    return P

def create_mesh(n, relaxations=0):
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
    return mesh
