# BatchMessageConsumer
# считывает минимум по 10 сообщений за один poll, обрабатывает сообщения в цикле и один раз коммитит оффсет после обработки пачки
from confluent_kafka import Consumer, serialization, DeserializingConsumer

MIN_COMMIT_COUNT = 10

str_deserializer = serialization.StringDeserializer("utf_8")

# Настройка консьюмера – адрес сервера
conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "group-tst-batch",        # Уникальный идентификатор группы
    "enable.auto.commit": False,          # Автоматический коммит смещений
    "auto.offset.reset": "earliest",      # Начало чтения с самого начала
    "key.deserializer": str_deserializer,
    "value.deserializer": str_deserializer
}
# Создание консьюмера
#consumer = Consumer(conf)
consumer = DeserializingConsumer(conf)

# Подписка на топик
consumer.subscribe(["topic-tst-1"])

# Чтение сообщений
running = True
msg_count = 0
try:
    while running:
        # Получение сообщений
        msg = consumer.poll(1.0)  # poll timeout = 1s

        if msg is None:
            continue
        if msg.error():
            print(f"Ошибка: {msg.error()}")
            running = False
            continue

        #key = msg.key().decode("utf-8")
        #value = msg.value().decode("utf-8")
        key = msg.key()
        value = msg.value()
        print(f"Получено сообщение: {key=}, {value=}, offset={msg.offset()}")
        msg_count += 1
        if msg_count % MIN_COMMIT_COUNT == 0:
            consumer.commit(asynchronous=False)
            print("обработано ", MIN_COMMIT_COUNT, "сообщений")
finally:
    # Закрытие консьюмера
    consumer.close()