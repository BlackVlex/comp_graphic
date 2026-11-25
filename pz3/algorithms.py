# algorithms.py — алгоритмы в виде генераторов шагов
# НЕ импортирует pygame!

def bubble_sort_steps(values):
    """Пузырьковая сортировка. Возвращает состояние на каждом шаге."""
    arr = values[:]
    n = len(arr)
    states = ["default"] * n
    comparisons = 0
    swaps = 0
    passes = 0
    steps = 0

    for i in range(n):
        swapped = False
        passes += 1
        for j in range(0, n - i - 1):
            # Подсветка сравниваемых
            cur_states = states[:]
            cur_states[j] = "compare"
            cur_states[j + 1] = "compare"
            # Отсортированная часть справа
            for k in range(n - i, n):
                cur_states[k] = "sorted"
            yield {
                "array": arr[:],
                "states": cur_states,
                "stats": {
                    "Comparisons": comparisons,
                    "Swaps": swaps,
                    "Pass": passes,
                    "Steps": steps,
                },
                "message": f"Сравнение arr[{j}] и arr[{j+1}]",
            }
            steps += 1
            comparisons += 1

            if arr[j] > arr[j + 1]:
                # Подсветка обмена
                swap_states = states[:]
                swap_states[j] = "swap"
                swap_states[j + 1] = "swap"
                for k in range(n - i, n):
                    swap_states[k] = "sorted"
                yield {
                    "array": arr[:],
                    "states": swap_states,
                    "stats": {
                        "Comparisons": comparisons,
                        "Swaps": swaps,
                        "Pass": passes,
                        "Steps": steps,
                    },
                    "message": f"Обмен arr[{j}] и arr[{j+1}]",
                }
                steps += 1
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True

        # Фиксируем отсортированный элемент
        states[n - i - 1] = "sorted"

        # Раннее завершение
        if not swapped:
            for k in range(n):
                states[k] = "sorted"
            yield {
                "array": arr[:],
                "states": states[:],
                "stats": {
                    "Comparisons": comparisons,
                    "Swaps": swaps,
                    "Pass": passes,
                    "Steps": steps,
                },
                "message": "Раннее завершение — массив отсортирован",
                "finished": True,
            }
            return

    # Финальный кадр
    yield {
        "array": arr[:],
        "states": ["sorted"] * n,
        "stats": {
            "Comparisons": comparisons,
            "Swaps": swaps,
            "Pass": passes,
            "Steps": steps,
        },
        "message": "Сортировка завершена",
        "finished": True,
    }


def selection_sort_steps(values):
    """Сортировка выбором."""
    arr = values[:]
    n = len(arr)
    states = ["default"] * n
    comparisons = 0
    swaps = 0
    passes = 0
    steps = 0

    for i in range(n):
        passes += 1
        min_idx = i
        states = ["sorted"] * i + ["default"] * (n - i)
        states[i] = "min"

        for j in range(i + 1, n):
            cur_states = states[:]
            cur_states[j] = "compare"
            yield {
                "array": arr[:],
                "states": cur_states,
                "stats": {
                    "Comparisons": comparisons,
                    "Swaps": swaps,
                    "Pass": passes,
                    "Steps": steps,
                },
                "message": f"Ищем минимум, сравниваем с arr[{j}]",
            }
            steps += 1
            comparisons += 1

            if arr[j] < arr[min_idx]:
                min_idx = j
                states[min_idx] = "min"

        # Обмен
        if min_idx != i:
            swap_states = states[:]
            swap_states[i] = "swap"
            swap_states[min_idx] = "swap"
            yield {
                "array": arr[:],
                "states": swap_states,
                "stats": {
                    "Comparisons": comparisons,
                    "Swaps": swaps,
                    "Pass": passes,
                    "Steps": steps,
                },
                "message": f"Обмен arr[{i}] и arr[{min_idx}]",
            }
            steps += 1
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1

        states[i] = "sorted"

    yield {
        "array": arr[:],
        "states": ["sorted"] * n,
        "stats": {
            "Comparisons": comparisons,
            "Swaps": swaps,
            "Pass": passes,
            "Steps": steps,
        },
        "message": "Сортировка завершена",
        "finished": True,
    }


def binary_search_steps(values, target):
    """Бинарный поиск по отсортированному массиву."""
    arr = values[:]
    n = len(arr)
    left = 0
    right = n - 1
    steps = 0
    comparisons = 0
    states = ["default"] * n

    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        steps += 1

        cur_states = ["excluded"] * n
        for k in range(left, right + 1):
            cur_states[k] = "range"
        cur_states[mid] = "mid"

        yield {
            "array": arr[:],
            "states": cur_states,
            "stats": {
                "Target": target,
                "Comparisons": comparisons,
                "Steps": steps,
                "Current range": f"[{left}, {right}]",
                "Result": "поиск...",
            },
            "message": f"mid={mid}, arr[mid]={arr[mid]}",
        }

        if arr[mid] == target:
            cur_states[mid] = "found"
            yield {
                "array": arr[:],
                "states": cur_states,
                "stats": {
                    "Target": target,
                    "Comparisons": comparisons,
                    "Steps": steps,
                    "Current range": f"[{left}, {right}]",
                    "Result": f"Element found: index {mid}",
                },
                "message": f"Найдено: arr[{mid}] = {target}",
                "finished": True,
            }
            return
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # Не найдено
    yield {
        "array": arr[:],
        "states": ["excluded"] * n,
        "stats": {
            "Target": target,
            "Comparisons": comparisons,
            "Steps": steps,
            "Current range": "пусто",
            "Result": "Element not found",
        },
        "message": f"Элемент {target} не найден",
        "finished": True,
    }