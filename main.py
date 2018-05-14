import mapgenerator.terrain
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d

def main():
    mesh = mapgenerator.terrain.create_mesh(512)
    voronoi_plot_2d(mesh)
    plt.show()

if __name__ == '__main__':
    main()
