import pygame
import sys

# Khởi tạo pygame
pygame.init()

# Màn hình
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game đi cảnh nhỏ")

# Màu sắc
WHITE = (255, 255, 255)
PINK = (255, 182, 193)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 50, 50)

# Clock
clock = pygame.time.Clock()

# Nhân vật
player_radius = 30
player_x, player_y = 100, HEIGHT - player_radius - 50
player_vel_x = 0
player_vel_y = 0
gravity = 0.8
jump_strength = -15
on_ground = True

# Nền đất
ground_y = HEIGHT - 50

# Chướng ngại vật
obstacles = [
    pygame.Rect(300, ground_y - 40, 40, 40),
    pygame.Rect(500, ground_y - 60, 50, 60),
    pygame.Rect(700, ground_y - 30, 30, 30)
]

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Điều khiển
    keys = pygame.key.get_pressed()
    player_vel_x = 0
    if keys[pygame.K_LEFT]:
        player_vel_x = -5
    if keys[pygame.K_RIGHT]:
        player_vel_x = 5
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = jump_strength
        on_ground = False

    # Cập nhật vị trí
    player_x += player_vel_x
    player_y += player_vel_y
    player_vel_y += gravity

    # Chạm đất
    if player_y + player_radius >= ground_y:
        player_y = ground_y - player_radius
        player_vel_y = 0
        on_ground = True

    # Giữ nhân vật không ra khỏi màn hình
    if player_x - player_radius < 0:
        player_x = player_radius
    if player_x + player_radius > WIDTH:
        player_x = WIDTH - player_radius

    # Tạo rect nhân vật để kiểm tra va chạm
    player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius,
                              player_radius * 2, player_radius * 2)

    # Kiểm tra va chạm
    for obs in obstacles:
        if player_rect.colliderect(obs):
            print("Game Over!")
            running = False

    # Vẽ
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, 50))  # nền đất

    # Vẽ nhân vật dễ thương (hình tròn + mắt + tai)
    pygame.draw.circle(screen, PINK, (int(player_x), int(player_y)), player_radius)  # thân
    # tai
    pygame.draw.circle(screen, PINK, (int(player_x - 20), int(player_y - 30)), 10)
    pygame.draw.circle(screen, PINK, (int(player_x + 20), int(player_y - 30)), 10)
    # mắt
    pygame.draw.circle(screen, BLACK, (int(player_x - 10), int(player_y - 5)), 5)
    pygame.draw.circle(screen, BLACK, (int(player_x + 10), int(player_y - 5)), 5)

    # Vẽ chướng ngại vật
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)

    pygame.display.flip()
