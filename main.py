import pygame
import random
import math

pygame.init()

# =========================
# SETTINGS
# =========================
WIDTH = 1000
HEIGHT = 700
FPS = 60
GAME_TIME = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")
clock = pygame.time.Clock()

# Fonts
FONT = pygame.font.Font(None, 32)
BIG_FONT = pygame.font.Font(None, 64)
SMALL_FONT = pygame.font.Font(None, 24)

# Colors
BG = (18, 20, 27)
WHITE = (240, 240, 240)
RED = (235, 70, 70)
GREEN = (70, 220, 120)
BLUE = (70, 150, 255)
GRAY = (70, 75, 85)
YELLOW = (255, 210, 70)

# =========================
# TARGET
# =========================
class Target:
    def __init__(self):
        self.radius = random.randint(20, 40)
        self.x = random.randint(self.radius + 20, WIDTH - self.radius - 20)
        self.y = random.randint(120 + self.radius, HEIGHT - self.radius - 20)

    def draw(self):
        # Outer circle
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

        # Red circle
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius - 5)

        # White circle
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius - 12)

        # Center
        pygame.draw.circle(screen, RED, (self.x, self.y), max(3, self.radius - 22))

    def hit(self, mouse_pos):
        distance = math.sqrt(
            (mouse_pos[0] - self.x) ** 2 +
            (mouse_pos[1] - self.y) ** 2
        )

        return distance <= self.radius


# =========================
# GAME VARIABLES
# =========================
target = Target()

score = 0
shots = 0
hits = 0
combo = 0
best_combo = 0

start_time = pygame.time.get_ticks()
game_over = False

# Hit effects
hit_effects = []


# =========================
# RESET GAME
# =========================
def reset_game():
    global target
    global score, shots, hits
    global combo, best_combo
    global start_time, game_over
    global hit_effects

    target = Target()

    score = 0
    shots = 0
    hits = 0
    combo = 0
    best_combo = 0

    start_time = pygame.time.get_ticks()
    game_over = False
    hit_effects = []


# =========================
# DRAW TEXT
# =========================
def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


# =========================
# MAIN LOOP
# =========================
running = True

while running:

    clock.tick(FPS)

    # ---------------------
    # EVENTS
    # ---------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if not game_over:

                shots += 1

                if target.hit(event.pos):

                    hits += 1
                    combo += 1

                    if combo > best_combo:
                        best_combo = combo

                    # More points with combo
                    points = 100 + (combo * 10)
                    score += points

                    # Create hit effect
                    hit_effects.append({
                        "x": target.x,
                        "y": target.y,
                        "radius": 5,
                        "alpha": 255
                    })

                    # New target
                    target = Target()

                else:
                    combo = 0

        # Restart
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                reset_game()

    # ---------------------
    # TIMER
    # ---------------------
    if not game_over:

        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        remaining = max(0, GAME_TIME - elapsed)

        if remaining <= 0:
            game_over = True

    else:
        remaining = 0

    # ---------------------
    # DRAW BACKGROUND
    # ---------------------
    screen.fill(BG)

    # Top bar
    pygame.draw.rect(
        screen,
        (25, 28, 38),
        (0, 0, WIDTH, 90)
    )

    pygame.draw.line(
        screen,
        GRAY,
        (0, 90),
        (WIDTH, 90),
        2
    )

    # ---------------------
    # HUD
    # ---------------------
    draw_text(
        f"SCORE: {score}",
        FONT,
        WHITE,
        25,
        20
    )

    draw_text(
        f"HITS: {hits}",
        FONT,
        GREEN,
        220,
        20
    )

    draw_text(
        f"SHOTS: {shots}",
        FONT,
        WHITE,
        350,
        20
    )

    accuracy = 0

    if shots > 0:
        accuracy = (hits / shots) * 100

    draw_text(
        f"ACCURACY: {accuracy:.1f}%",
        FONT,
        BLUE,
        520,
        20
    )

    draw_text(
        f"COMBO: {combo}",
        FONT,
        YELLOW,
        760,
        20
    )

    # Timer
    draw_text(
        f"{remaining:.1f}s",
        BIG_FONT,
        RED if remaining <= 5 else WHITE,
        WIDTH // 2 - 45,
        100
    )

    # ---------------------
    # TARGET
    # ---------------------
    if not game_over:
        target.draw()

    # ---------------------
    # HIT EFFECTS
    # ---------------------
    for effect in hit_effects[:]:

        pygame.draw.circle(
            screen,
            GREEN,
            (effect["x"], effect["y"]),
            effect["radius"],
            3
        )

        effect["radius"] += 4
        effect["alpha"] -= 15

        if effect["alpha"] <= 0:
            hit_effects.remove(effect)

    # ---------------------
    # GAME OVER
    # ---------------------
    if game_over:

        # Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((5, 5, 8))
        screen.blit(overlay, (0, 0))

        draw_text(
            "GAME OVER",
            BIG_FONT,
            WHITE,
            WIDTH // 2 - 150,
            200
        )

        draw_text(
            f"Score: {score}",
            FONT,
            WHITE,
            WIDTH // 2 - 70,
            290
        )

        draw_text(
            f"Accuracy: {accuracy:.1f}%",
            FONT,
            BLUE,
            WIDTH // 2 - 85,
            330
        )

        draw_text(
            f"Best Combo: {best_combo}",
            FONT,
            YELLOW,
            WIDTH // 2 - 95,
            370
        )

        draw_text(
            "Press R to play again",
            FONT,
            GREEN,
            WIDTH // 2 - 110,
            450
        )

    # ---------------------
    # CROSSHAIR
    # ---------------------
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if not game_over:

        pygame.draw.line(
            screen,
            WHITE,
            (mouse_x - 10, mouse_y),
            (mouse_x + 10, mouse_y),
            1
        )

        pygame.draw.line(
            screen,
            WHITE,
            (mouse_x, mouse_y - 10),
            (mouse_x, mouse_y + 10),
            1
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (mouse_x, mouse_y),
            12,
            1
        )

    pygame.display.flip()

pygame.quit()