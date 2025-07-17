import json
from confluent_kafka import Producer, SerializingProducer, serialization

str_serializer = serialization.StringSerializer("utf_8")

# Конфигурация продюсера – адрес сервера
conf = {
    "bootstrap.servers": "localhost:9092, localhost:9093",
    "key.serializer": str_serializer,
    "value.serializer": str_serializer,
    "acks": "all",  # Для синхронной репликации, количество реплик, которые должны подтвердить синхронизацию
    "retries": 3,  # Количество попыток при сбоях
}
# Создание продюсера
producer = SerializingProducer(conf)

# Тема Kafka
topic = "topic-tst-1"

for i in range(10):
  # Сообщение для отправки
  #key_str = "643"
  #message_value = {"code": 643, "acode": "RU", "name": "Российская Федерация"}
  #key_str = "688"
  #message_value = {"code": 688, "acode": "RS", "name": "Республика Сербия"}
  key_str = "716"
  message_value = {"code": 716, "acode": "ZW", "name": "Республика Зимбабве"}
  #key_str = "0"
  #message_value = {"code": 0, "acode": "XX", "name": "Test"}

  message_value_str = json.dumps(message_value, ensure_ascii=False) # JSON как текст

  # Отправка сообщения
  producer.produce(
      topic=topic,
      key=key_str,
      value=message_value_str
  )
  print(message_value_str)

# Ожидание завершения отправки всех сообщений
producer.flush()

print("done!")