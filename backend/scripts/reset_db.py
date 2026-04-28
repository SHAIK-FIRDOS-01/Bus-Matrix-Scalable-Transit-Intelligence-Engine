import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def reset_db():
    with connection.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            t_name = table[0]
            print(f"Dropping table {t_name}")
            cursor.execute(f"DROP TABLE `{t_name}`")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("Database reset complete.")


if __name__ == '__main__':
    reset_db()
