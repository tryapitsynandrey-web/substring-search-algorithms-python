from pathlib import Path
from timeit import timeit


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
    raise UnicodeDecodeError(f"Не вдалося прочитати файл {filename}")


def boyer_moore_search(text, pattern):
    if not pattern:
        return 0

    pattern_length = len(pattern)
    text_length = len(text)
    if pattern_length > text_length:
        return -1

    # Таблиця зміщень для правила поганого символу.
    shift = {char: pattern_length - index - 1 for index, char in enumerate(pattern[:-1])}
    index = 0

    while index <= text_length - pattern_length:
        pattern_index = pattern_length - 1

        while pattern_index >= 0 and pattern[pattern_index] == text[index + pattern_index]:
            pattern_index -= 1

        if pattern_index < 0:
            return index

        bad_char = text[index + pattern_length - 1]
        index += shift.get(bad_char, pattern_length)

    return -1


def build_lps(pattern):
    # LPS зберігає довжину найдовшого префікса, який є суфіксом.
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

    # Множник для видалення першого символу з rolling hash.
    for _ in range(pattern_length - 1):
        high_order = (high_order * base) % modulus

    for index in range(pattern_length):
        pattern_hash = (base * pattern_hash + ord(pattern[index])) % modulus
        window_hash = (base * window_hash + ord(text[index])) % modulus

    for index in range(text_length - pattern_length + 1):
        if pattern_hash == window_hash and text[index:index + pattern_length] == pattern:
            return index

        if index < text_length - pattern_length:
            window_hash = (
                base * (window_hash - ord(text[index]) * high_order)
                + ord(text[index + pattern_length])
            ) % modulus

    return -1


def measure_algorithm(algorithm, text, pattern):
    # timeit запускає однаковий пошук багато разів для стабільнішого заміру.
    return timeit(lambda: algorithm(text, pattern), number=ITERATIONS)


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


def print_results(results):
    for filename, pattern_results in results.items():
        print(f"\n{filename}")
        print("| Підрядок | Алгоритм | Час, сек | Індекс |")
        print("|---|---|---:|---:|")
        for pattern_type, algorithm_results in pattern_results.items():
            for algorithm_name, data in algorithm_results.items():
                print(
                    f"| {pattern_type} | {algorithm_name} | "
                    f"{data['time']:.6f} | {data['index']} |"
                )

        fastest = min(
            (
                (data["time"], algorithm_name, pattern_type)
                for pattern_type, algorithm_results in pattern_results.items()
                for algorithm_name, data in algorithm_results.items()
            ),
            key=lambda item: item[0],
        )
        print(
            f"Найшвидший для {filename}: {fastest[1]} "
            f"({fastest[2]}, {fastest[0]:.6f} сек)"
        )


if __name__ == "__main__":
    benchmark_results = run_benchmarks()
    print_results(benchmark_results)
