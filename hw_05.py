from pathlib import Path
from timeit import timeit

from tabulate import tabulate

BASE_DIR = Path(__file__).resolve().parent
ITERATIONS = 1000


def read_text(filename):
    """Читає файл з урахуванням можливих кодувань."""
    path = BASE_DIR / filename

    for encoding in ("utf-8", "cp1251"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Не вдалося прочитати файл {filename}")


def boyer_moore_search(text, pattern):
    if not pattern:
        return 0

    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length > text_length:
        return -1

    last_occurrence = {char: index for index, char in enumerate(pattern)}
    index = 0

    while index <= text_length - pattern_length:
        pattern_index = pattern_length - 1

        while pattern_index >= 0 and pattern[pattern_index] == text[index + pattern_index]:
            pattern_index -= 1

        if pattern_index < 0:
            return index

        bad_char = text[index + pattern_index]
        index += max(1, pattern_index - last_occurrence.get(bad_char, -1))

    return -1


def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    index = 1

    while index < len(pattern):
        if pattern[index] == pattern[length]:
            length += 1
            lps[index] = length
            index += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[index] = 0
            index += 1

    return lps


def kmp_search(text, pattern):
    if not pattern:
        return 0

    lps = build_lps(pattern)
    text_index = 0
    pattern_index = 0

    while text_index < len(text):
        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1

            if pattern_index == len(pattern):
                return text_index - pattern_index

        elif pattern_index != 0:
            pattern_index = lps[pattern_index - 1]
        else:
            text_index += 1

    return -1


def rabin_karp_search(text, pattern):
    if not pattern:
        return 0

    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length > text_length:
        return -1

    base = 256
    modulus = 101
    pattern_hash = 0
    window_hash = 0
    high_order = 1

    for _ in range(pattern_length - 1):
        high_order = (high_order * base) % modulus

    for index in range(pattern_length):
        pattern_hash = (base * pattern_hash + ord(pattern[index])) % modulus
        window_hash = (base * window_hash + ord(text[index])) % modulus

    for index in range(text_length - pattern_length + 1):
        if pattern_hash == window_hash and text[index : index + pattern_length] == pattern:
            return index

        if index < text_length - pattern_length:
            window_hash = (
                base * (window_hash - ord(text[index]) * high_order)
                + ord(text[index + pattern_length])
            ) % modulus

    return -1


def measure_algorithm(algorithm, text, pattern):
    total_time = timeit(lambda: algorithm(text, pattern), number=ITERATIONS)
    return total_time / ITERATIONS


def run_benchmarks():
    texts = {
        "1.txt": read_text("1.txt"),
        "2.txt": read_text("2.txt"),
    }

    patterns = {
        "1.txt": {
            "наявний": "алгоритми та структури даних",
            "вигаданий": "вигаданий підрядок якого точно немає у першому тексті",
        },
        "2.txt": {
            "наявний": "рекомендаційної системи",
            "вигаданий": "вигаданий підрядок якого точно немає у другому тексті",
        },
    }

    algorithms = {
        "Боєра-Мура": boyer_moore_search,
        "Кнута-Морріса-Пратта": kmp_search,
        "Рабіна-Карпа": rabin_karp_search,
    }

    results = {}

    for filename, text in texts.items():
        results[filename] = {}

        for pattern_type, pattern in patterns[filename].items():
            results[filename][pattern_type] = {}

            for algorithm_name, algorithm in algorithms.items():
                found_index = algorithm(text, pattern)
                elapsed = measure_algorithm(algorithm, text, pattern)

                results[filename][pattern_type][algorithm_name] = {
                    "time": elapsed,
                    "index": found_index,
                }

    return results


def find_fastest_for_file(pattern_results):
    return min(
        (
            (data["time"], algorithm_name, pattern_type)
            for pattern_type, algorithm_results in pattern_results.items()
            for algorithm_name, data in algorithm_results.items()
        ),
        key=lambda item: item[0],
    )


def find_fastest_overall(results):
    return min(
        (
            (data["time"], algorithm_name, filename, pattern_type)
            for filename, pattern_results in results.items()
            for pattern_type, algorithm_results in pattern_results.items()
            for algorithm_name, data in algorithm_results.items()
        ),
        key=lambda item: item[0],
    )


def print_results(results):
    for filename, pattern_results in results.items():
        rows = []

        for pattern_type, algorithm_results in pattern_results.items():
            for algorithm_name, data in algorithm_results.items():
                rows.append(
                    [
                        pattern_type,
                        algorithm_name,
                        f"{data['time']:.8f}",
                        data["index"],
                    ]
                )

        print(f"\n{'=' * 80}")
        print(f"{filename:^80}")
        print(f"{'=' * 80}")

        table = tabulate(
            rows,
            headers=["Підрядок", "Алгоритм", "Середній час, сек", "Індекс"],
            tablefmt="fancy_grid",
            stralign="center",
            numalign="center",
        )

        print(table)

        fastest = find_fastest_for_file(pattern_results)

        print(
            f"\n🏆 Найшвидший алгоритм для {filename}: "
            f"{fastest[1]} "
            f"({fastest[2]}, {fastest[0]:.8f} сек)"
        )


def print_overall_result(results):
    fastest = find_fastest_overall(results)

    print(f"\n{'=' * 80}")
    print(f"{'ЗАГАЛЬНИЙ РЕЗУЛЬТАТ':^80}")
    print(f"{'=' * 80}")

    print(
        f"🏆 Найшвидший алгоритм в цілому: "
        f"{fastest[1]} "
        f"({fastest[2]}, {fastest[3]}, {fastest[0]:.8f} сек)"
    )


if __name__ == "__main__":
    benchmark_results = run_benchmarks()
    print_results(benchmark_results)
    print_overall_result(benchmark_results)