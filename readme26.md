1. Поднятие инстанса PostgreSQL (версии 12) c 3 volume:  
[docker-compose манифест](https://github.com/Serg2123/devops-netology/blob/main/docker-compose.yml)  

2.
Создание пользователя test-admin-user:  
```
CREATE ROLE " test-admin-user" WITH
  LOGIN
  SUPERUSER
  INHERIT
  CREATEDB
  CREATEROLE
  NOREPLICATION
  ENCRYPTED PASSWORD 'md5...';
```
Создание базы данных:  
```
CREATE DATABASE test_db
    WITH 
    OWNER = " test-admin-user"
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
```
Создание таблиц orders и clients сразу же с овнером test-admin-user:  
```
CREATE TABLE public.orders
(
    id serial NOT NULL,
    "наименование" text,
    "цена" integer,
    PRIMARY KEY (id)
)
TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.orders
    OWNER to " test-admin-user";
```
```
CREATE TABLE public.clients
(
    id serial NOT NULL,
    "фамилия" text,
    "страна проживания" text,
    "заказ" serial,
    PRIMARY KEY (id),
    CONSTRAINT "Заказ_Foreign_key" FOREIGN KEY ("заказ")
        REFERENCES public.orders (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.clients
    OWNER to " test-admin-user";
```
Создание индекса для для страны проживания:  
```
CREATE INDEX "страна_idx"
    ON public.clients USING btree
    ("страна проживания" ASC NULLS FIRST)
    TABLESPACE pg_default;
```
На самом деле для test-admin-user все привилегии уже есть, т.к. он был указан овнером при создании test_db, но еще раз:  
```
GRANT ALL ON SEQUENCE public.clients_id_seq TO " test-admin-user";
GRANT ALL ON SEQUENCE public."clients_заказ_seq" TO " test-admin-user";
GRANT ALL ON SEQUENCE public.orders_id_seq TO " test-admin-user";
GRANT ALL ON TABLE public.clients TO " test-admin-user";
GRANT ALL ON TABLE public.orders TO " test-admin-user";
```
Создадим простого пользователя test-simple-user:  
```
CREATE ROLE "test-simple-user" WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  ENCRYPTED PASSWORD 'md5...';
```
Предоставим пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE для данных таблиц БД test_db:  
```
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.clients TO " test-admin-user";
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.orders TO " test-admin-user";
```
Подключимся к серверу в консоли через psql и вызовем список БД:  
```
docker-compose exec postgres bash -c "psql -U vagrant template1"
\l
```
```
template1-# \l
                                     List of databases
    Name     |      Owner       | Encoding |  Collate   |   Ctype    |  Access privileges
-------------+------------------+----------+------------+------------+---------------------
 netology-db | vagrant          | UTF8     | en_US.utf8 | en_US.utf8 |
 postgres    | vagrant          | UTF8     | en_US.utf8 | en_US.utf8 |
 template0   | vagrant          | UTF8     | en_US.utf8 | en_US.utf8 | =c/vagrant         +
             |                  |          |            |            | vagrant=CTc/vagrant
 template1   | vagrant          | UTF8     | en_US.utf8 | en_US.utf8 | =c/vagrant         +
             |                  |          |            |            | vagrant=CTc/vagrant
 test_db     |  test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 |
(5 rows)
```
Либо "SELECT datname FROM pg_database" все в том же pqAdmin.  
  
Описание таблиц (describe):  
```
test_db=# \d+ orders
                                                   Table "public.orders"
    Column    |  Type   | Collation | Nullable |              Default               | Storage  | Stats target | Description
--------------+---------+-----------+----------+------------------------------------+----------+--------------+-------------
 id           | integer |           | not null | nextval('orders_id_seq'::regclass) | plain    |              |
 наименование | text    |           |          |                                    | extended |              |
 цена         | integer |           |          |                                    | plain    |              |
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "Заказ_Foreign_key" FOREIGN KEY ("заказ") REFERENCES orders(id)
Access method: heap

test_db=# \d+ clients
                                                        Table "public.clients"
      Column       |  Type   | Collation | Nullable |                 Default                  | Storage  | Stats target | Description
-------------------+---------+-----------+----------+------------------------------------------+----------+--------------+-------------
 id                | integer |           | not null | nextval('clients_id_seq'::regclass)      | plain    |
 |
 фамилия           | text    |           |          |                                          | extended |
 |
 страна проживания | text    |           |          |                                          | extended |
 |
 заказ             | integer |           |          |                                          | plain    |
 |
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
    "страна_idx" btree ("страна проживания" NULLS FIRST)
Foreign-key constraints:
    "Заказ_Foreign_key" FOREIGN KEY ("заказ") REFERENCES orders(id)
```
SQL-запрос для выдачи списка пользователей с правами над таблицами test_db:  
```
SELECT table_name, grantee, privilege_type 
FROM information_schema.role_table_grants 
WHERE table_catalog='test_db' and (table_name = 'clients' or table_name = 'orders')
```
Список пользователей с правами над таблицами test_db:  
```
test_db-# \z clients
                                            Access privileges
 Schema |  Name   | Type  |               Access privileges               | Column privileges | Policies
--------+---------+-------+-----------------------------------------------+-------------------+----------
 public | clients | table | " test-admin-user"=arwdDxt/" test-admin-user"+|                   |
        |         |       | "test-simple-user"=arwd/" test-admin-user"    |                   |
(1 row)

test_db-# \z orders
                                           Access privileges
 Schema |  Name  | Type  |               Access privileges               | Column privileges | Policies
--------+--------+-------+-----------------------------------------------+-------------------+----------
 public | orders | table | " test-admin-user"=arwdDxt/" test-admin-user"+|                   |
        |        |       | "test-simple-user"=arwd/" test-admin-user"    |                   |
(1 row)
```

3.  
Заполняем orders:  
```
INSERT INTO orders (наименование, цена) VALUES
    ('Шоколад', '10'),
    ('Принтер', '3000'),
    ('Книга', '500'),
    ('Монитор', '7000'),
    ('Гитара', '4000');
```
Заполняем clients:
```
INSERT INTO clients (фамилия, "страна проживания") VALUES
    ('Иванов Иван Иванович', 'USA'),
    ('Петров Петр Петрович', 'Canada'),
    ('Иоганн Себастьян Бах', 'Japan'),
    ('Ронни Джеймс Дио', 'Russia'),
    ('Ritchie Blackmore', 'Russia');
```
Вычисление количества записей для каждой таблицы:  
```
SELECT COUNT (*) FROM orders
SELECT COUNT (*) FROM clients
```
везде по 5 записей.  
  
4.  
```
UPDATE clients SET заказ = orders.id
FROM orders
WHERE clients.фамилия = 'Иванов Иван Иванович' and orders.наименование = 'Книга'
```
```
UPDATE clients SET заказ = orders.id
FROM orders
WHERE clients.фамилия = 'Петров Петр Петрович' and orders.наименование = 'Монитор'
```
```
UPDATE clients SET заказ = orders.id
FROM orders
WHERE clients.фамилия = 'Иоганн Себастьян Бах' and orders.наименование = 'Гитара'
```
Вывод пользователей которые сделали покупки:  
```
SELECT clients.фамилия as "Пользователи, совершившие заказы", clients."страна проживания" as "Страна", orders.наименование as "Что купили"
FROM clients JOIN orders ON clients.заказ = orders.id 
WHERE clients.заказ NOTNULL
```
"Пользователи, совершившие заказы"	"Страна"	"Что купили"  
"Иванов Иван Иванович"	"USA"	"Книга"  
"Иоганн Себастьян Бах"	"Japan"	"Гитара"  
"Петров Петр Петрович"	"Canada"	"Монитор"  
  
5. Использование EXPLAIN:  
```
EXPLAIN (ANALYZE, VERBOSE, FORMAT YAML)
SELECT clients.фамилия as "Пользователи, совершившие заказы", clients."страна проживания" as "Страна", orders.наименование as "Что купили"
FROM clients JOIN orders ON clients.заказ = orders.id 
WHERE clients.заказ NOTNULL
```
```
- Plan: 
    Node Type: "Hash Join"
    Parallel Aware: false
    Join Type: "Inner"
    Startup Cost: 37.00
    Total Cost: 57.23
    Plan Rows: 806
    Plan Width: 96
    Actual Startup Time: 0.031
    Actual Total Time: 0.034
    Actual Rows: 3
    Actual Loops: 1
    Output: 
      - "clients.\"фамилия\""
      - "clients.\"страна проживания\""
      - "orders.\"наименование\""
    Inner Unique: true
    Hash Cond: "(clients.\"заказ\" = orders.id)"
    Plans: 
      - Node Type: "Seq Scan"
        Parent Relationship: "Outer"
        Parallel Aware: false
        Relation Name: "clients"
        Schema: "public"
        Alias: "clients"
        Startup Cost: 0.00
        Total Cost: 18.10
        Plan Rows: 806
        Plan Width: 68
        Actual Startup Time: 0.013
        Actual Total Time: 0.014
        Actual Rows: 3
        Actual Loops: 1
        Output: 
          - "clients.id"
          - "clients.\"фамилия\""
          - "clients.\"страна проживания\""
          - "clients.\"заказ\""
        Filter: "(clients.\"заказ\" IS NOT NULL)"
        Rows Removed by Filter: 2
      - Node Type: "Hash"
        Parent Relationship: "Inner"
        Parallel Aware: false
        Startup Cost: 22.00
        Total Cost: 22.00
        Plan Rows: 1200
        Plan Width: 36
        Actual Startup Time: 0.010
        Actual Total Time: 0.010
        Actual Rows: 5
        Actual Loops: 1
        Output: 
          - "orders.\"наименование\""
          - "orders.id"
        Hash Buckets: 2048
        Original Hash Buckets: 2048
        Hash Batches: 1
        Original Hash Batches: 1
        Peak Memory Usage: 17
        Plans: 
          - Node Type: "Seq Scan"
            Parent Relationship: "Outer"
            Parallel Aware: false
            Relation Name: "orders"
            Schema: "public"
            Alias: "orders"
            Startup Cost: 0.00
            Total Cost: 22.00
            Plan Rows: 1200
            Plan Width: 36
            Actual Startup Time: 0.004
            Actual Total Time: 0.006
            Actual Rows: 5
            Actual Loops: 1
            Output: 
              - "orders.\"наименование\""
              - "orders.id"
  Planning Time: 0.116
  Triggers: 
  Execution Time: 0.054
```
EXPLAIN позволяет нам получить отчет о выполнении запроса (план выполнения запроса), 
который дает суммарную информацию о выполнении запроса с подробным отчетом о времени, 
потраченном на каждом шаге, и затратах на его выполнение. Необходимо для отладки, 
оптимизации времени выполнения, оптимизации хранения данных и ускорения доступа к ним.  
  
6.  
Cоздаем бекап и складываем его сразу же на созданый ранее volume:
```
docker-compose exec postgres bash -c "/usr/bin/pg_dump -U vagrant test_db > /var/lib/postgresql/backup/test_db_06.01.bak"
```
Т.к. pg_dump бекапит только саму БД, то первым делом (что бы не нарываться на ошибки) в новом контейнере создаем заново:  
2-х пользователей test-admin-user, test-simple-user, а так же саму пустую БД: test_db сразу же с овнером test-admin-user (все команды создания объектов приведены в п.2).  
После того как создалась пустая БД test_db в нее можно разворачивать бекап комадой:  
```
docker-compose exec postgres bash -c "/usr/bin/psql -U vagrant test_db < /var/lib/postgresql/backup/test_db_06.01.bak"
```

