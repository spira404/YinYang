import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1200, 800
COLUMNS, ROWS = 8, 10
CELL_WIDTH = WIDTH // COLUMNS
CELL_HEIGHT = HEIGHT // ROWS
RADIUS = min(CELL_WIDTH, CELL_HEIGHT) // 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 120

center_col = COLUMNS // 2
center_row = ROWS // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black 'n white")
clock = pygame.time.Clock()

grid = [[True for _ in range(COLUMNS)] for _ in range(ROWS)]

# create 2*2 dark cells at the center
for r in range(center_row - 1, center_row + 1):
    for c in range(center_col - 1, center_col + 1):
        if 0 <= r < ROWS and 0 <= c < COLUMNS:
            grid[r][c] = False

class Ball:
    def __init__(self, x, y, color, speed, passes_white):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.radius = RADIUS
        self.dx = speed
        self.dy = speed
        self.passes_white = passes_white

    # correct speed that has too big decline
    def correct(self, delta):
        if 1.8*self.speed < abs(delta) or abs(delta) < self.speed / 4:
            if delta < 0:
                return -self.speed
            return self.speed
        return delta

    def move(self):
        self.dx = self.correct(self.dx)
        self.dy = self.correct(self.dy)

        self.x += self.dx
        self.y += self.dy

        # collision with borders
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.dx = -self.dx
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.dy = -self.dy

        # check cells around
        for row in range(
                max(0, int(self.y / CELL_HEIGHT) - 1), 
                min(ROWS, int(self.y / CELL_HEIGHT) + 2)):
            for column in range(
                    max(0, int(self.x / CELL_WIDTH) - 1), 
                    min(COLUMNS, int(self.x / CELL_WIDTH) + 2)):

                # check if cell's white and ball don't pass through whites or vice versa
                if grid[row][column] != self.passes_white:

                    cell_rect = pygame.Rect(column * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)

                    if self.collision(cell_rect):
                        # detect side of bounce
                        hit_left = abs(self.x - cell_rect.left) <= self.radius
                        hit_right = abs(self.x - cell_rect.right) <= self.radius
                        hit_top = abs(self.y - cell_rect.top) <= self.radius
                        hit_bottom = abs(self.y - cell_rect.bottom) <= self.radius

                        # change color
                        grid[row][column] = not grid[row][column]

                        # make ball bounce
                        if hit_left or hit_right:
                            self.dx = -self.dx
                        if hit_top or hit_bottom:
                            self.dy = -self.dy

                        # add slight randomness of speed/angle
                        self.dy *= random.randrange(90, 110) / 100
                        self.dx *= random.randrange(90, 110) / 100

    def collision(self, rect):
        extended_rect = pygame.Rect(
            rect.left - self.radius,
            rect.top - self.radius,
            rect.width + 2 * self.radius,
            rect.height + 2 * self.radius
        )
        return extended_rect.collidepoint(self.x, self.y)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

default_speed = 10

white_ball_x = (center_col + 0.5) * CELL_WIDTH
white_ball_y = (center_row + 0.5) * CELL_HEIGHT
white_ball = Ball(white_ball_x, white_ball_y, WHITE, default_speed, False)

dark_ball_x = random.randint(RADIUS, WIDTH - RADIUS)
dark_ball_y = random.randint(RADIUS, HEIGHT - RADIUS)
dark_ball = Ball(dark_ball_x, dark_ball_y, BLACK, default_speed, True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    white_ball.move()
    dark_ball.move()

    for row in range(ROWS):
        for col in range(COLUMNS):
            color = WHITE if grid[row][col] else BLACK
            pygame.draw.rect(screen, color, (col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

    white_ball.draw()
    dark_ball.draw()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
