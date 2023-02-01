import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    pep_status_count = defaultdict(int)
    total_pep_count = 0

    def open_spider(self, spider):
        """Создает путь до директории results."""
        result_dir = BASE_DIR / 'results'
        result_dir.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        """Считает количество статусов."""
        if item.get('status'):
            self.total_pep_count += 1
            self.pep_status_count[
                item['status']] = self.pep_status_count.get(
                item['status'], 0) + 1

        return item

    def close_spider(self, spider):
        """Записывает результы в csv-файл."""
        results = [('Cтатус', 'Количество')]
        results.extend(self.pep_status_count.items())
        results.append(('Total: ', self.total_pep_count))

        file_format = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f'status_summary_{file_format}.csv'
        file_path = BASE_DIR / 'results' / file_name

        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(results)
