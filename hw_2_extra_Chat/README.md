# ДЗ
## Доп. Задание - WebSocket (+1 доп балл)

Реализовать чат для пользователей в отдельных комнатах (в примере из лекции чат
был один на всех).

Пользователи подключаются к чату по WebSocket ручке `/chat/{chat_name}`.
Пользователи, которые ввели один и тот же `chat_name` буду подключены к одному
чату (то есть будут получать сообщения друг от друга). Пользователи, не
подключенные к диалогу, не будут получать сообщения.

Сообщение - текст в теле сообщения от клиента. Сервер должен broadcast'ить
сообщения на других пользователей в своем чате. Каждому клиенту сервер
присваивает случайное имя и дополняет каждое сообщение именем пользователя в
начале в следующем виде: `{username} :: {message}`.

### Запуск
Чтобы запустить сервер, достаточно из данной директории запустить команду `uvicorn server:app --reload` \
Для проверки работоспособности сервера можно запустить в разных терминалах скрипт client.py `python client.py`,
указать один чат и начать переписку (на одно входящее сообщение выводится одно сообщение из вне). 