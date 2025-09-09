import pygame, sys

pygame.init()

# Cấu hình cửa sổ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game vượt ải có quái")

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Nhân vật
player = pygame.Rect(50, 500, 40, 40)
velocity = 5
player_hp = 3
score = 0

# Cửa ra
exit_rect = pygame.Rect(700, 500, 40, 40)

# Danh sách level: mỗi level có [chướng ngại, quái]
levels = [
    {
        "walls": [pygame.Rect(300, 500, 100, 40), pygame.Rect(500, 400, 100, 40)],
        "enemies": [pygame.Rect(400, 500, 40, 40)]
    },
    {
        "walls": [pygame.Rect(200, 450, 150, 40), pygame.Rect(450, 350, 200, 40)],
        "enemies": [pygame.Rect(300, 450, 40, 40), pygame.Rect(600, 350, 40, 40)]
    },
    {
        "walls": [pygame.Rect(200, 450, 150, 40), pygame.Rect(450, 350, 200, 40)],
        "enemies": [pygame.Rect(390, 450, 40, 40), pygame.Rect(680, 350, 40, 40)]
    }
]

current_level = 0
enemy_speed = 2
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Tải hình ảnh
rock_img = pygame.image.load(r"d:\laptrinhgame\rock.jpg")
rock_img = pygame.transform.scale(rock_img, (100, 40))  # chỉnh kích thước cho phù hợp

# Tải các ảnh nhân vật
player_imgs = [
    pygame.image.load(r"d:\laptrinhgame\tile_0040.png"),
    pygame.image.load(r"d:\laptrinhgame\tile_0041.png"),
    pygame.image.load(r"d:\laptrinhgame\tile_0042.png")
]
for i in range(3):
    player_imgs[i] = pygame.transform.scale(player_imgs[i], (40, 40))  # chỉnh kích thước

player_img_index = 0
frame_count = 0

def reset_player():
    player.x, player.y = 50, 500

# Thêm biến kiểm tra hướng
facing_left = False

is_jumping = False
jump_speed = 12
gravity = 1
vertical_velocity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_a]:
        player.x -= velocity
        moved = True
        facing_left = True
    if keys[pygame.K_d]:
        player.x += velocity
        moved = True
        facing_left = False
    # Chỉ cho nhảy khi không đang nhảy
    if not is_jumping and (keys[pygame.K_w] or keys[pygame.K_SPACE]):
        is_jumping = True
        vertical_velocity = -jump_speed
        moved = True

    if keys[pygame.K_s]:
        player.y += velocity
        moved = True

    # Giới hạn nhân vật trong màn hình
    player.x = max(0, min(WIDTH - player.width, player.x))
    player.y = max(0, min(HEIGHT - player.height, player.y))

    # Đổi ảnh nhân vật khi di chuyển
    if moved:
        frame_count += 1
        if frame_count % 10 == 0:  # đổi ảnh mỗi 10 frame
            player_img_index = (player_img_index + 1) % 3

    # Kiểm tra thắng màn
    if player.colliderect(exit_rect):
        score += 100
        current_level += 1
        if current_level >= len(levels):
            screen.fill(WHITE)
            win_text = font.render("🎉 YOU WIN! Điểm: " + str(score), True, GREEN)
            screen.blit(win_text, (WIDTH//2 - 100, HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
        else:
            reset_player()

    # Di chuyển quái (đi qua lại trái - phải)
    for enemy in levels[current_level]["enemies"]:
        enemy.x += enemy_speed
        if enemy.x <= 100 or enemy.x >= WIDTH - 100:
            enemy_speed *= -1

    # Xử lý nhảy và rơi
    if is_jumping:
        player.y += vertical_velocity
        vertical_velocity += gravity
        # Chạm đất (giả sử đất là y=500)
        if player.y >= 500:
            player.y = 500
            is_jumping = False
            vertical_velocity = 0

    # Kiểm tra va chạm với nền
    if player.y >= HEIGHT - player.height:
        player.y = HEIGHT - player.height
        is_jumping = False

    # Vẽ màn hình
    screen.fill(WHITE)
    # Lật ảnh nếu đi sang trái
    if facing_left:
        img = pygame.transform.flip(player_imgs[player_img_index], True, False)
    else:
        img = player_imgs[player_img_index]
    screen.blit(img, (player.x, player.y))
    pygame.draw.rect(screen, GREEN, exit_rect) # Cửa ra
    # Vẽ chướng ngại vật
    for wall in levels[current_level]["walls"]:
        screen.blit(rock_img, (wall.x, wall.y))
        if player.colliderect(wall):
            reset_player()

    # Vẽ và kiểm tra quái
    for enemy in levels[current_level]["enemies"]:
        pygame.draw.rect(screen, BLUE, enemy)
        if player.colliderect(enemy):
            player_hp -= 1
            reset_player
            if player_hp <= 0:
                print("💀 Game Over! Điểm:", score)
                pygame.quit()
                sys.exit()

    # Vẽ thông tin HUD
    hp_text = font.render(f"HP: {player_hp}", True, RED)
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {current_level+1}", True, GREEN)
    screen.blit(hp_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(level_text, (10, 70))

    pygame.display.flip()
    clock.tick(60)
