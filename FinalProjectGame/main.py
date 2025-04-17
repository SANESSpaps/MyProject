import pygame
from random import randint

# Инициализация PyGame
pygame.init()

# Размеры окна и заголовок игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = 'Мини Платформер'

# Определённые цвета
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)

# Игровые параметры
GRAVITY = 1
JUMP_STRENGTH = 15
PLAYER_SIZE = 50
VELOCITY_X = 5
VELOCITY_Y = 0
COIN_SIZE = 20
PLATFORM_HEIGHT = 20
PLATFORM_WIDTH = 100

# Поверхности и окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Исходная позиция игрока
player_position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
camera_offset = [0, 0]

# Больше платформ
platforms = [
    [SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2, SCREEN_HEIGHT - PLATFORM_HEIGHT],
    [SCREEN_WIDTH // 4, SCREEN_HEIGHT - PLATFORM_HEIGHT * 3],
    [SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - PLATFORM_HEIGHT * 4],
    [SCREEN_WIDTH // 3, SCREEN_HEIGHT - PLATFORM_HEIGHT * 5],
    [SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT - PLATFORM_HEIGHT * 6],
    [SCREEN_WIDTH // 5, SCREEN_HEIGHT - PLATFORM_HEIGHT * 7],
    [SCREEN_WIDTH * 4 // 5, SCREEN_HEIGHT - PLATFORM_HEIGHT * 8]
]

# Монеты
coins = []
for _ in range(10):
    coins.append([randint(0, SCREEN_WIDTH - COIN_SIZE), randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - PLATFORM_HEIGHT)])

# Состояния игры
STATES = ['menu', 'settings', 'shop', 'game']
state = STATES[0]

# Переменная для счета монет
coin_count = 0

# Магазин цветов
colors = {
    1: {"name": "Красный", "cost": 0, "color": RED},
    2: {"name": "Зелёный", "cost": 100, "color": GREEN},
    3: {"name": "Чёрный", "cost": 150, "color": BLACK},
    4: {"name": "Жёлтый", "cost": 200, "color": YELLOW}
}
current_color = colors[1]["color"]  # Красный по умолчанию

# Функция для вывода текста
def draw_text(text, position, color=WHITE):
    font = pygame.font.SysFont(None, 36)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)

# Основной игровой цикл
running = True
while running:
    clock.tick(FPS)
    screen.fill(SKY_BLUE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # Выход из игры по нажатию Esc

    # Разделение состояний игры
    if state == 'menu':
        draw_text("МЕНЮ", (SCREEN_WIDTH // 2 - 50, 100))
        draw_text("Нажмите ENTER для начала игры", (SCREEN_WIDTH // 2 - 150, 200))
        draw_text("Нажмите ESC для выхода", (SCREEN_WIDTH // 2 - 100, 300))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            state = 'game'

    elif state == 'settings':
        draw_text("НАСТРОЙКИ", (SCREEN_WIDTH // 2 - 70, 100))
        draw_text("Звуковой режим:", (SCREEN_WIDTH // 2 - 100, 200))
        draw_text("Графический режим:", (SCREEN_WIDTH // 2 - 100, 300))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            state = 'menu'

    elif state == 'shop':
        draw_text("МАГАЗИН", (SCREEN_WIDTH // 2 - 50, 100))
        draw_text(f"У вас {coin_count} монет", (SCREEN_WIDTH // 2 - 100, 150))
        for idx, item in colors.items():
            cost = item["cost"]
            color_name = item["name"]
            draw_text(f"{idx}. {color_name}: {cost} монет", (SCREEN_WIDTH // 2 - 100, 200 + idx * 50))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            current_color = colors[1]["color"]
        elif keys[pygame.K_2] and coin_count >= colors[2]["cost"]:
            coin_count -= colors[2]["cost"]
            current_color = colors[2]["color"]
        elif keys[pygame.K_3] and coin_count >= colors[3]["cost"]:
            coin_count -= colors[3]["cost"]
            current_color = colors[3]["color"]
        elif keys[pygame.K_4] and coin_count >= colors[4]["cost"]:
            coin_count -= colors[4]["cost"]
            current_color = colors[4]["color"]
        elif keys[pygame.K_BACKSPACE]:
            state = 'menu'

    elif state == 'game':
        # Управление персонажем
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_position[0] -= VELOCITY_X
        if keys[pygame.K_RIGHT]:
            player_position[0] += VELOCITY_X
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            # Проверка столкновения с платформой перед прыжком
            collision = any(
                abs(player_position[1] + PLAYER_SIZE - p[1]) < GRAVITY and
                abs(player_position[0] - p[0]) <= PLATFORM_WIDTH // 2
                for p in platforms
            )
            if collision:
                VELOCITY_Y = -JUMP_STRENGTH  # Происходит прыжок

        # Обновление физики персонажа
        VELOCITY_Y += GRAVITY
        player_position[1] += VELOCITY_Y

        # Ограничение по нижнему краю экрана
        if player_position[1] > SCREEN_HEIGHT - PLAYER_SIZE:
            player_position[1] = SCREEN_HEIGHT - PLAYER_SIZE
            VELOCITY_Y = 0

        # Корректировка камеры
        camera_offset[0] = max(min(0, player_position[0] - SCREEN_WIDTH // 2), -(SCREEN_WIDTH - SCREEN_WIDTH))
        camera_offset[1] = max(min(0, player_position[1] - SCREEN_HEIGHT // 2), -(SCREEN_HEIGHT - SCREEN_HEIGHT))

        # Отрисовка платформ
        for plat in platforms:
            pygame.draw.rect(screen, PURPLE, (plat[0] - camera_offset[0], plat[1] - camera_offset[1], PLATFORM_WIDTH, PLATFORM_HEIGHT))

        # Монеты
        new_coins = []
        for c in coins:
            coin_x = c[0] - camera_offset[0]
            coin_y = c[1] - camera_offset[1]
            pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), COIN_SIZE // 2)
            dist = ((player_position[0] - c[0]) ** 2 + (player_position[1] - c[1]) ** 2) ** 0.5
            if dist < PLAYER_SIZE * 0.75:
                coin_count += 1
            else:
                new_coins.append(c)
        coins = new_coins

        # Отрисовка персонажа
        pygame.draw.rect(screen, current_color, (player_position[0] - PLAYER_SIZE // 2 - camera_offset[0], player_position[1] - PLAYER_SIZE // 2 - camera_offset[1], PLAYER_SIZE, PLAYER_SIZE))

        # Информация о монетах
        draw_text(f"МОНЕТЫ: {coin_count}", (10, 10))

    # Обновляем экран
    pygame.display.update()

pygame.quit()