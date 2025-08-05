import asyncio
import shutil
import os
from pathlib import Path
import argparse
import logging

# Налаштування логування
logging.basicConfig(
    filename='file_sorter.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Асинхронна функція для копіювання одного файлу
async def copy_file(file_path: Path, output_dir: Path):
    try:
        ext = file_path.suffix.lower().lstrip('.') or "no_extension"
        target_dir = output_dir / ext
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / file_path.name

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, shutil.copy2, file_path, target_file)
    except Exception as e:
        logging.error(f"Помилка при копіюванні {file_path}: {e}")

# Асинхронна функція для читання папки та запуску копіювання файлів
async def read_folder(source_dir: Path, output_dir: Path):
    tasks = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, output_dir))
    await asyncio.gather(*tasks)

# Основний блок
def main():
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширеннями.")
    parser.add_argument("source", help="Шлях до вихідної папки.")
    parser.add_argument("output", help="Шлях до цільової папки.")
    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    output_dir = Path(args.output).resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Вихідна папка не існує: {source_dir}")
        return

    try:
        asyncio.run(read_folder(source_dir, output_dir))
        print("Сортування завершено успішно.")
    except Exception as e:
        logging.error(f"Глобальна помилка: {e}")
        print("Сталася помилка. Перевірте лог для деталей.")

# Запуск скрипта
if __name__ == "__main__":
    main()
