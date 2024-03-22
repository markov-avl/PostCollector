# Post Collector

Приложение для сбора постов с разных telegram-каналов в один чат с telegram-ботом.

## Требования

- Ненужный telegram-аккаунт (для возможности подписок на разные telegram-каналы).
- Python >= 3.12.

## Как работает

### Главные сущности

1. **Telegram-бот**, принимающий роль **пользовательского интерфейса**, а также **рассылателя постов**.
2. **Telegram-аккаунт**, который **принимает заявки на подписку** и **слушает новости** из telegram-каналов.

### Бизнес-логика

- Когда telegram-бот получает запрос на подписку, telegram-аккаунт подписывается на предложенный канал.
- Когда telegram-аккаунт получает какую-либо активность из telegram-каналов, он пересылает ее telegram-боту.
- Когда telegram-бот получает переотправленные сообщения от выделенного telegram-аккаунта, он пересылает контент всем "подписчикам".
- Вся дополнительная информация (о подписчиках, каналах и т.д.) хранится в СУБД sqlite.

## Создание Telegram WebApp

Создание Telegram WebApp описано [здесь](https://core.telegram.org/api/obtaining_api_id). Существуют также сторонние гайды.

Наиболее важными ключами (их обязательно нужно сохранить) при создании Telegram WebApp являются:
- `api_id`;
- `api_hash`.

## Создание Telegram Bot

Создание Telegram Bot описано [здесь](https://core.telegram.org/bots#how-do-i-create-a-bot). Существуют также сторонние гайды.

Наиболее важными ключем (его обязательно нужно сохранить) при создании Telegram Bot является: `token`.

## Файлы настройки

### .env

Это файл, хранящий переменные окружения для настройки приложения.

Переменные окружения, которые считываются приложением:
```shell
export DATABASE_NAME=<название базы данных, к которой будет производиться подключение>
export DATABASE_LOGGING=<параметр, влияющий на наличие дополнительных логов от драйвера базы данных>

export TELEGRAM_USER_NAME=<любое удобное имя для telegram-аккаунта>
export TELEGRAM_USER_PHONE=<номер телефона telegram-аккаунта>
export TELEGRAM_USER_API_ID=<api_id, выданный при создании Telegram WebApp>
export TELEGRAM_USER_API_HASH=<api_hash, выданный при создании Telegram WebApp>

export TELEGRAM_BOT_TOKEN=<token, выданный при создании Telegram Bot>
export TELEGRAM_BOT_ALBUM_FORWARD_PAUSE=<параметр, влияющий на задержку переотправки альбомов (в секундах)>
```

Пример настроек:
```shell
export DATABASE_NAME=production
export DATABASE_LOGGING=false

export TELEGRAM_USER_NAME=main
export TELEGRAM_USER_PHONE=+79998887766
export TELEGRAM_USER_API_ID=12345678
export TELEGRAM_USER_API_HASH=0123456789abcdef0123456789abcdef

export TELEGRAM_BOT_TOKEN=0123456789:ABC-abcdefghijklmnopqrstu-vwxyz0123
export TELEGRAM_BOT_ALBUM_FORWARD_PAUSE=10
```

### properties.yaml

Можно также указать настройки в `properties.yaml`, что является плохим тоном.

Пример заполненных настроек:
```yaml
database:
  name: 'production'
  logging: false

telegram:
  user:
    name: 'main'
    phone: '+79998887766'
    api_id: 12345678
    api_hash: '0123456789abcdef0123456789abcdef'
  bot:
    token: '0123456789:ABC-abcdefghijklmnopqrstu-vwxyz0123'
    album_forward_pause: 10
```

В нормальных условиях этот файл не требует изменений, если настройки всё же будут считываться из `.env`.

## Первая настройка окружения (для linux)

```shell
cd <путь к директории приложения>
python3.12 -m venv .venv
source .venv/bin/activate
pip3.12 install -r requirements.txt
pip3.12 install -i https://test.pypi.org/simple/ puripy
```

## Запуск приложения

Если используется `.env` файл:
```shell
source .env && python3.12 main.py
```

Если не используется `.env` файл:
```shell
python3.12 main.py
```

## Первый запуск приложения с новым telegram-аккаунтом

При первом запуске приложения с новым telegram-аккаунтом в терминал потребуется ввести одноразовый код, высланный в сообщения этого аккаунта (от Telegram Notifier).

## Требования для коректной работы приложения

- Все ключи введены верно (без лишних пробелов, без упущенных символов).
- Telegram-аккаунт должен начать диалог с telegram-ботом.
- Нельзя мьютить или архивировать telegram-бота со стороны telegram-аккаунта.
- Нельзя мьютить, архивировать или отписываться от telegram-каналов, которые были добавлены под воздействием работы приложения.
- Нельзя чистить БД (файл `{DATABASE_NAME}.db`, создастся при первом запуске).
- Нельзя запускать приложение дважды при одинаковых значениях ключей.
