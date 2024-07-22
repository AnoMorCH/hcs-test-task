# Тестовое задание для компании Единая Информационная Система ЖКХ

## Запуск приложения

```bash
docker compose build
docker compose up
```

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
