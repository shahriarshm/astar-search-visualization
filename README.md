# A* Search Visualization

An interactive visualization tool for the A* pathfinding algorithm built with Python and Pygame.

## Demo
![A* Demo](assets/AStar_Demo.gif)

## Features:

- Interactive grid to set start, end, and barrier nodes.
- A* search visualization.
- Option to reset the grid.
- Option to fill the grid randomly with barriers.
- Clear and simple user interface with buttons.

## Installation:

### Prerequisites:

Make sure you have Python 3.x installed. You'll also need to install `pygame`.

```bash
pip install pygame
```

### Cloning the Repository:

```bash
git clone git@github.com:shahriarshm/astar-search-visualization.git
cd astar-search-visualization
```


## Usage:

Run the main Python script:

```bash
python main.py
```

### Controls:

- **Left Mouse Button**: Click on an empty cell to set the start node (red). Click again to set the end node (blue). Subsequent clicks will create barrier nodes (black).
  
- **Right Mouse Button**: Click on a node to reset it to an empty state.

- **Reset Button**: Resets the entire grid to its initial state.

- **Random Fill Button**: Fills the grid randomly with barriers.

- **Search Button**: Initiates the A* search from the start node to the end node. If a path is found, it's displayed in purple.

## How A* Works:

The A* algorithm finds the shortest path between a start and end node based on two main factors: 

1. **G cost**: The distance from the start node to the current node.
  
2. **H cost (Heuristic)**: The estimated distance from the current node to the end node (often using Manhattan distance as the heuristic).

The algorithm selects the node with the lowest sum of its G and H costs and explores its neighbors. This process is repeated until the end node is reached, ensuring the shortest path is found.

## Contributing:

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License:

[MIT](https://choosealicense.com/licenses/mit/)
