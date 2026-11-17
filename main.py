
import asyncio
import random
import pygame

WIDTH, HEIGHT = 1000, 600
FPS = 60
GAME_TIME = 30.0

BG = (14, 17, 27)
WHITE = (240, 244, 255)
GRAY = (90, 100, 120)
GREEN = (80, 230, 150)
BLUE = (90, 170, 255)
YELLOW = (255, 215, 90)
RED = (255, 90, 100)

class Target:
    def __init__(self):
        self.radius = 27
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.move()

    def move(self):
        margin = self.radius + 12
        self.x = random.randint(margin, WIDTH - margin)
        self.y = random.randint(115 + self.radius, HEIGHT - margin)

    def draw(self, screen):
        pygame.draw.circle(
            screen, (35, 90, 75),
            (self.x, self.y), self.radius + 5
        )
        pygame.draw.circle(
            screen, GREEN,
            (self.x, self.y), self.radius
        )
        pygame.draw.circle(
            screen, WHITE,
            (self.x, self.y), self.radius, 2
        )
        pygame.draw.circle(
            screen, (20, 50, 45),
            (self.x, self.y), 7
        )

class AimTrainer:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Aim Trainer")

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 64)

        self.overlay = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )
        self.overlay.fill((0, 0, 0, 185))

        self.target = Target()
        self.hit_effects = []

        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.hits = 0
        self.shots = 0
        self.combo = 0
        self.best_combo = 0
        self.game_over = False

        self.start_time = pygame.time.get_ticks()

        self.target.move()
        self.hit_effects = []

    def draw_text(self, text, font, color, x, y):
        image = font.render(text, True, color)
        self.screen.blit(image, (x, y))

    def handle_click(self, position):
        if self.game_over:
            return

        self.shots += 1

        dx = position[0] - self.target.x
        dy = position[1] - self.target.y

        if dx * dx + dy * dy <= self.target.radius ** 2:
            self.hits += 1
            self.score += 100
            self.combo += 1

            self.best_combo = max(
                self.best_combo, self.combo
            )

            self.hit_effects.append({
                "x": self.target.x,
                "y": self.target.y,
                "life": 0.25,
                "radius": self.target.radius
            })

            self.target.move()

        else:
            self.combo = 0

    def draw_hud(self, remaining):
        accuracy = (
            self.hits / self.shots * 100
            if self.shots else 0.0
        )

        pygame.draw.rect(
            self.screen, (25, 28, 38),
            (0, 0, WIDTH, 90)
        )

        pygame.draw.line(
            self.screen, GRAY,
            (0, 90), (WIDTH, 90), 2
        )

        self.draw_text(
            f"SCORE: {self.score}",
            self.font, WHITE, 25, 20
        )

        self.draw_text(
            f"HITS: {self.hits}",
            self.font, GREEN, 220, 20
        )

        self.draw_text(
            f"SHOTS: {self.shots}",
            self.font, WHITE, 350, 20
        )

        self.draw_text(
            f"ACCURACY: {accuracy:.1f}%",
            self.font, BLUE, 520, 20
        )

        self.draw_text(
            f"COMBO: {self.combo}",
            self.font, YELLOW, 800, 20
        )

        timer_color = RED if remaining <= 5 else WHITE

        timer_image = self.big_font.render(
            f"{remaining:.1f}s",
            True, timer_color
        )

        timer_rect = timer_image.get_rect(
            center=(WIDTH // 2, 125)
        )

        self.screen.blit(timer_image, timer_rect)

    def update_and_draw_effects(self, dt):
        active = []

        for effect in self.hit_effects:
            effect["life"] -= dt
            effect["radius"] += 180 * dt

            if effect["life"] > 0:
                pygame.draw.circle(
                    self.screen,
                    GREEN,
                    (effect["x"], effect["y"]),
                    max(1, int(effect["radius"])),
                    3
                )

                active.append(effect)

        self.hit_effects = active

    def draw_game_over(self):
        self.screen.blit(self.overlay, (0, 0))

        accuracy = (
            self.hits / self.shots * 100
            if self.shots else 0.0
        )

        title = self.big_font.render(
            "GAME OVER", True, WHITE
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(WIDTH // 2, 220)
            )
        )

        lines = [
            (f"Score: {self.score}", WHITE),
            (f"Accuracy: {accuracy:.1f}%", BLUE),
            (f"Best Combo: {self.best_combo}", YELLOW)
        ]

        for index, (label, color) in enumerate(lines):
            image = self.font.render(
                label, True, color
            )

            self.screen.blit(
                image,
                image.get_rect(
                    center=(WIDTH // 2, 300 + index * 40)
                )
            )

        message = self.font.render(
            "Press R or click to play again",
            True, GREEN
        )

        self.screen.blit(
            message,
            message.get_rect(
                center=(WIDTH // 2, 465)
            )
        )

    async def run(self):
        running = True

        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.handle_click(event.pos)

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif (
                        event.key == pygame.K_r
                        and self.game_over
                    ):
                        self.reset_game()

            elapsed = (
                pygame.time.get_ticks() - self.start_time
            ) / 1000.0

            remaining = max(
                0.0, GAME_TIME - elapsed
            )

            if remaining <= 0:
                self.game_over = True

            self.screen.fill(BG)

            self.draw_hud(remaining)

            if not self.game_over:
                self.target.draw(self.screen)

            self.update_and_draw_effects(dt)

            if self.game_over:
                self.draw_game_over()

            else:
                mx, my = pygame.mouse.get_pos()

                pygame.draw.line(
                    self.screen, WHITE,
                    (mx - 10, my), (mx + 10, my), 1
                )

                pygame.draw.line(
                    self.screen, WHITE,
                    (mx, my - 10), (mx, my + 10), 1
                )

                pygame.draw.circle(
                    self.screen, WHITE,
                    (mx, my), 12, 1
                )

            pygame.display.flip()

            await asyncio.sleep(0)

        pygame.quit()

async def main():
    game = AimTrainer()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())
