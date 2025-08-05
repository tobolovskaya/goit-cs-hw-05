import requests
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt


# Завантажити текст із URL
def download_text(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


# Map: обробка блоку тексту та підрахунок слів у ньому
def map_function(text_block: str) -> Counter:
    words = re.findall(r'\b\w+\b', text_block.lower())
    return Counter(words)


# Reduce: об'єднання результатів усіх мапперів
def reduce_function(counters) -> Counter:
    total = Counter()
    for counter in counters:
        total.update(counter)
    return total


# Візуалізація топ слів
def visualize_top_words(word_counter: Counter, top_n: int = 10):
    most_common = word_counter.most_common(top_n)
    words, counts = zip(*most_common)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color="skyblue")
    plt.title(f"Top {top_n} Words by Frequency")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Головна функція
def main():
    url = input("Введіть URL тексту: ").strip()

    try:
        text = download_text(url)
    except Exception as e:
        print(f"Помилка при завантаженні тексту: {e}")
        return

    # Розділимо текст на блоки для паралельної обробки
    block_size = 5000  # символів
    text_blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]

    with ThreadPoolExecutor() as executor:
        mapped = list(executor.map(map_function, text_blocks))

    word_counter = reduce_function(mapped)
    visualize_top_words(word_counter, top_n=10)


if __name__ == "__main__":
    main()
