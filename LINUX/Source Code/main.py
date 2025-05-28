import pygame
import random
import sys
import os
import math
from typing import List, Tuple
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850
SNAKE_SIZE = 20
FOOD_SIZE = 15
GRID_SIZE = SNAKE_SIZE  # Use snake size as grid size
GRID_WIDTH = int(WINDOW_WIDTH // GRID_SIZE)
GRID_HEIGHT = int(WINDOW_HEIGHT // GRID_SIZE)
BOUNDARY_THICKNESS = 0.25  # Keep the thin boundary

# Reserve top area for UI (score, level, etc.)
UI_HEIGHT = 40  # pixels
PLAY_AREA_HEIGHT = WINDOW_HEIGHT - UI_HEIGHT
GRID_HEIGHT_PLAYABLE = PLAY_AREA_HEIGHT // GRID_SIZE

# Menu settings
MENU_SPACING = 100  # Space between menu items
MENU_ITEM_HEIGHT = 60  # Height of each menu item

# Title Animation Settings
TITLE_FONT_SIZE = 120
SNAKE_SEGMENTS = 15  # Increased segments for smoother animation
SNAKE_RADIUS = 130  # Radius of the figure-8 pattern
SNAKE_SPEED = 1.5  # Adjusted speed for smoother movement
PULSE_SPEED = 0.05  # Speed of the pulsing effect

# Game settings
class Level(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

# Colors for UI and backgrounds
UI_COLORS = {
    Level.EASY: {
        'background': (10, 10, 30),      # Dark blue-black background
        'ui_background': (30, 30, 60),   # Dark blue-purple UI
        'text': (200, 255, 200),         # Light green text
        'boundary': (150, 255, 150)      # Green boundary
    },
    Level.MEDIUM: {
        'background': (10, 10, 30),      # Dark blue-black background
        'ui_background': (30, 30, 60),   # Dark blue-purple UI
        'text': (255, 200, 150),         # Light orange text
        'boundary': (255, 150, 0)        # Orange boundary
    },
    Level.HARD: {
        'background': (10, 10, 30),      # Dark blue-black background
        'ui_background': (30, 30, 60),   # Dark blue-purple UI
        'text': (255, 255, 255),         # White text
        'boundary': (0, 255, 255)        # Cyan boundary
    }
}

# Game speeds for different levels
SPEED_EASY = 10
SPEED_MEDIUM = 8
SPEED_HARD = 10

# UI Elements
class Button:
    def __init__(self, x, y, width, height, text, font_size=36, level=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.level = level
        self.hovered = False

    def draw(self, surface, current_level):
        colors = UI_COLORS[current_level]
        color = (min(255, colors['ui_background'][0] + 50),
                min(255, colors['ui_background'][1] + 50),
                min(255, colors['ui_background'][2] + 50)) if self.hovered else colors['ui_background']
        pygame.draw.rect(surface, color, self.rect)
        
        # Use white color for button outline and text
        WHITE = (255, 255, 255)
        pygame.draw.rect(surface, WHITE, self.rect, 1)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Snake:
    def __init__(self, level: Level):
        self.length = 1
        start_x = GRID_WIDTH // 4
        start_y = (GRID_HEIGHT_PLAYABLE // 2) + (UI_HEIGHT // GRID_SIZE)
        if level in [Level.MEDIUM, Level.HARD]:
            start_x = max(int(BOUNDARY_THICKNESS + 1), start_x)
            start_y = max(int((UI_HEIGHT // GRID_SIZE) + BOUNDARY_THICKNESS + 1), start_y)
        self.positions = [(start_x, start_y)]
        self.direction = (1, 0)  # Start moving right
        self.score = 0
        self.level = level
        # Define snake colors based on level
        if level == Level.EASY:
            self.head_color = (50, 205, 50)     # Limegreen
            self.body_color = (34, 139, 34)     # Darker green
        elif level == Level.MEDIUM:
            self.head_color = (255, 165, 0)     # Orange
            self.body_color = (255, 140, 0)     # Darker orange
        else:  # HARD
            self.head_color = (0, 255, 200)     # Neon cyan
            self.body_color = (0, 200, 160)     # Darker cyan

    def get_head_position(self) -> Tuple[int, int]:
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)

        # Check UI area collision
        if new[1] < UI_HEIGHT // GRID_SIZE:
            return False

        # Check boundary collision for Medium and Hard levels
        if self.level in [Level.MEDIUM, Level.HARD]:
            # Add a small buffer to boundary collision to prevent clipping
            buffer = 0.1
            if (new[0] < BOUNDARY_THICKNESS + buffer or 
                new[0] >= GRID_WIDTH - (BOUNDARY_THICKNESS + buffer) or 
                new[1] < (UI_HEIGHT // GRID_SIZE) + BOUNDARY_THICKNESS + buffer or 
                new[1] >= GRID_HEIGHT - (BOUNDARY_THICKNESS + buffer)):
                return False
        else:
            # Wrap around for Easy level, but respect UI area
            new = (new[0] % GRID_WIDTH, 
                   max(UI_HEIGHT // GRID_SIZE, 
                       ((new[1] - (UI_HEIGHT // GRID_SIZE)) % (GRID_HEIGHT - (UI_HEIGHT // GRID_SIZE))) + (UI_HEIGHT // GRID_SIZE)))

        if new in self.positions[3:]:  # Snake collides with itself
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        # Adjust reset position to account for boundary thickness
        start_x = GRID_WIDTH // 4
        start_y = (GRID_HEIGHT_PLAYABLE // 2) + (UI_HEIGHT // GRID_SIZE)
        if self.level in [Level.MEDIUM, Level.HARD]:
            start_x = max(int(BOUNDARY_THICKNESS + 1), start_x)
            start_y = max(int((UI_HEIGHT // GRID_SIZE) + BOUNDARY_THICKNESS + 1), start_y)
        self.length = 1
        self.positions = [(start_x, start_y)]
        self.direction = (1, 0)
        self.score = 0

    def render(self, surface):
        for i, p in enumerate(self.positions):
            color = self.head_color if i == 0 else self.body_color
            # Center the snake segments in their grid cells
            x = p[0] * GRID_SIZE + (GRID_SIZE - SNAKE_SIZE) // 2
            y = p[1] * GRID_SIZE + (GRID_SIZE - SNAKE_SIZE) // 2
            r = pygame.Rect(x, y, SNAKE_SIZE, SNAKE_SIZE)
            pygame.draw.rect(surface, color, r)
            pygame.draw.rect(surface, UI_COLORS[self.level]['text'], r, 1)

class Food:
    def __init__(self, level: Level):
        self.position = (0, 0)
        self.level = level
        self.food_color = (255, 0, 0)  # Bright red color for food
        self.randomize_position()

    def randomize_position(self):
        # Add buffer to prevent food spawning too close to boundaries
        buffer = 1
        if self.level in [Level.MEDIUM, Level.HARD]:
            min_x = int(BOUNDARY_THICKNESS + buffer)
            max_x = int(GRID_WIDTH - BOUNDARY_THICKNESS - buffer)
            min_y = int((UI_HEIGHT // GRID_SIZE) + BOUNDARY_THICKNESS + buffer)
            max_y = int(GRID_HEIGHT - BOUNDARY_THICKNESS - buffer)
        else:
            min_x = 0
            max_x = GRID_WIDTH - 1
            min_y = UI_HEIGHT // GRID_SIZE
            max_y = GRID_HEIGHT - 1

        # Ensure we have valid ranges
        max_x = max(min_x, max_x)
        max_y = max(min_y, max_y)

        self.position = (
            random.randint(min_x, max_x),
            random.randint(min_y, max_y)
        )

    def render(self, surface):
        # Center the food in its grid cell
        x = self.position[0] * GRID_SIZE + (GRID_SIZE - FOOD_SIZE) // 2
        y = self.position[1] * GRID_SIZE + (GRID_SIZE - FOOD_SIZE) // 2
        r = pygame.Rect(x, y, FOOD_SIZE, FOOD_SIZE)
        pygame.draw.rect(surface, self.food_color, r)  # Use the red color for food
        pygame.draw.rect(surface, UI_COLORS[self.level]['text'], r, 1)  # Keep the outline using theme color

    def get_collision_rect(self):
        # Return the actual rect used for collision detection
        x = self.position[0] * GRID_SIZE + (GRID_SIZE - FOOD_SIZE) // 2
        y = self.position[1] * GRID_SIZE + (GRID_SIZE - FOOD_SIZE) // 2
        return pygame.Rect(x, y, FOOD_SIZE, FOOD_SIZE)

def draw_menu(screen):
    # Use EASY theme colors for menu background
    colors = UI_COLORS[Level.EASY]
    screen.fill(colors['background'])
    font = pygame.font.Font(None, 74)
    
    # Define menu colors that will match snake colors
    MENU_COLORS = {
        'Easy': (50, 205, 50),     # Limegreen
        'Medium': (255, 165, 0),   # Orange
        'Hard': (0, 255, 200),      # Neon cyan
        'hover_outline': (255, 255, 255),  # White outline for hover effect
        'click_fill': (240, 240, 240, 128)  # Dusty white with transparency for click effect
    }
    
    # Create all text surfaces first
    title_text = font.render('Choose LEVEL', True, colors['text'])
    easy_text = font.render('Easy', True, MENU_COLORS['Easy'])
    medium_text = font.render('Medium', True, MENU_COLORS['Medium'])
    hard_text = font.render('Hard', True, MENU_COLORS['Hard'])

    # Calculate total menu height
    total_height = MENU_ITEM_HEIGHT * 4  # Title + 3 options
    start_y = (WINDOW_HEIGHT - total_height) // 2  # Center vertically

    # Create rectangles for menu items with padding
    padding = 20  # Padding around text for hover/click effects
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, start_y))
    easy_rect = easy_text.get_rect(center=(WINDOW_WIDTH/2, start_y + MENU_SPACING))
    medium_rect = medium_text.get_rect(center=(WINDOW_WIDTH/2, start_y + MENU_SPACING * 2))
    hard_rect = hard_text.get_rect(center=(WINDOW_WIDTH/2, start_y + MENU_SPACING * 3))

    # Create larger rectangles for hover/click effects
    easy_hover_rect = pygame.Rect(easy_rect.x - padding, easy_rect.y - padding,
                                easy_rect.width + padding * 2, easy_rect.height + padding * 2)
    medium_hover_rect = pygame.Rect(medium_rect.x - padding, medium_rect.y - padding,
                                  medium_rect.width + padding * 2, medium_rect.height + padding * 2)
    hard_hover_rect = pygame.Rect(hard_rect.x - padding, hard_rect.y - padding,
                                hard_rect.width + padding * 2, hard_rect.height + padding * 2)

    # Get mouse position and state
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]  # Left mouse button

    # Draw hover and click effects
    for rect, text_rect in [(easy_hover_rect, easy_rect), 
                           (medium_hover_rect, medium_rect), 
                           (hard_hover_rect, hard_rect)]:
        if rect.collidepoint(mouse_pos):
            # Draw white outline for hover
            pygame.draw.rect(screen, MENU_COLORS['hover_outline'], rect, 2)
            if mouse_pressed:
                # Create a surface with transparency for the click effect
                s = pygame.Surface((rect.width, rect.height))
                s.set_alpha(128)  # 50% transparency
                s.fill(MENU_COLORS['click_fill'])
                screen.blit(s, rect)

    # Draw menu items
    screen.blit(title_text, title_rect)
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(hard_text, hard_rect)
    pygame.display.update()

    return easy_rect, medium_rect, hard_rect

def draw_ui_area(screen, score, level, pause_button):
    colors = UI_COLORS[level]
    # Draw UI background
    pygame.draw.rect(screen, colors['ui_background'], (0, 0, WINDOW_WIDTH, UI_HEIGHT))
    
    # Draw score and level with white text
    WHITE = (255, 255, 255)
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    level_text = font.render(f'Level: {level.name}', True, WHITE)
    
    # Calculate positions
    score_pos = (10, 10)
    level_text_width = level_text.get_width()
    level_pos = (WINDOW_WIDTH - pause_button.rect.width - level_text_width - 40, 10)
    
    screen.blit(score_text, score_pos)
    screen.blit(level_text, level_pos)
    
    # Draw pause button
    pause_button.draw(screen, level)

def draw_boundaries(screen, level):
    colors = UI_COLORS[level]
    # Draw thinner boundaries, starting below UI area
    boundary_pixel_size = int(BOUNDARY_THICKNESS * GRID_SIZE)  # Convert to pixels
    for i in range(1):  # Only one iteration needed for thinner boundary
        # Top boundary (below UI)
        pygame.draw.rect(screen, colors['boundary'], (i * GRID_SIZE, UI_HEIGHT + (i * GRID_SIZE), 
                                      WINDOW_WIDTH - (2 * i * GRID_SIZE), boundary_pixel_size))
        # Bottom boundary
        pygame.draw.rect(screen, colors['boundary'], (i * GRID_SIZE, WINDOW_HEIGHT - boundary_pixel_size - (i * GRID_SIZE), 
                                      WINDOW_WIDTH - (2 * i * GRID_SIZE), boundary_pixel_size))
        # Left boundary
        pygame.draw.rect(screen, colors['boundary'], (i * GRID_SIZE, UI_HEIGHT + (i * GRID_SIZE), 
                                      boundary_pixel_size, WINDOW_HEIGHT - UI_HEIGHT - (2 * i * GRID_SIZE)))
        # Right boundary
        pygame.draw.rect(screen, colors['boundary'], (WINDOW_WIDTH - boundary_pixel_size - (i * GRID_SIZE), UI_HEIGHT + (i * GRID_SIZE), 
                                      boundary_pixel_size, WINDOW_HEIGHT - UI_HEIGHT - (2 * i * GRID_SIZE)))

def show_game_over(screen, score, level):
    colors = UI_COLORS[level]
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(colors['background'])
    screen.blit(overlay, (0, 0))

    game_over_font = pygame.font.Font(None, 100)
    text_font = pygame.font.Font(None, 65)

    # Use white color (255, 255, 255) for all text regardless of level
    WHITE = (255, 255, 255)
    
    game_over_text = game_over_font.render('GAME OVER', True, WHITE)
    score_text = text_font.render(f'Final Score: {score}', True, WHITE)
    continue_text = text_font.render('Press SPACE to restart or ESC to quit', True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 100))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 100))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(continue_text, continue_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    return True

def show_pause_screen(screen, level):
    colors = UI_COLORS[level]
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(colors['background'])
    screen.blit(overlay, (0, 0))

    pause_font = pygame.font.Font(None, 100)
    text_font = pygame.font.Font(None, 65)

    # Use white color (255, 255, 255) for all text regardless of level
    WHITE = (255, 255, 255)
    
    pause_text = pause_font.render('PAUSED', True, WHITE)
    continue_text = text_font.render('Press ESC or click Pause to resume', True, WHITE)
    menu_text = text_font.render('Press M to return to Main Menu', True, WHITE)

    pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 100))
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 100))

    screen.blit(pause_text, pause_rect)
    screen.blit(continue_text, continue_rect)
    screen.blit(menu_text, menu_rect)
    pygame.display.update()

    return False  # Continue game by default

def resize_window(width, height, screen, snake=None, food=None, level=None, pause_button=None, paused=False):
    global WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT, PLAY_AREA_HEIGHT, GRID_HEIGHT_PLAYABLE
    
    # Update window dimensions
    WINDOW_WIDTH = max(800, width)  # Minimum width of 800
    WINDOW_HEIGHT = max(600, height)  # Minimum height of 600
    
    # Update grid dimensions
    GRID_WIDTH = int(WINDOW_WIDTH // GRID_SIZE)
    GRID_HEIGHT = int(WINDOW_HEIGHT // GRID_SIZE)
    
    # Update play area
    PLAY_AREA_HEIGHT = WINDOW_HEIGHT - UI_HEIGHT
    GRID_HEIGHT_PLAYABLE = PLAY_AREA_HEIGHT // GRID_SIZE
    
    # Create new resized surface
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    
    # If we're in the menu, redraw it
    if not snake and not food:
        draw_menu(screen)
    # If we're in the game, redraw everything
    elif snake and food and level:
        screen.fill(UI_COLORS[level]['background'])
        if pause_button:
            pause_button.rect.x = WINDOW_WIDTH - 100  # Update pause button position
            draw_ui_area(screen, snake.score, level, pause_button)
        if level in [Level.MEDIUM, Level.HARD]:
            draw_boundaries(screen, level)
        snake.render(screen)
        food.render(screen)
        if paused:
            show_pause_screen(screen, level)
        pygame.display.update()
    
    return screen

def main():
    # Set up display with windowed mode
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Snake Ventures')
    
    # Center the window on the screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    clock = pygame.time.Clock()

    while True:
        # Level selection menu
        easy_rect, medium_rect, hard_rect = draw_menu(screen)
        level = None

        while level is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if easy_rect.collidepoint(mouse_pos):
                        level = Level.EASY
                    elif medium_rect.collidepoint(mouse_pos):
                        level = Level.MEDIUM
                    elif hard_rect.collidepoint(mouse_pos):
                        level = Level.HARD
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    screen = resize_window(event.w, event.h, screen)
                    easy_rect, medium_rect, hard_rect = draw_menu(screen)

        # Set speed based on level
        if level == Level.EASY:
            SNAKE_SPEED = SPEED_EASY
        elif level == Level.MEDIUM:
            SNAKE_SPEED = SPEED_MEDIUM
        else:  # HARD
            SNAKE_SPEED = SPEED_HARD

        snake = Snake(level)
        food = Food(level)
        
        # Create pause button
        pause_button = Button(WINDOW_WIDTH - 100, 5, 90, 30, "Pause", level=level)
        paused = False
        return_to_menu = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                        if paused:
                            return_to_menu = show_pause_screen(screen, level)
                    elif event.key == pygame.K_m and paused:
                        return_to_menu = True
                    elif not paused:
                        if event.key == pygame.K_UP and snake.direction != (0, 1):
                            snake.direction = (0, -1)
                        elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                            snake.direction = (0, 1)
                        elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                            snake.direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                            snake.direction = (1, 0)
                elif event.type == pygame.VIDEORESIZE:
                    screen = resize_window(event.w, event.h, screen, snake, food, level, pause_button, paused)
                
                # Handle pause button events
                if pause_button.handle_event(event):
                    paused = not paused
                    if paused:
                        return_to_menu = show_pause_screen(screen, level)

            if return_to_menu:
                break

            if not paused:
                # Update snake
                if not snake.update():
                    if show_game_over(screen, snake.score, level):
                        break

                # Check if snake ate the food using the actual rendered rectangles
                snake_head_rect = pygame.Rect(
                    snake.positions[0][0] * GRID_SIZE + (GRID_SIZE - SNAKE_SIZE) // 2,
                    snake.positions[0][1] * GRID_SIZE + (GRID_SIZE - SNAKE_SIZE) // 2,
                    SNAKE_SIZE,
                    SNAKE_SIZE
                )
                food_rect = food.get_collision_rect()

                if snake_head_rect.colliderect(food_rect):
                    snake.length += 1
                    snake.score += 10
                    food.randomize_position()

                # Draw everything
                screen.fill(UI_COLORS[level]['background'])
                draw_ui_area(screen, snake.score, level, pause_button)
                if level in [Level.MEDIUM, Level.HARD]:
                    draw_boundaries(screen, level)
                snake.render(screen)
                food.render(screen)

                pygame.display.update()
                clock.tick(SNAKE_SPEED)

if __name__ == '__main__':
    main() 