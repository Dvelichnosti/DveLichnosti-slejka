# DveLichnosti-slejka
1. Получить api_id и api_hash для Telegram API
Перейди на сайт https://my.telegram.org и войди через свой номер телефона.

Перейди в раздел API Development Tools.

Создай новое приложение, введи название, короткое описание и сайт (можно любой, например, https://example.com).

После создания увидишь свои api_id и api_hash.

Запомни их или скопируй — они понадобятся для скрипта.



2. pip install telethon rich



3. Подставить свои api_id и api_hash в скрипт
В начале скрипта замени:

python
Копировать
Редактировать
api_id = 1234567          # твой api_id
api_hash = "your_api_hash_here"  # твой api_hash

4. Авторизация TelegramClient
При первом запуске Telethon попросит ввести номер телефона, на который зарегистрирован твой Telegram.

Затем придёт SMS с кодом — введи его в терминал.

Клиент сохранит сессию в файле session.session — дальше вход будет автоматическим.

5. Мониторинг
После авторизации в консоли начнёт выводиться логотип, потом статус пользователя.

Будет показано, когда пользователь в сети, как долго он онлайн или оффлайн.

Статус будет обновляться каждые 3 секунды.

Логи статусов пишутся в файл user_status.log рядом с скриптом.


6. Остановка
Чтобы остановить программу — нажми Ctrl+C.



