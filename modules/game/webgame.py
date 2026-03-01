import random
import asyncio
import pygame

class Player:
    def __init__(self, w=800, h=600):
        self.width = 50
        self.height = 30
        self.x = w // 2 - self.width // 2
        self.y = h - 70
        self.speed = 8
        self.color = (0, 255, 0)
        self.lives = 3
        self.score = 0
        self.screen_width = w
        self.screen_height = h

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.polygon(screen, self.color, [
            (self.x + self.width // 2, self.y - 15),
            (self.x + self.width // 3, self.y),
            (self.x + 2 * self.width // 3, self.y)
        ])

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < self.screen_width - self.width:
            self.x += self.speed

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Enemy:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.x = x
        self.y = y
        self.speed = 1
        self.direction = 1
        self.color = random.choice([(255, 0, 0), (0, 120, 255), (255, 255, 255)])
        self.points = 10 if self.color == (255, 0, 0) else 20 if self.color == (0, 120, 255) else 30
        self.frame = 0
        self.animation_timer = 0

    def draw(self, screen):
        self.animation_timer += 1
        if self.animation_timer >= 30:
            self.frame = 1 - self.frame
            self.animation_timer = 0

        if self.frame == 0:
            self.draw_frame1(screen)
        else:
            self.draw_frame2(screen)

    def draw_frame1(self, screen):
        pygame.draw.rect(screen, self.color, (self.x + 5, self.y, self.width - 10, 30))
        pygame.draw.rect(screen, self.color, (self.x, self.y + 10, self.width, 20))
        pygame.draw.rect(screen, self.color, (self.x + 15, self.y + 30, 5, 10))
        pygame.draw.rect(screen, self.color, (self.x + 25, self.y + 30, 5, 10))
        pygame.draw.rect(screen, (0, 0, 0), (self.x + 10, self.y + 5, 8, 8))
        pygame.draw.rect(screen, (0, 0, 0), (self.x + 25, self.y + 5, 8, 8))
        pygame.draw.rect(screen, (0, 0, 0), (self.x + 15, self.y + 20, 12, 3))

    def draw_frame2(self, screen):
        pygame.draw.rect(screen, self.color, (self.x + 5, self.y, self.width - 10, 30))
        pygame.draw.rect(screen, self.color, (self.x, self.y + 10, self.width, 20))
        pygame.draw.rect(screen, self.color, (self.x + 15, self.y + 30, 5, 15))
        pygame.draw.rect(screen, self.color, (self.x + 25, self.y + 30, 5, 15))
        pygame.draw.rect(screen, (0, 0, 0), (self.x + 10, self.y + 5, 8, 3))
        pygame.draw.rect(screen, (0, 0, 0), (self.x + 25, self.y + 5, 8, 3))
        pygame.draw.rect(screen, (0, 0, 0), (self.x + 12, self.y + 20, 18, 5))

    def move(self):
        self.x += self.speed * self.direction

    def change_direction(self):
        self.direction *= -1
        self.y += 20

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Bullet:
    def __init__(self, x, y, direction="up", h=600):
        self.width = 5
        self.height = 15
        self.x = x
        self.y = y
        self.speed = 10
        self.direction = direction
        self.color = (255, 255, 0) if direction == "up" else (255, 0, 0)
        self.screen_height = h

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        if self.direction == "up":
            self.y -= self.speed
        else:
            self.y += self.speed

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        return self.y < 0 or self.y > self.screen_height


class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("impact", 36)
        self.small_font = pygame.font.SysFont("impact", 24)
        self.player = None
        self.bullets = []
        self.enemies = []
        self.enemy_bullets = []
        self.game_over = False
        self.level = 1
        self.running = True
        self.reset_game()

    def reset_game(self):
        self.player = Player(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.bullets = []
        self.enemy_bullets = []
        self.game_over = False
        self.level = 1
        self.create_enemies()

    def create_enemies(self):
        self.enemies = []
        rows = 3 + self.level % 7
        cols = 8
        for row in range(rows):
            for col in range(cols):
                x = 100 + col * 70
                y = 50 + row * 50
                enemy = Enemy(x, y)
                enemy.speed = 1 + self.level * 0.5
                self.enemies.append(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    bullet = Bullet(
                        self.player.x + self.player.width // 2 - 2,
                        self.player.y,
                        "up",
                        self.SCREEN_HEIGHT
                    )
                    self.bullets.append(bullet)
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move("left")
        if keys[pygame.K_d]:
            self.player.move("right")

    def update(self):
        if self.game_over:
            return

        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)

        change_direction = False
        for enemy in self.enemies:
            enemy.move()
            if enemy.x <= 0 or enemy.x + enemy.width >= self.SCREEN_WIDTH:
                change_direction = True
            if random.random() < 0.0005 + self.level * 0.0002:
                enemy_bullet = Bullet(
                    enemy.x + enemy.width // 2 - 2,
                    enemy.y + enemy.height,
                    "down",
                    self.SCREEN_HEIGHT
                )
                self.enemy_bullets.append(enemy_bullet)

        if change_direction:
            for enemy in self.enemies:
                enemy.change_direction()

        for bullet in self.bullets[:]:
            bullet_rect = bullet.get_rect()
            for enemy in self.enemies[:]:
                if bullet_rect.colliderect(enemy.get_rect()):
                    self.player.score += enemy.points
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    break

        for bullet in self.enemy_bullets[:]:
            if bullet.get_rect().colliderect(self.player.get_rect()):
                self.player.lives -= 1
                self.enemy_bullets.remove(bullet)
                if self.player.lives <= 0:
                    self.game_over = True

        for enemy in self.enemies:
            if enemy.get_rect().colliderect(self.player.get_rect()):
                self.game_over = True
            if enemy.y + enemy.height >= self.SCREEN_HEIGHT - 50:
                self.game_over = True
                break

        if not self.enemies:
            self.level += 1
            self.create_enemies()

    def draw(self):
        self.screen.fill((0, 0, 0))

        for _ in range(50):
            x = random.randint(0, self.SCREEN_WIDTH)
            y = random.randint(0, self.SCREEN_HEIGHT)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1)

        self.player.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        score_text = self.font.render(f"Score: {self.player.score}", False, (0, 255, 0))
        lives_text = self.font.render(f"Lives: {self.player.lives}", False, (0, 255, 0))
        level_text = self.font.render(f"Level: {self.level}", False, (0, 255, 0))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (self.SCREEN_WIDTH - 150, 10))
        self.screen.blit(level_text, (self.SCREEN_WIDTH // 2 - 60, 10))

        controls_text = self.small_font.render("Control: A/D for move, SPACE for shoot", False, (255, 255, 255))
        self.screen.blit(controls_text,
                         (self.SCREEN_WIDTH // 2 - controls_text.get_width() // 2, self.SCREEN_HEIGHT - 30))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER", False, (255, 0, 0))
            restart_text = self.font.render("Press R for restart", False, (255, 255, 255))
            self.screen.blit(game_over_text,
                             (self.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, self.SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text,
                             (self.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, self.SCREEN_HEIGHT // 2))

        pygame.display.flip()

    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
            await asyncio.sleep(0)


if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())