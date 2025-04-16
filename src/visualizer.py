import matplotlib.pyplot as plt

def plot_map(ways, path=None):
    plt.figure(figsize=(10, 10))
    
    # Plot all roads
    for road in ways:
        x = [point[0] for point in road]
        y = [point[1] for point in road]
        plt.plot(x, y, 'gray', linewidth=0.5)
    
    # Highlight path
    if path:
        x = [point[0] for point in path]
        y = [point[1] for point in path]
        plt.plot(x, y, 'r-', linewidth=2)
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Dehradun Pathfinding')
    plt.show()
