import asyncio
import websockets


async def chat_client(chat_name):
    async with websockets.connect(f'ws://localhost:8000/chat/{chat_name}') as websocket:
        print(f"Connected to chat room: {chat_name}")

        # Основной цикл для отправки сообщений
        while True:
            message = input("Enter your message: ")
            await websocket.send(message)  # Отправка сообщения на сервер
            response = await websocket.recv()  # Получение ответа от сервера
            print(response)  # Вывод сообщения от других пользователей

if __name__ == "__main__":
    chat_name = input("Enter chat room name: ")
    asyncio.run(chat_client(chat_name))