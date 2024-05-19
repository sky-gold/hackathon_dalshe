# Хакатон «Код со смыслом»

### Кейс Благотворительный фонд «Дальше»

### Команда «НН»

- Ефимов Никита Андреевич
- Водолеев Никита Алексеевич

# Инструкция к сборке и запуску

### Требования

- Docker
- Docker Compose

## Установка, сборка и запуск

Для запуска проекта выполните следующие шаги:

1. Клонируйте репозиторий:

```bash
git clone https://github.com/sky-gold/hackathon_dalshe.git
cd hackathon_dalshe
```

2. Задайте переменные окружения в файле `.env`:
   Для работы нужно задать переменные для работы базы данных **DB_HOST**, **DB_NAME**, **DB_USER**, **DB_PASSWORD** и для работы бота **BOT_TOKEN**  
   [Как получить токен телеграм бота](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
   
   Пример .env:

```bash
DB_HOST=localhost
DB_NAME=mydatabase
DB_USER=postgres
DB_PASSWORD=example
BOT_TOKEN=<your_token>
```

3. Соберите и запустите проект с помощью Docker Compose:

```bash
docker-compose build
docker-compose up -d
```

4. После запуска проекта вы увидите вывод логов контейнеров в терминале. Если все прошло успешно, вы должны увидеть сообщения о запуске сервисов.

5. Для остановки проекта выполните команду:

```bash
docker-compose down
```

Эта команда остановит и удалит все контейнеры и сети, созданные Docker Compose.
