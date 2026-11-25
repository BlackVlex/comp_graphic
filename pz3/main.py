# main.py — окно, event loop, переключение режимов

import sys
import random
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, STEP_DELAY_MS,
    MIN_ELEMENTS, MAX_ELEMENTS, MIN_VALUE, MAX_VALUE,
)
from algorithms import bubble_sort_steps, selection_sort_steps, binary_search_steps
from visualizer import Visualizer


ALGO_NAMES = {
    1: "Bubble Sort",
    2: "Selection Sort",
    3: "Binary Search",
}


def generate_array():
    n = random.randint(MIN_ELEMENTS, MAX_ELEMENTS)
    return [random.randint(MIN_VALUE, MAX_VALUE) for _ in range(n)]


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("ПР-3: Визуализация алгоритмов")
        self.clock = pygame.time.Clock()
        self.vis = Visualizer(self.screen)

        self.arr = generate_array()
        self.mode = 1  # 1 — bubble, 2 — selection, 3 — binary
        self.gen = None
        self.current_step = None
        self.running = False
        self.finished = False
        self.step_timer = 0
        self.target = None
        self.target_input = ""
        self.typing_target = False

        self._start_algo()

    # ---------- управление алгоритмом ----------
    def _start_algo(self):
        self.finished = False
        self.running = False
        self.step_timer = 0

        if self.mode == 1:
            self.gen = bubble_sort_steps(self.arr)
        elif self.mode == 2:
            self.gen = selection_sort_steps(self.arr)
        elif self.mode == 3:
            # бинарный поиск — нужен отсортированный массив
            sorted_arr = sorted(self.arr)
            if self.target is None:
                self.target = random.choice(sorted_arr)
            self.gen = binary_search_steps(sorted_arr, self.target)

        self._next_step()

    def _next_step(self):
        if self.gen is None:
            return
        try:
            step = next(self.gen)
            self.current_step = step
            if step.get("finished"):
                self.finished = True
                self.running = False
        except StopIteration:
            self.finished = True
            self.running = False

    def _reset_array(self):
        if self.running:
            return  # по ТЗ: нельзя сбрасывать во время выполнения
        self.arr = generate_array()
        self.target = None
        self._start_algo()

    def _set_mode(self, mode):
        self.mode = mode
        self._start_algo()

    # ---------- обработка ввода target ----------
    def _apply_target(self):
        try:
            self.target = int(self.target_input)
        except ValueError:
            self.target = None
        self.typing_target = False
        self.target_input = ""
        self._start_algo()

    # ---------- event loop ----------
    def run(self):
        while True:
            dt = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    # Режимы
                    elif event.key == pygame.K_1:
                        self._set_mode(1)
                    elif event.key == pygame.K_2:
                        self._set_mode(2)
                    elif event.key == pygame.K_3:
                        self._set_mode(3)

                    # Управление
                    elif event.key == pygame.K_SPACE:
                        if not self.finished:
                            self.running = not self.running
                    elif event.key == pygame.K_n:
                        if not self.finished:
                            self._next_step()
                    elif event.key == pygame.K_r:
                        self._reset_array()

                    # Target для бинарного поиска
                    elif event.key == pygame.K_t and self.mode == 3:
                        self.typing_target = True
                        self.target_input = ""
                    elif event.key == pygame.K_f and self.mode == 3:
                        self.target = random.randint(MIN_VALUE, MAX_VALUE)
                        self._start_algo()

                    # Ввод цифр target
                    elif self.typing_target:
                        if event.key == pygame.K_RETURN:
                            self._apply_target()
                        elif event.key == pygame.K_BACKSPACE:
                            self.target_input = self.target_input[:-1]
                        elif event.unicode.isdigit():
                            self.target_input += event.unicode
                            if len(self.target_input) > 5:
                                self.target_input = self.target_input[:5]
                        elif event.key == pygame.K_ESCAPE:
                            self.typing_target = False

            # Авто-шаг по таймеру
            if self.running and not self.finished:
                self.step_timer += dt
                if self.step_timer >= STEP_DELAY_MS:
                    self.step_timer = 0
                    self._next_step()

            # Отрисовка
            if self.current_step is not None:
                self.vis.draw_all(
                    ALGO_NAMES[self.mode],
                    self.current_step["array"],
                    self.current_step["states"],
                    self.current_step["stats"],
                    self.current_step.get("message", ""),
                )
            else:
                self.vis.clear()

            # Подсказка ввода target
            if self.typing_target:
                prompt = f"Введи target и нажми Enter: {self.target_input}_"
                surf = self.vis.font.render(prompt, True, (255, 220, 80))
                self.screen.blit(surf, (20, 50))

            pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()