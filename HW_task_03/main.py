import os
import re

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
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parsed_line = parse_log_line(line)
            if parsed_line:
                logs.append(parsed_line)
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log['level'] == level.strip().upper()]

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
    # log_file_path = "my_log_error.log"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(script_dir, "my_log_error.log")
    print(f"Аналіз файлу: {log_file_path}\n")

    logs = load_logs(log_file_path)

    if logs:
        counts = count_logs_by_level(logs)
        display_log_counts(counts)
        print()

        for level in counts.keys():
            print(f"Деталі логів для рівня '{level}':")

            filtered_logs = filter_logs_by_level(logs, level)

            for log in filtered_logs:
                print(f"{log['date']} {log['time']} - {log['message']}")
