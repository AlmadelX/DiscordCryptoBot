# DiscordCryptoBot
## Информация
Бот использует Discord-аккаунт, который подписан на нужные серверы.
Для удобства, я создал такой аккаунт, данные для входа в аккаунт и его токен перешлю в ЛС.

## Инструкция по запуску бота
1. Создайте бота с помощью @BotFather в Telegram, настройте желаемую метаинформацию
2. Задайте настройки в файле ```settings.ini``` (по примеру ```settings_example.ini```):

- TelegramID админов (свой ID можно узнать написав боту "Get my ID")
- Токен бота, полученный на шаге 1
- Токен Discord-аккаунта 

3. Откройте текущую папку в командной строке
4. Настройте среду и зависимости:
   
   Unix:
   ```commandline
   python -m venv .venv
   source .venv/Scripts/activate
   pip install -r requirements.txt
   ```
   Windows:
   ```commandline
   python -m venv .venv
   .venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

5. Запустите скрипт:
   ```commandline
   python main.py
   ```

## Инструкция по добавлению нового сервера
1. Вступите в сервер с используемого Discord-аккаунта
2. В боте выберите: Admin Panel -> Add Server
3. Введите название сервера
4. Введите ссылку на канал, который будет отслеживаться:

![tutorial](tutorial.png "Tutorial")
