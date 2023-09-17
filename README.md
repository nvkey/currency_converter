# Currency converter
Конвертер валют
## Задание:
Написать сервис "Конвертер валют" который работает по REST-API.
Пример запроса:  
```GET /api/rates?from=USD&to=RUB&value=1```  
Ответ:  
```json
{
"result": 62.16
}
```
Любой фреймворк в пределах python.  
Данные о текущих курсах валют необходимо получать с внешнего сервиса.  
Контейнерезация, документация, и прочее — приветствуется.  

## Описание проекта
Сервис работает на базе открытого ресурса Open Access Endpoint  
https://www.exchangerate-api.com/  
Доступны следующие функции:  
- Конвертация через кэшируемые данные (1 час)
- Прямой запрос к открытому ресурсу open_erapi

## Запуск проекта(Docker):
Клонировать репозиторий и перейти в него в командной строке:
``` bash
git clone git@github.com:nvkey/currency_converter.git
cd currency_converter
```

Создайте файл .env в папке `/infra/` со следующими ключами:
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Запустить docker-compose:
``` bash
cd infra
docker compose up -d --build
```

Выполнить миграции и сформировать статику:
``` bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --no-input 
```
Проект: http://localhost/api/v1  
Swagger API: http://localhost/swagger/  
Redoc: http://localhost/redoc