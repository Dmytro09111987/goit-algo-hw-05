import os
import re
import sys

def parse_log_line(line: str) -> dict:
    match = re.match(r'^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\s*[A-Za-z]+)\s+(.+)$', line.strip())
    if match:
        return {
            'date': match.group(1),
            'time': match.group(2),
            'level': match.group(3).strip().upper(),
            'message': match.group(4)
        }
    return {}

def load_logs(file_path: str) -> list:
    logs = []
    if not os.path.exists(file_path):
        print(f"Помилка: Файл {file_path} не знайдено.")
        return logs
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parsed_line = parse_log_line(line)
                if parsed_line:
                    logs.append(parsed_line)
    except Exception as e:
        print(f"Помилка при читанні файлу {file_path}: {e}")
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    target_level = level.strip().upper()
    return [log for log in logs if log['level'] == target_level]

def count_logs_by_level(logs: list) -> dict:
    counts = {}
    for log in logs:
        level = log['level']
        counts[level] = counts.get(level, 0) + 1
    return counts

def display_log_counts(counts: dict):
    col_level_width = 17
    col_count_width = 9
    print(f"{'Рівень логування':<{col_level_width}} | {'Кількість':<{col_count_width}}")
    print("-" * col_level_width + "-|-" + "-" * col_count_width)
    for level, count in counts.items():
        print(f"{level:<{col_level_width}} | {count:<{col_count_width}}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Помилка: за вказаним шляхом файл не знайдено.")
        sys.exit(1)

    log_file_path = sys.argv[1]
    filter_level = sys.argv[2].strip() if len(sys.argv) > 2 else None
    logs = load_logs(log_file_path)

    if logs:
        counts = count_logs_by_level(logs)
        display_log_counts(counts)

        if filter_level:
            print()
            filtered_logs = filter_logs_by_level(logs, filter_level)

            if filter_level in counts:
                print(f"Деталі логів для рівня '{filter_level}':")
                for log in filtered_logs:
                    print(f"{log['date']} {log['time']} - {log['message']}")
            else:
                print(f"Рівень логування '{filter_level}' не знайдено у файлі.")