# Conway's Game of Life

This project is a graphical implementation of Conway's Game of Life using Pygame, offering an interactive environment to play, visualize, and explore the behavior of cellular automata according to the iconic rules.

## Interactive Control Dynamics
- **Real-Time Simulation Control**: Easily play or pause the simulation.
- **Cell Interaction**: Click on the grid to add or remove cells.
- **State Management**: Save and load the simulation state at any point.
- **View Customization**: Utilize adjustable zoom and pan for enhanced visualization.
- **Manual Generation Step**: Step through generations manually to observe the evolution of the game world.
- **Environment Reset**: Clear the grid or revert to the last saved state.

## Enhanced Features

- **Efficient Cell Storage**: This implementation adopts a sparse representation for cells, storing only live cell coordinates. This method optimizes memory usage, enabling potentially infinite game worlds within the confines of computer resources.

- **Step-through Debugging**: The "Step Over" feature offers a strategic tool for curious players, enabling them to observe the subsequent state of cells. This functionality serves as a debugging aid, offering insights into the dynamic changes of cell configurations with each generation.

- **Serialization**: This implementation incorporates a thoughtful serialization approach that efficiently captures and preserves the current state of the game world, including the living cells and viewport settings. By clicking the save button, players can effortlessly save the entire state of the game, ensuring that when they return, they can pick up exactly where they left off, with the viewport and all game elements intact. This feature is designed to provide a seamless transition between sessions.

- **Optimized Rendering with Infinite Exploration**: Despite the potentially vast size of the world, the game engine smartly renders only the visible portion of the viewport. This optimization ensures efficient performance while allowing the game to run in the background. The gameplay experience is enhanced with intuitive panning and zooming functionalities, reminiscent of navigating through Google Maps. Unfortunately, Street View is not available —though hopefully you will enjoy exploring the cellular cosmos just as much!

  To mimic the dynamic zoom functionality akin to Google Maps, the game seamlessly integrates the real mouse position with its game world equivalent. This integration focuses on maintaining the pointer-centered zoom, requiring calculations to adjust the camera position according to the new view scale. <br /> Let's denote the initial screen position of the pointer as $(mouse\_x, mouse\_y)$, and the analogous game world positions as $(mouse\_u, mouse\_v)$, with the zoom factor and camera position represented by $viewscale$ and $(camera\_x, camera\_y)$, respectively. During zooming, centered on the pointer, $(mouse\_x, mouse\_y)$ and $(mouse\_u, mouse\_v)$ remain constant, while $viewscale$ changes to $viewscale'$. The objective is to calculate the new camera position, $(camera\_x', camera\_y')$, to keep the focus unchanged in the game world.

  Given the relationship:<br />

  $mouse\_u = \frac{(mouse\_x - camera\_x)}{viewscale}$ <br />

  $mouse\_v = \frac{(mouse\_y - camera\_y)}{viewscale}$
  <br><br>

  For the updated state:

  $mouse\_u' = \frac{(mouse\_x - camera\_x')}{viewscale'}$ <br />

  $mouse\_v' = \frac{(mouse\_y - camera\_y')}{viewscale'}$ <br />
  <br>

  Since $mouse\_u = mouse\_u'$ and $mouse\_v = mouse\_v'$ due to the zoom action being centered on the pointer, and knowing the new    $viewscale'$, the new camera positions can be deduced:

  $camera\_x' = mouse\_x - viewscale' \cdot mouse\_u$ <br />
  $camera\_x' = mouse\_x - (mouse\_x - camera\_x) \cdot \frac{viewscale'}{viewscale}$ <br />
  <br>

  Similarly, for $camera\_y'$: <br />
  $camera\_y' = mouse\_y - (mouse\_y - camera\_y) \cdot \frac{viewscale'}{viewscale}$ <br />
  <br><br>
  This mathematical approach ensures intuitive and cursor-centered zooming, enhancing the navigation experience.



## Installation

To run this project, you will need Python 3 and Pygame installed on your system.

1. Clone the repository to your local machine:<br />
`git clone <git@github.com:larissapoghosyan/gameoflife.git>`
2. Install Pygame if you haven't already:<br />
`pip install pygame`

## Usage

To start the game, navigate to the project directory in your terminal and run:<br />
`python main.py`
