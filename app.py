import random
import pygame
from queue import PriorityQueue

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)

# Display
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Search Visualization")

# Settings
ROWS = 50
BLOCK_WIDTH = WIDTH // ROWS

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 40
BUTTON_Y = WIDTH + 10
BUTTON_FONT = pygame.font.SysFont("arial", 20)


class Button:
    def __init__(self, x, y, width, height, color, text=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(
                win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4)
            )
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        if self.text:
            font = BUTTON_FONT
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(
                text,
                (
                    self.x + (self.width - text.get_width()) // 2,
                    self.y + (self.height - text.get_height()) // 2,
                ),
            )

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * BLOCK_WIDTH
        self.y = col * BLOCK_WIDTH
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = RED

    def make_end(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = YELLOW

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, BLOCK_WIDTH, BLOCK_WIDTH))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if (
            self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier()
        ):  # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])
        if (
            self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_barrier()
        ):  # Right
            self.neighbors.append(grid[self.row][self.col + 1])


def make_grid(rows, width):
    grid = []
    block_width = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    block_width = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * block_width), (width, i * block_width))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * block_width, 0), (j * block_width, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)

    # Draw buttons here
    reset_button.draw(win, GREY)
    random_fill_button.draw(win, GREY)
    search_button.draw(win, GREY)

    pygame.display.update()


def get_clicked_position(pos, rows, width):
    block_width = width // rows
    y, x = pos
    row = y // block_width
    col = x // block_width
    return row, col


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    global reset_button, random_fill_button, search_button
    reset_button = Button(10, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, ORANGE, "Reset")
    random_fill_button = Button(
        170, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, ORANGE, "Random Fill"
    )
    search_button = Button(330, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, ORANGE, "Search")

    # Adjust the window size for the buttons
    win = pygame.display.set_mode((WIDTH, WIDTH + BUTTON_HEIGHT + 20))

    start = None
    end = None

    manuall_filled = False
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT mouse button
                if reset_button.is_over(pos):
                    # reset the grid
                    start = None
                    end = None
                    manuall_filled = False
                    grid = make_grid(ROWS, width)
                elif random_fill_button.is_over(pos):
                    if manuall_filled:
                        continue
                    # fill a percentage of the grid with barriers randomly
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    for row in grid:
                        for node in row:
                            if (
                                random.random() < 0.3
                            ):  # adjust the value for more or less barriers
                                node.make_barrier()
                elif search_button.is_over(pos):
                    # start the search
                    if start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                        a_star_search(
                            lambda: draw(win, grid, ROWS, width), grid, start, end
                        )
                else:
                    row, col = get_clicked_position(pos, ROWS, width)
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_barrier()
                    manuall_filled = True

            elif pygame.mouse.get_pressed()[2]:  # RIGHT mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)
