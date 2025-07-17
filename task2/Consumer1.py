# SingleMessageConsumer  
# считывает по одному сообщению, обрабатывает и коммитит оффсет автоматически  
from confluent_kafka import Consumer, serialization, DeserializingConsumer  
  
str_deserializer = serialization.StringDeserializer("utf_8")  
  
# Настройка консьюмера – адрес сервера  
conf = {  
    "bootstrap.servers": "localhost:9092",  
    "group.id": "group-tst-single",        # Уникальный идентификатор группы  
    "enable.auto.commit": True,            # Автоматический коммит смещений  
    "auto.offset.reset": "earliest",       # Начало чтения с самого начала  
    "key.deserializer": str_deserializer,  # не уверен что это единственный способ задействовать десериализатор  
    "value.deserializer": str_deserializer  
}  
# Создание консьюмера  
#consumer = Consumer(conf)  
consumer = DeserializingConsumer(conf)  
  
# Подписка на топик  
consumer.subscribe(["topic-tst-1"])  
  
# Чтение сообщений  
running = True  
try:  
    while running:  
        # Получение сообщений  
        msg = consumer.poll(1.0)  # poll timeout = 1s  
  
        if msg is None:  
            #не понятно почему если расскомментировать эти строки то перестает считывать сообщения, при этом если дебажить то считывает  
            #print('none')            #running = False            continue  
        if msg.error():  
            print(f"Ошибка: {msg.error()}")  
            running = False  
            continue  
        #key = msg.key().decode("utf-8")  
        #value = msg.value().decode("utf-8")        key = msg.key()  
        value = msg.value()  
        print(f"Получено сообщение: {key=}, {value=}, offset={msg.offset()}")  
finally:  
    # Закрытие консьюмера  
    consumer.close()