import pygame
import sys

pygame.init()

# Cửa sổ game
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bắn đạn với F")

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Nhân vật
x, y = 300, 300
size = 40
speed = 5

# Nhảy & trọng lực
vel_y = 0
gravity = 0.5
is_jumping = False
ground_y = HEIGHT - size

# Ảnh nhân vật
player_images = [
    pygame.image.load("kenney_pixel-line-platformer/Tiles/tile_0040.png"),
    pygame.image.load("kenney_pixel-line-platformer/Tiles/tile_0041.png"),
    pygame.image.load("kenney_pixel-line-platformer/Tiles/tile_0042.png")
]
player_images = [pygame.transform.scale(img, (size, size)) for img in player_images]

current_img = 0
frame_count = 0
facing_left = False

# Ảnh chướng ngại vật (mục tiêu)
obstacle_img = pygame.image.load("kenney_pixel-line-platformer/Tiles/tile_0016.png")
obstacle_size = 40
obstacle_img = pygame.transform.scale(obstacle_img, (obstacle_size, obstacle_size))
obstacle_x, obstacle_y = 400, ground_y
obstacle_alive = True
hit_count = 0
respawn_time = 0

# Đạn
bullets = []
bullet_speed = 8

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # chỉ thoát khi bấm nút X
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:  # bấm F thì bắn 1 viên
                bullet_x = x + size//2
                bullet_y = y + size//2
                direction = -1 if facing_left else 1
                bullets.append({"x": bullet_x, "y": bullet_y, "dir": direction})

    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_a]:
        x -= speed
        facing_left = True
        moving = True
    if keys[pygame.K_d]:
        x += speed
        facing_left = False
        moving = True
    if keys[pygame.K_SPACE] and not is_jumping:
        vel_y = -10
        is_jumping = True

    # Trọng lực
    vel_y += gravity
    y += vel_y
    if y >= ground_y:
        y = ground_y
        vel_y = 0
        is_jumping = False

    # Giới hạn màn hình
    if x < 0: x = 0
    if x > WIDTH - size: x = WIDTH - size

    # Animation
    if moving:
        frame_count += 1
        if frame_count >= 10:
            current_img = (current_img + 1) % len(player_images)
            frame_count = 0
    else:
        current_img = 0

    # Ảnh nhân vật theo hướng
    image = player_images[current_img]
    if facing_left:
        image = pygame.transform.flip(image, True, False)

    # Tạo rect
    player_rect = pygame.Rect(x, y, size, size)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_size, obstacle_size)

    # Update đạn
    for bullet in bullets[:]:
        bullet["x"] += bullet_speed * bullet["dir"]

        # Check va chạm với mục tiêu
        if obstacle_alive and obstacle_rect.collidepoint(bullet["x"], bullet["y"]):
            bullets.remove(bullet)
            hit_count += 1
            print("💥 Trúng mục tiêu! Hit:", hit_count)
            if hit_count >= 5:
                obstacle_alive = False
                respawn_time = pygame.time.get_ticks() + 10000  # 10s hồi sinh
        elif bullet["x"] < 0 or bullet["x"] > WIDTH:
            bullets.remove(bullet)

    # Hồi sinh mục tiêu sau 10s
    if not obstacle_alive and pygame.time.get_ticks() >= respawn_time:
        obstacle_alive = True
        hit_count = 0
        print("✅ Mục tiêu đã hồi sinh!")

    # Vẽ
    screen.fill(WHITE)
    screen.blit(image, (x, y))  # nhân vật

    # Vẽ mục tiêu
    if obstacle_alive:
        screen.blit(obstacle_img, (obstacle_x, obstacle_y))

    # Vẽ đạn
    for bullet in bullets:
        pygame.draw.circle(screen, RED, (bullet["x"], bullet["y"]), 5)

    # Vẽ mặt đất
    pygame.draw.rect(screen, GREEN, (0, ground_y + size, WIDTH, 20))
    pygame.display.flip()
    clock.tick(60)
    print ("huy thong minh")
pygame.quit()