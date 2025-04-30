import pygame
import random
import heapq
import sys

WIDTH, HEIGHT = 300, 300
ROWS, COLS = 3, 3
TILE_SIZE = WIDTH // COLS
FONT_SIZE = 50

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("N-Puzzle Game")
font = pygame.font.Font(None, FONT_SIZE)

# Goal state for comparison [1, 2, 3, 4, 5, 6, 7, 8, 0]
goal_state = list(range(1, ROWS * COLS)) + [0] 

# A* Helper Functions
def manhattan_distance(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile == 0: continue
        target_pos = goal_state.index(tile)
        target_row, target_col = divmod(target_pos, COLS)
        current_row, current_col = divmod(i, COLS)
        distance += abs(target_row - current_row) + abs(target_col - current_col)
    return distance

def is_solvable(puzzle):
    inv_count = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] and puzzle[j] and puzzle[i] > puzzle[j]:
                inv_count += 1
    return inv_count % 2 == 0

def valid_moves(empty_pos):
    row, col = divmod(empty_pos, COLS)
    moves = []
    if row > 0: moves.append(empty_pos - COLS)   
    if row < ROWS - 1: moves.append(empty_pos + COLS) 
    if col > 0: moves.append(empty_pos - 1)   
    if col < COLS - 1: moves.append(empty_pos + 1)  
    return moves

def solve_puzzle(start_state):
    open_list = []
    closed_list = set()
    parent_map = {}  
    g_cost = {tuple(start_state): 0}
    f_cost = {tuple(start_state): manhattan_distance(start_state)}

    heapq.heappush(open_list, (f_cost[tuple(start_state)], tuple(start_state)))

    while open_list:
        _, current_state = heapq.heappop(open_list)
        
        if current_state == tuple(goal_state):
            path = []
            while current_state in parent_map:
                path.append(current_state)
                current_state = parent_map[current_state]
            path.append(tuple(start_state))
            return path[::-1]

        closed_list.add(current_state)

        empty_pos = current_state.index(0)
        for move in valid_moves(empty_pos):
            new_state = list(current_state)
            new_state[empty_pos], new_state[move] = new_state[move], new_state[empty_pos]
            new_state_tuple = tuple(new_state)
            if new_state_tuple in closed_list:
                continue

            tentative_g = g_cost[tuple(current_state)] + 1
            if new_state_tuple not in g_cost or tentative_g < g_cost[new_state_tuple]:
                g_cost[new_state_tuple] = tentative_g
                f = tentative_g + manhattan_distance(new_state)
                f_cost[new_state_tuple] = f
                heapq.heappush(open_list, (f, new_state_tuple))
                parent_map[new_state_tuple] = current_state

    return None  # No solution found

board = list(range(1, ROWS * COLS)) + [0]
random.shuffle(board)
while not is_solvable(board):
    random.shuffle(board)

path_to_solution = solve_puzzle(board)

if not path_to_solution:
    print("No solution found")
    pygame.quit()
    sys.exit()

# Game loop
running = True
step = 0 
interactive_mode = True  

def draw_board(state):
    screen.fill(GRAY)
    for i in range(ROWS * COLS):
        value = state[i]
        x = (i % COLS) * TILE_SIZE
        y = (i // COLS) * TILE_SIZE

        if value == 0:
            pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE))
        else:
            pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)
            text = font.render(str(value), True, BLACK)
            rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
            screen.blit(text, rect)

    pygame.display.flip()

def display_main_menu():
    screen.fill(GRAY)
    title = font.render("N-Puzzle Game", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)

    manual_button = font.render("1. Manual", True, BLACK)
    manual_button_rect = manual_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(manual_button, manual_button_rect)

    auto_button = font.render("2. Auto (A*)", True, BLACK)
    auto_button_rect = auto_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(auto_button, auto_button_rect)

    pygame.display.update()

# Main menu loop
mode_selected = False
while not mode_selected:
    display_main_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if HEIGHT // 2 - FONT_SIZE // 2 < mouse_y < HEIGHT // 2 + FONT_SIZE // 2:
               
                mode_selected = True
                interactive_mode = True
            elif HEIGHT // 2 + 50 - FONT_SIZE // 2 < mouse_y < HEIGHT // 2 + 50 + FONT_SIZE // 2:
                
                mode_selected = True
                interactive_mode = False

# Game loop after mode selection
while running:
    draw_board(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if interactive_mode:
                
                mouse_x, mouse_y = event.pos
                clicked_row = mouse_y // TILE_SIZE
                clicked_col = mouse_x // TILE_SIZE
                clicked_pos = clicked_row * COLS + clicked_col

               
                empty_pos = board.index(0)
                if clicked_pos in valid_moves(empty_pos):
                    board[empty_pos], board[clicked_pos] = board[clicked_pos], board[empty_pos]
                    if board == goal_state:
                        interactive_mode = False  

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                interactive_mode = False

    if not interactive_mode:
       
        if step < len(path_to_solution) - 1:
            step += 1
            board = list(path_to_solution[step]) 
            pygame.time.wait(500)  
        else:
            running = False  # Stop the game after the solution is fully displayed
    pygame.display.update()

pygame.quit()
sys.exit()
