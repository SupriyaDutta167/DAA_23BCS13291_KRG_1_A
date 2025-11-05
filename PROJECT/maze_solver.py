import pygame
import math
from queue import PriorityQueue, Queue
import sys
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions - now resizable
WIDTH = 1400
HEIGHT = 900
ROWS = 50
COLS = 50

# These will be recalculated on resize
CELL_SIZE = 14
HEADER_HEIGHT = 80
PANEL_WIDTH = 350
PANEL_X_START = WIDTH - PANEL_WIDTH
MAZE_WIDTH = COLS * CELL_SIZE
MAZE_HEIGHT = ROWS * CELL_SIZE
MAZE_OFFSET_X = (PANEL_X_START - MAZE_WIDTH) // 2
MAZE_OFFSET_Y = HEADER_HEIGHT + (HEIGHT - HEADER_HEIGHT - MAZE_HEIGHT) // 2

# Modern color palette
COLORS = {
    'bg': (15, 23, 42),
    'surface': (30, 41, 59),
    'surface_light': (51, 65, 85),
    'surface_dark': (23, 31, 46),
    'primary': (59, 130, 246),
    'primary_dark': (37, 99, 235),
    'success': (34, 197, 94),
    'success_dark': (22, 163, 74),
    'danger': (239, 68, 68),
    'danger_dark': (220, 38, 38),
    'warning': (245, 158, 11),
    'warning_dark': (217, 119, 6),
    'purple': (168, 85, 247),
    'purple_dark': (147, 51, 234),
    'text': (241, 245, 249),
    'text_dim': (148, 163, 184),
    'text_header': (226, 232, 240),
    'wall': (71, 85, 105),
    'visited': (239, 68, 68, 100),
    'frontier': (59, 130, 246, 120),
    'path': (168, 85, 247),
    'start': (34, 197, 94),
    'end': (245, 158, 11),
    'shadow': (10, 15, 32, 100)
}

# Pygame screen - now resizable
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Maze Solver Pro - Pathfinding Visualizer")

# Fonts
try:
    FONT_SANS = 'Segoe UI'
    FONT_SANS_BOLD = 'Segoe UI'
    pygame.font.SysFont(FONT_SANS, 16)
except:
    FONT_SANS = 'Arial'
    FONT_SANS_BOLD = 'Arial'


# =================== UTILITY FUNCTIONS FOR RESIZING ===================
def recalculate_dimensions(width, height):
    """Recalculate all dimension-dependent variables based on new window size"""
    global WIDTH, HEIGHT, CELL_SIZE, HEADER_HEIGHT, PANEL_WIDTH, PANEL_X_START
    global MAZE_WIDTH, MAZE_HEIGHT, MAZE_OFFSET_X, MAZE_OFFSET_Y
    
    WIDTH = width
    HEIGHT = height
    
    # Maintain proportions
    HEADER_HEIGHT = max(60, int(height * 0.089))  # ~80 for 900px height
    PANEL_WIDTH = max(250, int(width * 0.25))  # ~350 for 1400px width
    PANEL_X_START = WIDTH - PANEL_WIDTH
    
    # Calculate cell size to fit the maze in available space
    available_width = PANEL_X_START - 100  # Some padding
    available_height = HEIGHT - HEADER_HEIGHT - 100
    
    cell_width = available_width // COLS
    cell_height = available_height // ROWS
    CELL_SIZE = max(8, min(cell_width, cell_height))  # Min 8px, maintain square cells
    
    MAZE_WIDTH = COLS * CELL_SIZE
    MAZE_HEIGHT = ROWS * CELL_SIZE
    MAZE_OFFSET_X = (PANEL_X_START - MAZE_WIDTH) // 2
    MAZE_OFFSET_Y = HEADER_HEIGHT + (HEIGHT - HEADER_HEIGHT - MAZE_HEIGHT) // 2

def update_node_positions(grid):
    """Update the pixel positions of all nodes after window resize"""
    for row in grid:
        for node in row:
            node.x = MAZE_OFFSET_X + node.col * CELL_SIZE
            node.y = MAZE_OFFSET_Y + node.row * CELL_SIZE

def create_buttons():
    """Create buttons based on current window dimensions"""
    button_y = HEIGHT - 65
    btn_width = max(90, int((PANEL_X_START - 100) / 6.5))
    btn_height = 40
    btn_gap = 20
    btn_start_x = 50
    
    buttons = [
        Button(btn_start_x, button_y, btn_width, btn_height, 'BFS (B)', COLORS['primary'], COLORS['primary_dark']),
        Button(btn_start_x + (btn_width + btn_gap), button_y, btn_width, btn_height, 'DFS (D)', COLORS['primary'], COLORS['primary_dark']),
        Button(btn_start_x + 2*(btn_width + btn_gap), button_y, btn_width, btn_height, 'Dijkstra (J)', COLORS['primary'], COLORS['primary_dark']),
        Button(btn_start_x + 3*(btn_width + btn_gap), button_y, btn_width, btn_height, 'A* (A)', COLORS['success'], COLORS['success_dark']),
        Button(btn_start_x + 4*(btn_width + btn_gap), button_y, int(btn_width * 1.3), btn_height, 'Random Maze (R)', COLORS['warning'], COLORS['warning_dark']),
        Button(btn_start_x + 5*(btn_width + btn_gap) + 30, button_y, int(btn_width * 1.1), btn_height, 'Clear All (C)', COLORS['danger'], COLORS['danger_dark']),
    ]
    
    win_btn_size = 25
    win_btn_y = (HEADER_HEIGHT - win_btn_size) // 2
    window_buttons = [
        Button(WIDTH - 45, win_btn_y, win_btn_size, win_btn_size, 'X', COLORS['danger'], COLORS['danger_dark'], font_size=12, border_radius=6),
        Button(WIDTH - 80, win_btn_y, win_btn_size, win_btn_size, '_', COLORS['warning'], COLORS['warning_dark'], font_size=12, border_radius=6),
    ]
    
    return buttons, window_buttons


# =================== BUTTON CLASS ===================
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=COLORS['text'], font_size=14, bold=True, border_radius=8):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.SysFont(FONT_SANS_BOLD if bold else FONT_SANS, font_size, bold=bold)
        self.border_radius = border_radius
        
    def draw(self, win):
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(win, COLORS['shadow'], shadow_rect, border_radius=self.border_radius)
        
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(win, color, self.rect, border_radius=self.border_radius)
        
        pygame.draw.rect(win, COLORS['surface_light'], self.rect, 1, border_radius=self.border_radius)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False

# =================== NODE CLASS ===================
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = MAZE_OFFSET_X + col * CELL_SIZE
        self.y = MAZE_OFFSET_Y + row * CELL_SIZE
        self.color = (60, 75, 90)
        self.neighbors = []
        self.distance = math.inf
        self.g_score = math.inf
        self.f_score = math.inf

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == COLORS['visited']

    def is_open(self):
        return self.color == COLORS['frontier']

    def is_barrier(self):
        return self.color == COLORS['wall']

    def is_start(self):
        return self.color == COLORS['start']

    def is_end(self):
        return self.color == COLORS['end']

    def reset(self):
        self.color = COLORS['surface']

    def make_start(self):
        self.color = COLORS['start']

    def make_closed(self):
        self.color = COLORS['visited']

    def make_open(self):
        self.color = COLORS['frontier']

    def make_barrier(self):
        self.color = COLORS['wall']

    def make_end(self):
        self.color = COLORS['end']

    def make_path(self):
        self.color = COLORS['path']

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < COLS - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

# =================== UTILITY FUNCTIONS ===================
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw, metrics):
    path_length = 0
    path_nodes = []
    while current in came_from:
        current = came_from[current]
        path_nodes.append(current)
        path_length += 1
    
    for node in reversed(path_nodes):
        if not node.is_start():
            node.make_path()
            draw()
            pygame.time.delay(10)
    
    metrics['path_length'] = path_length

def generate_random_maze(grid, density=0.3):
    count = 0
    for row in grid:
        for node in row:
            if random.random() < density:
                node.make_barrier()
                count += 1
    return count

def get_grid_stats(grid):
    obstacles = 0
    for row in grid:
        for node in row:
            if node.is_barrier():
                obstacles += 1
    return {
        'grid_size': f"{ROWS} x {COLS}",
        'obstacles': obstacles
    }

# =================== ALGORITHMS ===================
def bfs(draw, grid, start, end, metrics):
    queue = Queue()
    queue.put(start)
    came_from = {}
    visited = {start}
    count_nodes = 0
    start_time = time.time()

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = queue.get()
        count_nodes += 1

        if current == end:
            reconstruct_path(came_from, end, draw, metrics)
            end.make_end()
            start.make_start()
            metrics['nodes_explored'] = count_nodes
            metrics['time'] = time.time() - start_time
            metrics['algorithm'] = 'Breadth-First Search'
            metrics['complexity'] = 'O(V + E)'
            metrics['optimal'] = 'Yes (unweighted)'
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.put(neighbor)
                if not neighbor.is_end():
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    metrics['nodes_explored'] = count_nodes
    metrics['time'] = time.time() - start_time
    metrics['algorithm'] = 'Breadth-First Search'
    return False

def dfs(draw, grid, start, end, metrics):
    stack = [start]
    came_from = {}
    visited = {start}
    count_nodes = 0
    start_time = time.time()

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = stack.pop()
        count_nodes += 1

        if current == end:
            reconstruct_path(came_from, end, draw, metrics)
            end.make_end()
            start.make_start()
            metrics['nodes_explored'] = count_nodes
            metrics['time'] = time.time() - start_time
            metrics['algorithm'] = 'Depth-First Search'
            metrics['complexity'] = 'O(V + E)'
            metrics['optimal'] = 'No'
            return True

        # ✅ PRIORITIZE NEIGHBORS CLOSER TO END
        neighbors = sorted(
            current.neighbors,
            key=lambda node: abs(node.row - end.row) + abs(node.col - end.col)
        )

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)

                if not neighbor.is_end():
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    metrics['nodes_explored'] = count_nodes
    metrics['time'] = time.time() - start_time
    metrics['algorithm'] = 'Depth-First Search'
    return False


def dijkstra(draw, grid, start, end, metrics):
    count = 0
    pq = PriorityQueue()
    start.distance = 0
    pq.put((0, count, start))
    came_from = {}
    visited = set()
    count_nodes = 0
    start_time = time.time()

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = pq.get()[2]
        
        if current in visited:
            continue
            
        count_nodes += 1
        visited.add(current)

        if current == end:
            reconstruct_path(came_from, end, draw, metrics)
            end.make_end()
            start.make_start()
            metrics['nodes_explored'] = count_nodes
            metrics['time'] = time.time() - start_time
            metrics['algorithm'] = "Dijkstra's Algorithm"
            metrics['complexity'] = 'O((V+E)logV)'
            metrics['optimal'] = 'Yes (weighted)'
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                temp_dist = current.distance + 1
                if temp_dist < neighbor.distance:
                    neighbor.distance = temp_dist
                    came_from[neighbor] = current
                    count += 1
                    pq.put((neighbor.distance, count, neighbor))
                    if not neighbor.is_end():
                        neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    metrics['nodes_explored'] = count_nodes
    metrics['time'] = time.time() - start_time
    metrics['algorithm'] = "Dijkstra's Algorithm"
    return False

def a_star(draw, grid, start, end, metrics):
    count = 0
    open_set = PriorityQueue()
    start.g_score = 0
    start.f_score = h(start.get_pos(), end.get_pos())
    open_set.put((start.f_score, count, start))
    came_from = {}
    open_set_hash = {start}
    count_nodes = 0
    start_time = time.time()

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        count_nodes += 1

        if current == end:
            reconstruct_path(came_from, end, draw, metrics)
            end.make_end()
            start.make_start()
            metrics['nodes_explored'] = count_nodes
            metrics['time'] = time.time() - start_time
            metrics['algorithm'] = 'A* Search'
            metrics['complexity'] = 'O(b^d)'
            metrics['optimal'] = 'Yes (heuristic)'
            return True

        for neighbor in current.neighbors:
            temp_g_score = current.g_score + 1

            if temp_g_score < neighbor.g_score:
                came_from[neighbor] = current
                neighbor.g_score = temp_g_score
                neighbor.f_score = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((neighbor.f_score, count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_end():
                        neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    metrics['nodes_explored'] = count_nodes
    metrics['time'] = time.time() - start_time
    metrics['algorithm'] = 'A* Search'
    return False

# =================== UI DRAWING ===================
def draw_header(win, buttons):
    pygame.draw.rect(win, COLORS['surface'], (0, 0, WIDTH, HEADER_HEIGHT))
    
    title_font = pygame.font.SysFont(FONT_SANS_BOLD, 32, bold=True)
    title = title_font.render('Maze Solver Pro', True, COLORS['text_header'])
    win.blit(title, (20, 16))
    
    subtitle_font = pygame.font.SysFont(FONT_SANS, 14)
    subtitle = subtitle_font.render('Pathfinding Algorithm Visualizer', True, COLORS['text_dim'])
    win.blit(subtitle, (20, 52))
    
    for button in buttons:
        button.draw(win)

def draw_metric_card(win, x, y, width, height, label, value):
    card_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(win, COLORS['surface_dark'], card_rect, border_radius=10)
    pygame.draw.rect(win, COLORS['surface_light'], card_rect, 1, border_radius=10)
    
    font_label = pygame.font.SysFont(FONT_SANS, 13)
    label_surface = font_label.render(label, True, COLORS['text_dim'])
    win.blit(label_surface, (x + 15, y + 12))
    
    font_value = pygame.font.SysFont(FONT_SANS_BOLD, 20, bold=True)
    value_surface = font_value.render(str(value), True, COLORS['text'])
    win.blit(value_surface, (x + 15, y + 32))

def draw_side_panel(win, metrics):
    pygame.draw.rect(win, COLORS['surface'], (PANEL_X_START, 0, PANEL_WIDTH, HEIGHT))
    
    font_title = pygame.font.SysFont(FONT_SANS_BOLD, 20, bold=True)
    font_normal = pygame.font.SysFont(FONT_SANS, 14)
    
    y_offset = HEADER_HEIGHT + 30
    
    title = font_title.render('Performance Metrics', True, COLORS['text_header'])
    win.blit(title, (PANEL_X_START + 25, y_offset))
    y_offset += 50
    
    card_width = (PANEL_WIDTH - 75) // 2
    card_height = 80
    
    metric_items = [
        ('Algorithm', metrics.get('algorithm', 'N/A')),
        ('Time', f"{metrics.get('time', 0):.4f} s"),
        ('Nodes Explored', str(metrics.get('nodes_explored', 0))),
        ('Path Length', str(metrics.get('path_length', 0))),
        ('Grid Size', metrics.get('grid_size', 'N/A')),
        ('Obstacles', str(metrics.get('obstacles', 0))),
        ('Complexity', metrics.get('complexity', 'N/A')),
        ('Optimal Path', metrics.get('optimal', 'N/A')),
    ]
    
    for i, (label, value) in enumerate(metric_items):
        col = i % 2
        row = i // 2
        x = PANEL_X_START + 25 + (card_width + 25) * col
        y = y_offset + (card_height + 20) * row
        draw_metric_card(win, x, y, card_width, card_height, label, value)

    y_offset += (len(metric_items) + 1) // 2 * (card_height + 20)
    
    y_offset = max(y_offset, HEIGHT - 280)
    legend_title = font_title.render('Legend', True, COLORS['text_header'])
    win.blit(legend_title, (PANEL_X_START + 25, y_offset))
    y_offset += 40
    
    legend_items = [
        (COLORS['start'], 'Start Node'),
        (COLORS['end'], 'End Node'),
        (COLORS['wall'], 'Wall / Obstacle'),
        (COLORS['frontier'], 'Frontier Node'),
        ((75, 85, 99), 'Visited Node'),
        (COLORS['path'], 'Final Path'),
    ]
    
    for color, text in legend_items:
        pygame.draw.rect(win, color, (PANEL_X_START + 25, y_offset, 20, 20), border_radius=5)
        label = font_normal.render(text, True, COLORS['text'])
        win.blit(label, (PANEL_X_START + 55, y_offset + 1))
        y_offset += 35

def draw_grid(win):
    pygame.draw.rect(win, (30, 40, 60), (MAZE_OFFSET_X, MAZE_OFFSET_Y, MAZE_WIDTH, MAZE_HEIGHT))
    
    for i in range(ROWS + 1):
        pygame.draw.line(win, COLORS['surface_light'], 
                         (MAZE_OFFSET_X, MAZE_OFFSET_Y + i * CELL_SIZE), 
                         (MAZE_OFFSET_X + MAZE_WIDTH, MAZE_OFFSET_Y + i * CELL_SIZE), 1)
    for j in range(COLS + 1):
        pygame.draw.line(win, COLORS['surface_light'], 
                         (MAZE_OFFSET_X + j * CELL_SIZE, MAZE_OFFSET_Y), 
                         (MAZE_OFFSET_X + j * CELL_SIZE, MAZE_OFFSET_Y + MAZE_HEIGHT), 1)

def draw(win, grid, algo_buttons, window_buttons, metrics):
    win.fill(COLORS['bg'])
    
    draw_side_panel(win, metrics)
    draw_header(win, window_buttons)
    draw_grid(win)
    
    for row in grid:
        for node in row:
            node.draw(win)
    
    for button in algo_buttons:
        button.draw(win)
    
    pygame.display.update()

def get_clicked_pos(pos):
    x, y = pos
    if not (MAZE_OFFSET_X <= x < MAZE_OFFSET_X + MAZE_WIDTH and 
            MAZE_OFFSET_Y <= y < MAZE_OFFSET_Y + MAZE_HEIGHT):
        return None, None
    
    col = (x - MAZE_OFFSET_X) // CELL_SIZE
    row = (y - MAZE_OFFSET_Y) // CELL_SIZE
    
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    
    return None, None

def make_grid():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            node = Node(i, j)
            grid[i].append(node)
    return grid

def clear_path(grid):
    for row in grid:
        for node in row:
            if node.is_open() or node.is_closed() or node.color == COLORS['path']:
                node.reset()
            node.distance = math.inf
            node.g_score = math.inf
            node.f_score = math.inf

# =================== MAIN LOOP ===================
def main(win):
    grid = make_grid()
    start = None
    end = None
    metrics = get_grid_stats(grid)
    
    buttons, window_buttons = create_buttons()
    
    run = True
    drawing = False
    clock = pygame.time.Clock()

    while run:
        draw(win, grid, buttons, window_buttons, metrics)
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # Handle window resize
            if event.type == pygame.VIDEORESIZE:
                recalculate_dimensions(event.w, event.h)
                win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                update_node_positions(grid)
                buttons, window_buttons = create_buttons()
            
            if window_buttons[0].handle_event(event):
                run = False
            if window_buttons[1].handle_event(event):
                pygame.display.iconify()

            for i, button in enumerate(buttons):
                if button.handle_event(event):
                    if i < 4 and start and end:
                        clear_path(grid)
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                        
                        metrics = get_grid_stats(grid) 
                        
                        if i == 0:
                            bfs(lambda: draw(win, grid, buttons, window_buttons, metrics), grid, start, end, metrics)
                        elif i == 1:
                            dfs(lambda: draw(win, grid, buttons, window_buttons, metrics), grid, start, end, metrics)
                        elif i == 2:
                            dijkstra(lambda: draw(win, grid, buttons, window_buttons, metrics), grid, start, end, metrics)
                        elif i == 3:
                            a_star(lambda: draw(win, grid, buttons, window_buttons, metrics), grid, start, end, metrics)
                        
                        start.make_start()
                        end.make_end()

                    elif i == 4:
                        start = None
                        end = None
                        grid = make_grid()
                        obstacle_count = generate_random_maze(grid, 0.25)
                        metrics = get_grid_stats(grid)
                        
                    elif i == 5:
                        start = None
                        end = None
                        grid = make_grid()
                        metrics = get_grid_stats(grid)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if not any(b.rect.collidepoint(pos) for b in buttons) and \
                       not any(b.rect.collidepoint(pos) for b in window_buttons):
                        drawing = True
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            
            if event.type == pygame.MOUSEMOTION and drawing:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                if row is not None and col is not None:
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_barrier()
                        metrics = get_grid_stats(grid)

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                if row is not None and col is not None:
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None
                    metrics = get_grid_stats(grid)

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_b or event.key == pygame.K_d or \
                    event.key == pygame.K_j or event.key == pygame.K_a) and start and end:
                    
                    clear_path(grid)
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    metrics = get_grid_stats(grid)

                    if event.key == pygame.K_b:
                        bfs(lambda: draw(win, grid, buttons, window_buttons, metrics), grid, start, end, metrics)
                    if event.key == pygame.K_d:
                        dfs(lambda: draw(win, grid, buttons, window_buttons, metrics), grid, start, end, metrics)
                    if event.key == pygame.K_j:
                        dijkstra(lambda: draw(win, grid, buttons, window_buttons, metrics), grid, start, end, metrics)
                    if event.key == pygame.K_a:
                        a_star(lambda: draw(win, grid, buttons, window_buttons, metrics), grid, start, end, metrics)
                    
                    start.make_start()
                    end.make_end()

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid()
                    obstacle_count = generate_random_maze(grid, 0.25)
                    metrics = get_grid_stats(grid)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid()
                    metrics = get_grid_stats(grid)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main(WIN)