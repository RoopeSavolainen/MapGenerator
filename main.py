import mapgenerator.terrain
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import voronoi_plot_2d

def _draw_voronoi(terrain):
    fig = plt.figure()
    voronoi_plot_2d(terrain.mesh)
    plt.show()


def _draw_heights(terrain):
    fig = plt.figure()
    #voronoi_plot_2d(terrain.mesh)
    ax = fig.add_subplot(111, projection='3d')

    val = list(map(lambda h:
        (terrain.mesh.points[h[0]][0],
            terrain.mesh.points[h[0]][1],
            h[1])
        , terrain.heights))

    above = filter(lambda v: v[2] > 0.0, val)
    under = filter(lambda v: v[2] < 0.0, val)

    above_coord = list(zip(*above))
    under_coord = list(zip(*under))

    ax.scatter(above_coord[0], above_coord[1], above_coord[2], marker='.', c='g')
    ax.scatter(under_coord[0], under_coord[1], under_coord[2], marker='.', c='b')

    plt.show()


def main():
    terrain = mapgenerator.terrain.Terrain(1024, relaxations=1)
    _draw_heights(terrain)

if __name__ == '__main__':
    main()

