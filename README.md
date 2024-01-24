# «Меню ресторана»

Инструкция по запуску проекта.

## Шаг 1

Форкнуть и/или клонировать проект в нужную папку командой 
#### `clone <repo>`.

## Шаг 2

При необходимости создать и активировать виртуальное окружение проекта
####	`python3 -m venv env`
####	`source env/bin/activate`

## Шаг 3

Добавить в проект файл окружения `.env`, где задать ключам настройки доступа к БД.
####    `Переименовать и отредактировать  файл .env-example`

## Шаг 4

#### Подключить БД и PgAdmin командой

####	`docker compose up --build -d`

	В случае появления ошибки прав доступа при запуске контейнера PgAdmin ((HTTP code 500) server error 
	нужно:
	a) в Docker desktop расшарить /fastapi1_menu - рабочую директорию проекта (Настройки: Resources -> File sharing -> +)
	б) повторить п.4

## Шаг 5

Проверить, не занят ли порт `8000` приложения, например командой
####	`netstat -a -p TCP -n | grep 8000`

## Шаг 6

Запустить проект. Будет создана БД при первом запуске.
#