import os
import subprocess
from datetime import datetime
import logging
from dotenv import load_dotenv

# Загрузка .env файла
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=env_path)

# Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Параметры бэкапа
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "../backups")
BACKUP_FORMAT = os.environ.get("BACKUP_FORMAT", "sql")  # Возможные значения: "sql", "json", "custom", "sqlite"

# Настройка базы данных
DB_ENGINE = os.environ.get("DB_ENGINE", "postgresql")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")

# Создание папки для бэкапов
os.makedirs(BACKUP_DIR, exist_ok=True)

# Форматирование имени файла
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_file = os.path.join(BACKUP_DIR, f"astrawood_backup_{timestamp}")

# Проверка обязательных переменных окружения
required_vars = ["POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT"]
for var in required_vars:
    if not os.environ.get(var):
        logger.error(f"Переменная окружения {var} не установлена!")
        raise EnvironmentError(f"Переменная окружения {var} не установлена!")

# Функции для каждого типа базы данных
def backup_postgresql():
    os.environ["PGPASSWORD"] = DB_PASSWORD
    if BACKUP_FORMAT == "sql":
        return [
            "pg_dump",
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-F", "p",
            "-f", f"{backup_file}.sql",
            DB_NAME,
        ]
    elif BACKUP_FORMAT == "json":
        return [
            "pg_dump",
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "--data-only",
            "--column-inserts",
            "--file", f"{backup_file}.json",
            DB_NAME,
        ]
    elif BACKUP_FORMAT == "custom":
        return [
            "pg_dump",
            "-h", DB_HOST,
            "-p", DB_PORT,
            "-U", DB_USER,
            "-F", "c",
            "-f", f"{backup_file}.dump",
            DB_NAME,
        ]
    else:
        raise ValueError("Неподдерживаемый формат для PostgreSQL!")

def backup_sqlite():
    if BACKUP_FORMAT == "sqlite":
        return f"sqlite3 {DB_NAME} '.backup {backup_file}.db'"
    else:
        raise ValueError("SQLite поддерживает только sqlite формат!")

# Выбор команды
try:
    if DB_ENGINE == "postgresql":
        command = backup_postgresql()
    elif DB_ENGINE == "sqlite":
        command = backup_sqlite()
    else:
        raise ValueError("Неподдерживаемый движок базы данных!")

    # Выполнение команды
    if isinstance(command, list):
        subprocess.run(command, check=True)
    else:  # SQLite команда в строковом формате
        subprocess.run(command, shell=True, check=True)

    logger.info(f"Бэкап успешно создан: {backup_file}.{BACKUP_FORMAT}")

except subprocess.CalledProcessError as e:
    logger.error(f"Ошибка выполнения команды: {e}")
    raise

# Печать параметров базы данных
logger.info("Параметры базы данных:")
logger.info(f"DB_ENGINE: {DB_ENGINE}")
logger.info(f"DB_NAME: {DB_NAME}")
logger.info(f"DB_USER: {DB_USER}")
logger.info(f"DB_HOST: {DB_HOST}")
logger.info(f"DB_PORT: {DB_PORT}")
logger.info(f"BACKUP_FORMAT: {BACKUP_FORMAT}")
logger.info(f"BACKUP_FILE: {backup_file}")
