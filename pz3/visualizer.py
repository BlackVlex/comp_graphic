# visualizer.py — отрисовка массива, статистики, легенды, подсказок

import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, ARRAY_AREA_X, ARRAY_AREA_Y,
    ARRAY_AREA_WIDTH, ARRAY_AREA_HEIGHT, STATS_X, STATS_Y,
    BG_COLOR, TEXT_COLOR, PANEL_BG,
    COLOR_DEFAULT, COLOR_COMPARE, COLOR_SWAP, COLOR_MIN,
    COLOR_SORTED, COLOR_RANGE, COLOR_MID, COLOR_FOUND, COLOR_EXCLUDED,
    TITLE,
)

STATE_COLORS = {
    "default": COLOR_DEFAULT,
    "compare": COLOR_COMPARE,
    "swap": COLOR_SWAP,
    "min": COLOR_MIN,
    "sorted": COLOR_SORTED,
    "range": COLOR_RANGE,
    "mid": COLOR_MID,
    "found": COLOR_FOUND,
    "excluded": COLOR_EXCLUDED,
}

LEGEND = [
    ("Обычный", COLOR_DEFAULT),
    ("Сравнение", COLOR_COMPARE),
    ("Обмен", COLOR_SWAP),
    ("Минимум", COLOR_MIN),
    ("Отсортирован", COLOR_SORTED),
    ("Диапазон", COLOR_RANGE),
    ("mid", COLOR_MID),
    ("Найден", COLOR_FOUND),
    ("Исключён", COLOR_EXCLUDED),
]


class Visualizer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", 18)
        self.big_font = pygame.font.SysFont("consolas", 26, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 14)

    def clear(self):
        self.screen.fill(BG_COLOR)

    def draw_title(self, algo_name):
        title_surf = self.big_font.render(f"{TITLE}   |   Режим: {algo_name}", True, TEXT_COLOR)
        self.screen.blit(title_surf, (20, 15))

    def draw_array(self, arr, states):
        if not arr:
            return
        n = len(arr)
        max_val = max(arr) if arr else 1
        col_width = ARRAY_AREA_WIDTH // n
        bar_width = max(2, col_width - 4)

        for i, (val, state) in enumerate(zip(arr, states)):
            color = STATE_COLORS.get(state, COLOR_DEFAULT)
            height = int((val / max_val) * (ARRAY_AREA_HEIGHT - 30))
            x = ARRAY_AREA_X + i * col_width + 2
            y = ARRAY_AREA_Y + ARRAY_AREA_HEIGHT - height
            pygame.draw.rect(self.screen, color, (x, y, bar_width, height))

            # Число над столбцом, если элементов немного
            if n <= 35:
                num_surf = self.small_font.render(str(val), True, TEXT_COLOR)
                self.screen.blit(num_surf, (x, y - 16))

    def draw_stats(self, stats):
        pygame.draw.rect(self.screen, PANEL_BG,
                         (STATS_X - 10, STATS_Y - 10,
                          WINDOW_WIDTH - 60, 90), border_radius=8)
        y = STATS_Y
        for key, value in stats.items():
            text = f"{key}: {value}"
            surf = self.font.render(text, True, TEXT_COLOR)
            self.screen.blit(surf, (STATS_X, y))
            y += 22

    def draw_legend(self):
        x = WINDOW_WIDTH - 200
        y = 60
        pygame.draw.rect(self.screen, PANEL_BG,
                         (x - 10, y - 10, 190, len(LEGEND) * 18 + 20), border_radius=8)
        title = self.font.render("Легенда:", True, TEXT_COLOR)
        self.screen.blit(title, (x, y))
        y += 22
        for name, color in LEGEND:
            pygame.draw.rect(self.screen, color, (x, y, 14, 14))
            txt = self.small_font.render(name, True, TEXT_COLOR)
            self.screen.blit(txt, (x + 20, y))
            y += 18

    def draw_controls(self):
        lines = [
            "1 — Bubble Sort    2 — Selection Sort    3 — Binary Search",
            "SPACE — Start/Pause    N — Next step    R — New array    Esc — Exit",
            "T — ввести target (Binary Search)    F — случайный target",
        ]
        y = WINDOW_HEIGHT - 70
        for line in lines:
            surf = self.small_font.render(line, True, (180, 180, 200))
            self.screen.blit(surf, (20, y))
            y += 18

    def draw_message(self, message):
        if message:
            surf = self.font.render(message, True, (255, 255, 150))
            self.screen.blit(surf, (ARRAY_AREA_X, ARRAY_AREA_Y + ARRAY_AREA_HEIGHT + 10))

    def draw_all(self, algo_name, arr, states, stats, message):
        self.clear()
        self.draw_title(algo_name)
        self.draw_array(arr, states)
        self.draw_stats(stats)
        self.draw_legend()
        self.draw_controls()
        self.draw_message(message)