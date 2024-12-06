import boto3

# Укажите ваши ключи
ACCESS_KEY = "h6E9GzDHv6fqujJHrDUqna"
SECRET_KEY = "8sgjRzj4cEF2x9yoiE2zsrhD9XfNg3yuwGvHKf2qMrCS"
ENDPOINT_URL = "https://testbucketabay.hb.kz-ast.bizmrg.com/"

# Инициализация клиента S3 с кастомным endpoint
s3_client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url=ENDPOINT_URL
)

# Имя бакета
bucket_name = "testbucketabay"
# Локальный файл, который вы хотите загрузить
file_path = "local_file.txt"  # Замените на путь к вашему файлу
# Имя файла, которое будет в S3
s3_file_name = "uploaded_file.txt"

# Загрузка файла
try:
    s3_client.upload_file(file_path, bucket_name, s3_file_name)
    print(f"Файл {file_path} успешно загружен в бакет {bucket_name} как {s3_file_name}")
except Exception as e:
    print(f"Ошибка при загрузке файла: {e}")
