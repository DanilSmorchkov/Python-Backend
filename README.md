# Python Backend

## 1. Реализовать "Математическое API" из примера напрямую через ASGI-compatible функцию.
1. Сначала необходимо зайти в папку с заданием ``cd hw_1_asgi``. \
2. Для запуска сервера можно воспользоваться Makefile:
- ``make run`` 

    либо сделать все руками:
- ```shell
  python3 -m venv venv
  source ./venv/bin/activate
  pip install -r requirements.txt
  uvicorn asgi:app
  ```

3. Чтобы запустить тесты в новом терминале нужно снова перейти в папку с заданием и запустить команду ``make test``.