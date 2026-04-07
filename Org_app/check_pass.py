import hashlib
import binascii

def verify_django_hash(password, django_hash):
    # 1. Разбираем строку на части
    algorithm, iterations, salt, hash_val = django_hash.split('$')
    iterations = int(iterations)

    # 2. Преобразуем пароль в байты
    password_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')

    # 3. Вычисляем проверочный хеш (PBKDF2 SHA256)
    # По умолчанию Django использует длину ключа 32 байта
    dk = hashlib.pbkdf2_hmac(
        'sha256', 
        password_bytes, 
        salt_bytes, 
        iterations
    )

    # 4. Кодируем результат в Base64 (как это делает Django)
    calc_hash = binascii.b2a_base64(dk).decode('ascii').strip()

    # 5. Сравниваем результат
    return calc_hash == hash_val

# Данные для проверки
stored_hash = "pbkdf2_sha256$1200000$2ynFayP62ntxCTDJI4AOsG$NyIspGuP+DnDPyPCbrATuvwYOZXtOyF9ZI22Lq97BxA="
test_password = "asliddin_2002"

if verify_django_hash(test_password, stored_hash):
    print("✅ Пароль верный!")
else:
    print("❌ Пароль не подходит.")