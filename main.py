        image = font.render(text, True, color)
        self.screen.blit(image, (x, y))

    def draw_hud(self, remaining):
        accuracy = self.hits / self.shots * 100 if self.shots else 0.0

        pygame.draw.rect(self.screen, (25, 28, 38), (0, 0, WIDTH, 90))
        pygame.draw.line(self.screen, GRAY, (0, 90), (WIDTH, 90), 2)

        self.draw_text(f"SCORE: {self.score}", self.font, WHITE, 25, 20)
        self.draw_text(f"HITS: {self.hits}", self.font, GREEN, 220, 20)
        self.draw_text(f"SHOTS: {self.shots}", self.font, WHITE, 350, 20)
        self.draw_text(
            f"ACCURACY: {accuracy:.1f}%", self.font, BLUE, 520, 20
        )
        self.draw_text(f"COMBO: {self.combo}", self.font, YELLOW, 800, 20)

        timer_color = RED if remaining <= 5 else WHITE
        timer_image = self.big_font.render(
            f"{remaining:.1f}s", True, timer_color
        )
        timer_rect = timer_image.get_rect(center=(WIDTH // 2, 125))
        self.screen.blit(timer_image, timer_rect)

    def update_and_draw_effects(self, dt):
        remaining_effects = []

        for effect in self.hit_effects:
            effect["life"] -= dt
            effect["radius"] += 180 * dt

            if effect["life"] > 0:
                pygame.draw.circle(
                    self.screen,
                    GREEN,
                    (effect["x"], effect["y"]),
                    max(1, int(effect["radius"])),
                    3,
                )
                remaining_effects.append(effect)

        self.hit_effects = remaining_effects

    def draw_game_over(self):
        self.screen.blit(self.overlay, (0, 0))
        accuracy = self.hits / self.shots * 100 if self.shots else 0.0

        title = self.big_font.render("GAME OVER", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 230)))

        self.draw_text(
            f"Score: {self.score}", self.font, WHITE, WIDTH // 2 - 65, 300
        )
        self.draw_text(
            f"Accuracy: {accuracy:.1f}%",
            self.font, BLUE, WIDTH // 2 - 85, 340
        )
        self.draw_text(
            f"Best Combo: {self.best_combo}",
            self.font, YELLOW, WIDTH // 2 - 95, 380
        )

        message = self.font.render(
            "Press R to play again or ESC to quit", True, GREEN
        )
        self.screen.blit(message, message.get_rect(center=(WIDTH // 2, 460)))

    async def run(self):
        running = True

        while running:
            # Keep the desktop frame rate capped, but always yield to the
            # browser event loop below when running through Pygbag.
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000.0
            remaining = max(0.0, GAME_TIME - elapsed)

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
                mouse_x, mouse_y = pygame.mouse.get_pos()
                pygame.draw.line(
                    self.screen, WHITE,
                    (mouse_x - 10, mouse_y), (mouse_x + 10, mouse_y), 1
                )
                pygame.draw.line(
                    self.screen, WHITE,
                    (mouse_x, mouse_y - 10), (mouse_x, mouse_y + 10), 1
                )
                pygame.draw.circle(
                    self.screen, WHITE, (mouse_x, mouse_y), 12, 1
                )

            pygame.display.flip()

            # REQUIRED by Pygbag: let the browser process rendering and input.
            await asyncio.sleep(0)

        pygame.quit()


if __name__ == "__main__":
    asyncio.run(AimTrainer().run())
