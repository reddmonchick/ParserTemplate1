import redis

# Подключение к серверу Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Проверка наличия ключа
