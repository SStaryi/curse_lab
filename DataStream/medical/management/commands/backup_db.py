from django.core.management.base import BaseCommand
import os
import datetime
import yadisk
import psycopg2

class Command(BaseCommand):
    help = 'Creates database backup and uploads to Yandex.Disk using SDK'

    def handle(self, *args, **options):
        self.backup_database()

    def backup_database(self):
        # Инициализируем клиент Яндекс.Диска
        y = yadisk.YaDisk(token='y0__wgBEIrF4rUBGNuWAyCyjffsEcJSRnMGb9uCE4u3EvcVynvlhNVY')
        
        # Проверяем токен
        if not y.check_token():
            print('Invalid Yandex.Disk token')
            return
            
        # Формируем имя файла с датой
        date = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'backup_{date}.sql'
        
        # Временная папка для бэкапа
        temp_dir = 'backups_temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        temp_path = os.path.join(temp_dir, filename)
        
        try:
            # Параметры подключения к БД
            conn = psycopg2.connect(
                dbname='education_db',
                user='postgres',
                password='22833649557',
                host='127.0.0.1',
                port='5432'
            )
            
            # Создаем бэкап
            with conn.cursor() as cursor:
                with open(temp_path, 'w', encoding='utf-8') as f:
                    # Получаем схему базы данных
                    cursor.execute("""
                        SELECT 
                            'DROP TABLE IF EXISTS ' || tablename || ' CASCADE;' 
                        FROM pg_tables 
                        WHERE schemaname = 'public';
                    """)
                    for result in cursor:
                        f.write(result[0] + '\n')
                    
                    # Получаем структуру таблиц
                    cursor.execute("""
                        SELECT tablename FROM pg_tables WHERE schemaname = 'public';
                    """)
                    tables = cursor.fetchall()
                    
                    for table in tables:
                        table_name = table[0]
                        cursor.execute(f"SELECT * FROM {table_name};")
                        rows = cursor.fetchall()
                        
                        if rows:
                            # Получаем имена колонок
                            col_names = [desc[0] for desc in cursor.description]
                            
                            # Записываем INSERT запросы
                            f.write(f"\n-- Table: {table_name}\n")
                            for row in rows:
                                values = [
                                    'NULL' if v is None else f"'{str(v)}'" 
                                    for v in row
                                ]
                                f.write(
                                    f"INSERT INTO {table_name} ({', '.join(col_names)}) "
                                    f"VALUES ({', '.join(values)});\n"
                                )
            
            print(f'Successfully created backup at {temp_path}')
            
            # Создаем папку на Яндекс.Диске если её нет
            if not y.exists('/backups'):
                y.mkdir('/backups')
            
            # Загружаем файл
            y.upload(temp_path, f'/backups/{filename}')
            print('Successfully uploaded to Yandex.Disk')
            
            # Удаляем временный файл
            os.remove(temp_path)
            
            # Очищаем старые бэкапы
            self.cleanup_old_backups(y)
            
        except Exception as e:
            print(f'Backup failed: {str(e)}')
            
    def cleanup_old_backups(self, y):
        """Оставляет только 5 последних бэкапов"""
        try:
            # Получаем список файлов
            files = list(y.listdir('/backups'))
            
            # Сортируем по дате изменения (новые первые)
            files.sort(key=lambda x: x.modified, reverse=True)
            
            # Удаляем старые файлы
            for file in files[5:]:
                y.remove(file.path)
                print(f'Removed old backup: {file.name}')
                
        except Exception as e:
            print(f'Cleanup failed: {str(e)}')

# Для запуска как отдельный скрипт
if __name__ == '__main__':
    command = Command()
    command.backup_database() 