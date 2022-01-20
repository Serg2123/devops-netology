ДЗ во многом повторяет предпредыдущее про общий SQL на базе Postgers 12.  

1. Поднятие инстанса PostgreSQL (версии 13) c 3 volume:  
[docker-compose манифест](https://github.com/Serg2123/devops-netology/blob/main/docker-compose-psql.yml)  
Подключимся в консоль контейнера сразу же в искомую БД которую опредлили в docker-compose:  
```docker-compose exec postgres bash```
```psql -U vagrant test_database```
Вывод списка БД - "\l"  
Подключения к БД или смена БД - "\c template1"  
Вывод списка таблиц (расширенный) - "\dtS+"  
Вывод описания содержимого таблиц - "\dS+ имя_таблицы"  
Выход из psql - "\q"  
  
2.  
Восстанавливаем скаченный бекап и выполняем ANALYZE:  
```
/usr/bin/psql -U vagrant test_database < /var/lib/postgresql/backup/test_dump.sql
ANALYZE VERBOSE orders;
```
Ищем столбец таблицы orders с наибольшим средним значением размера элементов в байтах:  
```
SELECT schemaname, tablename, attname, avg_width  
      FROM pg_stats  
WHERE tablename = 'orders' and  
      avg_width = (SELECT max(avg_width) FROM pg_stats WHERE tablename = 'orders');
```
  
3. Шардирование orders на на orders_1 (price>499) и orders_2 (price<=499):  
```
START TRANSACTION;
--создадим 2 новых таблички с наследованием от orders
CREATE TABLE public.orders_1 (
    CHECK (price>499)
) INHERITS (orders);
CREATE TABLE public.orders_2 (
    CHECK (price > 0 and price <=499 )
) INHERITS (orders);

-- создадим 2 тригера для вставки данных в новые таблички при выполнении старой операции вставки в старую таблицу
CREATE RULE insert_new_order_1 AS ON INSERT TO public.orders WHERE (price>499)
DO INSTEAD INSERT INTO public.orders_1 VALUES (NEW.*);
CREATE RULE insert_new_order_2 AS ON INSERT TO public.orders WHERE (price > 0 and price <=499)
DO INSTEAD INSERT INTO public.orders_2 VALUES (NEW.*);

--переложим данные из старой таблички в 2 новые таблички по нашему условию шардирования
INSERT INTO public.orders_1 SELECT * FROM ONLY public.orders WHERE price>499;
INSERT INTO public.orders_2 SELECT * FROM ONLY public.orders WHERE (price > 0 and price <=499);

--почистим за собой старую табличку
DELETE FROM ONLY public.orders;
COMMIT;

--проверим все ли работает как и ранее:
SELECT * FROM public.orders
--убедимся что старая таблица пуста:
SELECT * FROM ONLY public.orders
```

4.  
Cоздаем бекап и складываем его на внешний volume:  
```
docker-compose exec postgres bash -c "/usr/bin/pg_dump -U vagrant test_database > /var/lib/postgresql/backup/test_database.bak"
```
Добавим в конец бекапа (после строчки создания первичного ключа) еще строчку проверки на уникатьность столбца title:  
```
ALTER TABLE ONLY public.orders ADD CONSTRAINT title_unique UNIQUE (title);
```
