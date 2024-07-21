# Тестовое задание для компании Единая Информационная Система ЖКХ

## [Схема базы данных (ссылка)](https://dbdiagram.io/d/hcs-test-task-669caa478b4bb5230ee6f85e)

![HCS schema](https://i.imgur.com/2B0FsIz.png)

## Список доступных API

### Посмотреть информацию о зданиях (все здания, их квартиры и счётчики)

```
METHOD: get
URL: http://127.0.0.1:8000/building/
```

### Добавить здание

```
METHOD: post
BODY:
- number: int
- address: varchar
URL: http://127.0.0.1:8000/building/
```

### Добавить квартиру в здание

```
METHOD: post
BODY:
- number: int
- building_id: int
- size_m2: int
URL: http://127.0.0.1:8000/apartment/
```

### Добавить счётчик в квартиру

```
METHOD: post
BODY:
- apartment_id: int
URL: http://127.0.0.1:8000/water_meter/
```
