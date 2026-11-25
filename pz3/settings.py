# settings.py — настройки, цвета, размеры, константы

# Размеры окна
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750
FPS = 60

# Область визуализации массива
ARRAY_AREA_X = 40
ARRAY_AREA_Y = 100
ARRAY_AREA_WIDTH = 1120
ARRAY_AREA_HEIGHT = 450

# Панель статистики
STATS_X = 40
STATS_Y = 580

# Параметры массива
MIN_ELEMENTS = 30
MAX_ELEMENTS = 30
MIN_VALUE = 10
MAX_VALUE = 100

# Скорость (мс между шагами алгоритма)
STEP_DELAY_MS = 80

# Цвета
BG_COLOR = (25, 25, 35)
TEXT_COLOR = (230, 230, 230)
PANEL_BG = (40, 40, 55)

# Цвета состояний элементов
COLOR_DEFAULT = (120, 140, 180)       # обычный
COLOR_COMPARE = (255, 220, 80)        # сравниваемый
COLOR_SWAP = (255, 90, 90)            # обмен
COLOR_MIN = (180, 80, 255)            # выбранный минимум
COLOR_SORTED = (80, 220, 120)         # отсортированный
COLOR_RANGE = (80, 180, 255)          # активный диапазон бинарного поиска
COLOR_MID = (255, 150, 50)            # mid в бинарном поиске
COLOR_FOUND = (255, 255, 100)         # найденный элемент
COLOR_EXCLUDED = (60, 60, 80)         # исключённый

# Заголовок
TITLE = "Визуализация: Bubble Sort / Selection Sort / Binary Search"