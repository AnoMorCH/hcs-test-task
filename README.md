# Тестовое задание для компании Единая Информационная Система ЖКХ

## Запуск приложения

```bash
docker compose build
docker compose up
```

## Пояснение по реализации в соответствии с ТЗ

### Пункт 1

* Реализация моделей расположена в `app/hcs/models.py`

* Условия, что в доме содержится множество квартир, в квартире &ndash; несколько счётчиков, реализованы при помощи отношения 1:М

* Площадь квартиры хранится как поле `size_m2` внутри модели `Apartment` в `app/hcs/models.py`

* Счётчик хранит показания за несколько месяцев благодаря модели `WaterMeter` (есть ограничение unique для предотвращения аномалий данных)

* Тариф реализован через модель `Tariff` &ndash; может хранить либо тариф за воду, либо за содержание придомового имущества

### Пункт 2

Все API расположены в `app/hcs/views.py`.

* `BuildingView`: get-запрос возвращает информацию о доме, в том числе обо всех квартирах в нём и счётчиках в помещениях; post-запрос &ndash; записывает информацию о доме

* `ApartmentView`: post-запрос записывает информацию о квартире в доме

* `WaterMeterView`: post-запрос записывает информацию о счётчике в квартире

Вся дополнительная логика вынесена в папку `app/hcs/entity`, чтобы предотвратить захламление `app/hcs/views.py` большим количеством кода.

### Пункт 3

* API реализовано через `CountCommunalServicePriceView` внутри файла `app/hcs/views.py`

* Водоснабжение учитывается в модели `WaterMeterLog`

* Содержание общедомового имущества находится в модели `BuildingServiceLog`

* Работоспособность с граничными случаями протестирована внутри `app/hcs/tests.py`

### Пункт 4

* Процесс расчёта хранится в моделях `WaterMeterLog` и `BuildingServiceLog`

* Распределение нагрузки через Celery реализовано при помощи Redis; настройки находятся в файле `app/house_accounting/celery.py`; задачи &ndash; `app/hcs/tasks.py`, для интеграции с докером реализовано ручное подключение к БД через `app/hcs/management/commands/wait_for_db.py`

## [Схема базы данных (ссылка)](https://dbdiagram.io/d/hcs-test-task-669caa478b4bb5230ee6f85e)

![HCS schema](https://i.imgur.com/w62dCWm.png)

## Список доступных API

### Посмотреть информацию о зданиях (все здания, их квартиры и счётчики)

```
METHOD: get
URL: http://0.0.0.0:8000/building/
RESPONSE: json
```

### Добавить здание

```
METHOD: post
BODY:
- number: int
- address: varchar
URL: http://0.0.0.0:8000/building/
RESPONSE: json
```

### Добавить квартиру в здание

```
METHOD: post
BODY:
- number: int
- building_id: int
- size_m2: int
URL: http://0.0.0.0:8000/apartment/
RESPONSE: json
```

### Добавить счётчик в квартиру

```
METHOD: post
BODY:
- apartment_id: int
URL: http://0.0.0.0:8000/water_meter/
RESPONSE: json
```

### Посчитать квитанции под весь дом

Прежде чем запустить выполнение функции, необходимо добавить значение тарифов на жильё и на водоснабжение через админ-панель в таблицу `Tariff`.

```
METHOD: post
BODY:
- building_id: int
- year: int
- month: int
URL: http://0.0.0.0:8000/communal_service_price_count/
```

## Особенности реализации приложения

### Если нет показаний ранее, но есть за текущий месяц

То приложение считает разницу между текущими показателями и нулём.

### Каким образом функция сохраняет процесс расчёта показаний 

При помощи логирования (отдельно записываются данные как для водоснабжения, так и для содержания общего имущества). 

### Как функция проводит процесс записи квартплаты на весь дом?

В логах о водоснабжении хранится только количество потреблённой воды, однако не её цена (поле этого параметра в БД `nullable`).

Когда запускается процесс подсчёта квартплаты, происходит следующее:

* Для водоснабжения

Расход умножается на самый актуальный тариф. Если человек не отправил показания счётчиков за месяц, то для него за текущий месяц не считается чек по этому параметру. 

* Для содержания общедомового имущества

Считается по формуле из ТЗ, когда происходит запуск функции по подсчёту квартплаты.

### Что будет, если человек ввёл показания о водоснабжении с опозданием (когда функция уже закончила выполнение)?

Это учтено программой. В таком случае старые показания не будут трогаться, а новые &ndash; где нет записи о цене чека на воду за указанный месяц &ndash; будут обновляться по самому актуальному тарифу.

### Способы улучшить приложение

* Добавить больше тестов (на данном этапе, протестирован только ключевой функционал, но опущены юнит тесты на отправку и получение HTTP-запросов, корректный формат выходных данных и т.д.)
