import pygame
import sys

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 650
FPS = 60
TITLE = "Bakery Simulator - PZ 2"

COLOR_BG = (245, 240, 230)
COLOR_COUNTER = (140, 90, 50)
COLOR_CASHIER = (100, 60, 30)
COLOR_ENTRANCE = (180, 220, 180)
COLOR_PICKUP = (180, 210, 240)
COLOR_PICKUP_READY = (100, 200, 120)
COLOR_PLAYER = (70, 130, 220)
COLOR_TEXT = (40, 40, 40)
COLOR_UI_BG = (255, 255, 255, 220)
COLOR_MENU_BG = (40, 40, 45)
COLOR_MENU_TEXT = (230, 230, 230)

PLAYER_COLORS = [
    (70, 130, 220),
    (60, 180, 110),
    (220, 90, 80),
    (230, 175, 60),
]

PRODUCTS = [
    {"name": "Хлеб", "price": 70, "stock": 3, "cook_time": 0.0},
    {"name": "Булочка", "price": 90, "stock": 4, "cook_time": 0.0},
    {"name": "Сэндвич", "price": 180, "stock": 2, "cook_time": 5.0},
    {"name": "Кофе", "price": 140, "stock": 5, "cook_time": 3.0},
]

def get_initial_state():
    return {
        "running": True,
        "player_pos": pygame.Vector2(500, 520),
        "player_radius": 22,
        "player_speed": 260.0,
        "player_color_index": 0,
        "money": 420,
        "order_state": "NO_ORDER",
        "current_product": None,
        "cooking_time_left": 0.0,
        "total_cook_time": 0.0,
        "menu_open": False,
        "message": "",
        "message_timer": 0.0,
    }

def get_zones():
    entrance_rect = pygame.Rect(400, 580, 200, 70)
    counter_rect = pygame.Rect(150, 200, 450, 80)
    cashier_rect = pygame.Rect(650, 200, 150, 80)
    pickup_rect = pygame.Rect(700, 420, 220, 120)
    counter_interact_rect = pygame.Rect(150, 280, 450, 70)
    pickup_interact_rect = pygame.Rect(700, 400, 220, 40)
    obstacles = [counter_rect, cashier_rect]
    
    return {
        "entrance": entrance_rect,
        "counter": counter_rect,
        "cashier": cashier_rect,
        "pickup": pickup_rect,
        "counter_interact": counter_interact_rect,
        "pickup_interact": pickup_interact_rect,
        "obstacles": obstacles,
    }

def handle_events(state, zones):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state["running"] = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if state["menu_open"]:
                    state["menu_open"] = False
                else:
                    state["running"] = False

            elif event.key == pygame.K_SPACE and not state["menu_open"]:
                state["player_color_index"] = (state["player_color_index"] + 1) % len(PLAYER_COLORS)

            elif event.key == pygame.K_e and not state["menu_open"]:
                player_rect = pygame.Rect(0, 0, state["player_radius"] * 2, state["player_radius"] * 2)
                player_rect.center = (round(state["player_pos"].x), round(state["player_pos"].y))

                if player_rect.colliderect(zones["counter_interact"]) and state["order_state"] == "NO_ORDER":
                    state["menu_open"] = True
                
                elif player_rect.colliderect(zones["pickup_interact"]) and state["order_state"] == "READY":
                    state["order_state"] = "DONE"
                    state["message"] = "Заказ получен! Нажмите R для нового заказа."
                    state["message_timer"] = 3.0

            elif event.key == pygame.K_r and state["order_state"] == "DONE":
                state["order_state"] = "NO_ORDER"
                state["current_product"] = None
                state["message"] = ""

            elif state["menu_open"] and event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                idx = int(event.unicode) - 1
                product = PRODUCTS[idx]
                
                if product["stock"] <= 0:
                    state["message"] = "Товар закончился"
                    state["message_timer"] = 2.0
                elif state["money"] < product["price"]:
                    state["message"] = "Недостаточно денег"
                    state["message_timer"] = 2.0
                else:
                    state["money"] -= product["price"]
                    product["stock"] -= 1
                    state["current_product"] = product
                    
                    if product["cook_time"] == 0:
                        state["order_state"] = "READY"
                        state["message"] = f"Заказ принят: {product['name']}. Готово!"
                    else:
                        state["order_state"] = "WAITING"
                        state["cooking_time_left"] = product["cook_time"]
                        state["total_cook_time"] = product["cook_time"]
                        state["message"] = f"Заказ принят: {product['name']}. Готовится..."
                    
                    state["message_timer"] = 2.5
                    state["menu_open"] = False

def handle_movement(state, zones, dt):
    if state["menu_open"]:
        return

    keys = pygame.key.get_pressed()
    direction = pygame.Vector2(0, 0)

    if keys[pygame.K_w]: direction.y -= 1
    if keys[pygame.K_s]: direction.y += 1
    if keys[pygame.K_a]: direction.x -= 1
    if keys[pygame.K_d]: direction.x += 1

    # Нормализация для одинаковой скорости по диагонали
    if direction.length_squared() > 0:
        direction = direction.normalize()

    next_position = state["player_pos"] + direction * state["player_speed"] * dt
    radius = state["player_radius"]

    next_position.x = max(radius, min(WINDOW_WIDTH - radius, next_position.x))
    next_position.y = max(radius, min(WINDOW_HEIGHT - radius, next_position.y))

    next_rect = pygame.Rect(0, 0, radius * 2, radius * 2)
    next_rect.center = (round(next_position.x), round(next_position.y))

    blocked = any(next_rect.colliderect(obs) for obs in zones["obstacles"])
    
    if not blocked:
        state["player_pos"] = next_position

def update_order(state, dt):
    # Таймер через dt, а не time.sleep
    if state["order_state"] == "WAITING":
        state["cooking_time_left"] -= dt
        if state["cooking_time_left"] <= 0:
            state["cooking_time_left"] = 0
            state["order_state"] = "READY"
            state["message"] = f"{state['current_product']['name']} готов! Заберите в зоне выдачи."
            state["message_timer"] = 3.0

    if state["message_timer"] > 0:
        state["message_timer"] -= dt
        if state["message_timer"] <= 0:
            state["message"] = ""

def draw_scene(screen, state, zones, font):
    screen.fill(COLOR_BG)

    pygame.draw.rect(screen, COLOR_ENTRANCE, zones["entrance"], border_radius=8)
    entrance_text = font.render("ВХОД", True, (50, 100, 50))
    screen.blit(entrance_text, (zones["entrance"].centerx - 30, zones["entrance"].centery - 10))

    pygame.draw.rect(screen, COLOR_COUNTER, zones["counter"], border_radius=6)
    counter_text = font.render("ПРИЛАВОК", True, (255, 255, 255))
    screen.blit(counter_text, (zones["counter"].centerx - 45, zones["counter"].centery - 10))

    pygame.draw.rect(screen, COLOR_CASHIER, zones["cashier"], border_radius=6)
    cashier_text = font.render("КАССА", True, (255, 255, 255))
    screen.blit(cashier_text, (zones["cashier"].centerx - 30, zones["cashier"].centery - 10))

    pickup_color = COLOR_PICKUP_READY if state["order_state"] == "READY" else COLOR_PICKUP
    pygame.draw.rect(screen, pickup_color, zones["pickup"], border_radius=8)
    pickup_text = font.render("ВЫДАЧА ЗАКАЗОВ", True, (40, 80, 120))
    screen.blit(pickup_text, (zones["pickup"].centerx - 75, zones["pickup"].centery - 10))

    pygame.draw.circle(
        screen,
        PLAYER_COLORS[state["player_color_index"]],
        (round(state["player_pos"].x), round(state["player_pos"].y)),
        state["player_radius"],
    )

def draw_ui(screen, state, zones, font, small_font, clock):
    ui_x, ui_y = 20, 20
    pygame.draw.rect(screen, (240, 240, 240), (10, 10, 260, 160), border_radius=8)
    pygame.draw.rect(screen, (200, 200, 200), (10, 10, 260, 160), width=2, border_radius=8)

    lines = [
        f"Money: {state['money']} ₽",
        f"Order: {state['current_product']['name'] if state['current_product'] else 'Нет'}",
        f"State: {state['order_state']}",
    ]
    
    if state["order_state"] == "WAITING":
        lines.append(f"Cooking: {state['cooking_time_left']:.1f} s")
    
    lines.append(f"FPS: {clock.get_fps():.0f}")

    for i, line in enumerate(lines):
        text_surf = font.render(line, True, COLOR_TEXT)
        screen.blit(text_surf, (ui_x, ui_y + i * 28))

    if state["order_state"] == "WAITING":
        bar_x, bar_y = ui_x, ui_y + 125
        bar_w, bar_h = 220, 16
        progress = 1.0 - (state["cooking_time_left"] / state["total_cook_time"])
        progress = max(0.0, min(1.0, progress))
        
        pygame.draw.rect(screen, (210, 210, 210), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(screen, (70, 170, 90), (bar_x, bar_y, int(bar_w * progress), bar_h), border_radius=4)

    player_rect = pygame.Rect(0, 0, state["player_radius"] * 2, state["player_radius"] * 2)
    player_rect.center = (round(state["player_pos"].x), round(state["player_pos"].y))

    prompt = ""
    if not state["menu_open"]:
        if player_rect.colliderect(zones["counter_interact"]) and state["order_state"] == "NO_ORDER":
            prompt = "E — сделать заказ"
        elif player_rect.colliderect(zones["pickup_interact"]) and state["order_state"] == "READY":
            prompt = "E — получить заказ"
        elif state["order_state"] == "DONE":
            prompt = "R — начать заново"

    if prompt:
        prompt_surf = font.render(prompt, True, (200, 80, 50))
        screen.blit(prompt_surf, (WINDOW_WIDTH // 2 - prompt_surf.get_width() // 2, WINDOW_HEIGHT - 50))

    if state["message"]:
        msg_surf = font.render(state["message"], True, (180, 50, 50))
        screen.blit(msg_surf, (WINDOW_WIDTH // 2 - msg_surf.get_width() // 2, 190))

    if state["menu_open"]:
        menu_w, menu_h = 360, 280
        menu_x = WINDOW_WIDTH // 2 - menu_w // 2
        menu_y = WINDOW_HEIGHT // 2 - menu_h // 2
        
        pygame.draw.rect(screen, COLOR_MENU_BG, (menu_x, menu_y, menu_w, menu_h), border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), (menu_x, menu_y, menu_w, menu_h), width=2, border_radius=10)
        
        title_surf = font.render("МЕНЮ ЗАКАЗА", True, COLOR_MENU_TEXT)
        screen.blit(title_surf, (menu_x + menu_w // 2 - title_surf.get_width() // 2, menu_y + 15))

        for i, prod in enumerate(PRODUCTS):
            y_offset = menu_y + 60 + i * 45
            stock_text = f"(Ост: {prod['stock']})" if prod['stock'] > 0 else "(Нет в наличии)"
            color = (150, 255, 150) if prod['stock'] > 0 else (255, 100, 100)
            
            item_text = f"{i + 1}. {prod['name']} - {prod['price']}₽ {stock_text}"
            item_surf = small_font.render(item_text, True, color)
            screen.blit(item_surf, (menu_x + 30, y_offset))

        hint_surf = small_font.render("Выберите 1-4 | ESC - закрыть", True, (180, 180, 180))
        screen.blit(hint_surf, (menu_x + menu_w // 2 - hint_surf.get_width() // 2, menu_y + menu_h - 35))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 22)

    state = get_initial_state()
    zones = get_zones()

    try:
        while state["running"]:
            dt = clock.tick(FPS) / 1000.0

            handle_events(state, zones)
            handle_movement(state, zones, dt)
            update_order(state, dt)
            
            draw_scene(screen, state, zones, font)
            draw_ui(screen, state, zones, font, small_font, clock)

            pygame.display.flip()
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()