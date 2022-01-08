1. Поднятие инстанса c MySQL (версии 8) c 4 volume:  
[docker-compose манифест](https://github.com/Serg2123/devops-netology/blob/main/docker-compose-mysql.yml)  
  
Подключаемся в консоль и восстанавливается из бекапа в базу данных netolody-db (хотя в бекапе указана test_db, но через компосер мы уже создали для тестовых целей netology-db, еще и как оказалось с некомендуемым символом "-"):  
```
mysql -u vagrant -p netology-db < /var/lib/mysql-backup/test_dump.sql
```
Получаем статус c версией сервера:  
```
mysql> \s
--------------
mysql  Ver 8.0.27 for Linux on x86_64 (MySQL Community Server - GPL)

Connection id:          91
Current database:       netology-db
Current user:           vagrant@localhost
SSL:                    Not in use
Current pager:          stdout
Using outfile:          ''
Using delimiter:        ;
Server version:         8.0.27 MySQL Community Server - GPL
Protocol version:       10
Connection:             Localhost via UNIX socket
Server characterset:    utf8mb4
Db     characterset:    utf8mb4
Client characterset:    latin1
Conn.  characterset:    latin1
UNIX socket:            /var/lib/mysql/mysql.sock
Binary data as:         Hexadecimal
Uptime:                 32 min 58 sec

Threads: 2  Questions: 200  Slow queries: 0  Opens: 167  Flush tables: 3  Open tables: 85  Queries per second avg: 0.101
--------------
```
Еще раз подключаемся к нашей БД (для примера) и получаем список таблиц:  
```
mysql> use netology-db
Database changed
mysql> show tables;
+-----------------------+
| Tables_in_netology-db |
+-----------------------+
| orders                |
+-----------------------+
1 row in set (0.00 sec)
```
Количество записей с price > 300 (пришлось подоброться с ошибкой ERROR 1064 (42000)):  
```
mysql> set @@sql_mode='IGNORE_SPACE';
Query OK, 0 rows affected (0.00 sec)
mysql> SELECT COUNT (*) FROM orders WHERE price>300;
+-----------+
| COUNT (*) |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
```

2. Добавим в my.cnf строку с другим плагином аутентификации и перезапустим контейнер:  
```
[mysqld]
default_authentication_plugin = mysql_native_password
```
Проверим текущий метод аутентификации:  
```
mysql> show variables like 'default_authentication_plugin';
+-------------------------------+-----------------------+
| Variable_name                 | Value                 |
+-------------------------------+-----------------------+
| default_authentication_plugin | mysql_native_password |
+-------------------------------+-----------------------+
1 row in set (0.01 sec)
```
Создим пользователя test в БД netology-db c паролем test-pass и всеми требуемыми параметрами и атрибутами:  
```
mysql> CREATE USER 'test'@'localhost' IDENTIFIED WITH mysql_native_password BY 'test-pass'
    -> WITH MAX_QUERIES_PER_HOUR 100
    -> PASSWORD EXPIRE INTERVAL 180 DAY
    -> FAILED_LOGIN_ATTEMPTS 3
    -> ATTRIBUTE '{"Last_name": "Pretty", "First_name": "James"}';
Query OK, 0 rows affected (0.00 sec)
```
Выдадим права на SELECT (используем доп.кавычки, т.к. был использован знак "-" в названии БД):  
```
mysql> GRANT SELECT ON `netology-db`.* to 'test'@'localhost';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```
Получаем информацию о пользователе:
```
mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES WHERE user = 'test';
+------+-----------+------------------------------------------------+
| USER | HOST      | ATTRIBUTE                                      |
+------+-----------+------------------------------------------------+
| test | localhost | {"Last_name": "Pretty", "First_name": "James"} |
+------+-----------+------------------------------------------------+
1 row in set (0.00 sec)
```
  
3. Профилирование:  
```
mysql> set profiling=1;
Query OK, 0 rows affected, 1 warning (0.00 sec)
mysql> SELECT COUNT (*) FROM orders WHERE price > 300;
+-----------+
| COUNT (*) |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
mysql> show profiles;
+----------+------------+------------------------------------------------+
| Query_ID | Duration   | Query                                          |
+----------+------------+------------------------------------------------+
|        1 | 0.00043150 | SELECT COUNT (*) FROM orders WHERE price > 300 |
+----------+------------+------------------------------------------------+
1 row in set, 1 warning (0.00 sec)
```
```
mysql> show profile for query 1;
+--------------------------------+----------+
| Status                         | Duration |
+--------------------------------+----------+
| starting                       | 0.000112 |
| Executing hook on transaction  | 0.000007 |
| starting                       | 0.000010 |
| checking permissions           | 0.000009 |
| Opening tables                 | 0.000039 |
| init                           | 0.000009 |
| System lock                    | 0.000013 |
| optimizing                     | 0.000015 |
| statistics                     | 0.000073 |
| preparing                      | 0.000032 |
| executing                      | 0.000049 |
| end                            | 0.000007 |
| query end                      | 0.000006 |
| waiting for handler commit     | 0.000012 |
| closing tables                 | 0.000011 |
| freeing items                  | 0.000016 |
| cleaning up                    | 0.000015 |
+--------------------------------+----------+
17 rows in set, 1 warning (0.00 sec)
```
Перечень Engine c указанием дефолтного:  
```
mysql> SHOW ENGINES;
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| Engine             | Support | Comment                                                        | Transactions | XA   | Savepoints |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| FEDERATED          | NO      | Federated MySQL storage engine                                 | NULL         | NULL | NULL       |
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables      | NO           | NO   | NO         |
| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
| PERFORMANCE_SCHEMA | YES     | Performance Schema                                             | NO           | NO   | NO         |
| MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                          | NO           | NO   | NO         |
| BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears) | NO           | NO   | NO         |
| CSV                | YES     | CSV storage engine                                             | NO           | NO   | NO         |
| ARCHIVE            | YES     | Archive storage engine                                         | NO           | NO   | NO         |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
9 rows in set (0.00 sec)
```
Используемый Engine таблицы orders в тестовой БД:  
```
mysql> SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA='netology-db' and TABLE_NAME = 'orders';
+--------+
| ENGINE |
+--------+
| InnoDB |
+--------+
1 row in set (0.01 sec)
```
Изменяем Engine 2 раза для таблицы orders и смотрим время выполняния запросов (запросы 15 и 17):  
```
mysql> ALTER TABLE orders ENGINE = 'MyISAM';
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA='netology-db' and TABLE_NAME = 'orders';
+--------+
| ENGINE |
+--------+
| MyISAM |
+--------+
1 row in set (0.00 sec)

mysql> ALTER TABLE orders ENGINE = 'InnoDB';
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA='netology-db' and TABLE_NAME = 'orders';
+--------+
| ENGINE |
+--------+
| InnoDB |
+--------+
1 row in set (0.00 sec)

mysql> show profiles;
+----------+------------+---------------------------------------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                                                   |
+----------+------------+---------------------------------------------------------------------------------------------------------+
|        4 | 0.00035750 | SHOW ENGINES                                                                                            |
|        5 | 0.00030375 | SHOW ENGINES                                                                                            |
|        6 | 0.00030125 | SHOW ENGINES                                                                                            |
|        7 | 0.00126475 | SELECT ENGINE FROM information_schema.TABLES
WHERE TABLE_SCHEMA='netology-db'                           |
|        8 | 0.00029925 | SHOW ENGINES                                                                                            |
|        9 | 0.00145225 | SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA='netology-db'                           |
|       10 | 0.00426225 | SELECT * FROM information_schema.TABLES WHERE TABLE_SCHEMA='netology-db'                                |
|       11 | 0.00132650 | SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA='netology-db'                           |
|       12 | 0.00134300 | SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA='netology-db' and TABLE_NAME = 'order'  |
|       13 | 0.00122775 | SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA='netology-db' and TABLE_NAME = 'orders' |
|       14 | 0.00030600 | SHOW ENGINES                                                                                            |
|       15 | 0.03357175 | ALTER TABLE orders ENGINE = 'MyISAM'                                                                    |
|       16 | 0.00493875 | SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA='netology-db' and TABLE_NAME = 'orders' |
|       17 | 0.03825500 | ALTER TABLE orders ENGINE = 'InnoDB'                                                                    |
|       18 | 0.00637325 | SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA='netology-db' and TABLE_NAME = 'orders' |
+----------+------------+---------------------------------------------------------------------------------------------------------+
15 rows in set, 1 warning (0.00 sec)

mysql> show profile for query 15;
+--------------------------------+----------+
| Status                         | Duration |
+--------------------------------+----------+
| starting                       | 0.000092 |
| Executing hook on transaction  | 0.000006 |
| starting                       | 0.000020 |
| checking permissions           | 0.000007 |
| checking permissions           | 0.000008 |
| init                           | 0.000013 |
| Opening tables                 | 0.000358 |
| setup                          | 0.000112 |
| creating table                 | 0.000861 |
| waiting for handler commit     | 0.000010 |
| waiting for handler commit     | 0.003559 |
| After create                   | 0.001553 |
| System lock                    | 0.000011 |
| copy to tmp table              | 0.000114 |
| waiting for handler commit     | 0.000010 |
| waiting for handler commit     | 0.000012 |
| waiting for handler commit     | 0.000037 |
| rename result table            | 0.000063 |
| waiting for handler commit     | 0.009637 |
| waiting for handler commit     | 0.000018 |
| waiting for handler commit     | 0.003215 |
| waiting for handler commit     | 0.000009 |
| waiting for handler commit     | 0.005669 |
| waiting for handler commit     | 0.000011 |
| waiting for handler commit     | 0.002264 |
| end                            | 0.001772 |
| query end                      | 0.001428 |
| closing tables                 | 0.000009 |
| waiting for handler commit     | 0.000020 |
| freeing items                  | 0.002654 |
| cleaning up                    | 0.000024 |
+--------------------------------+----------+
31 rows in set, 1 warning (0.01 sec)

mysql> show profile for query 17;
+--------------------------------+----------+
| Status                         | Duration |
+--------------------------------+----------+
| starting                       | 0.000695 |
| Executing hook on transaction  | 0.000007 |
| starting                       | 0.000021 |
| checking permissions           | 0.000006 |
| checking permissions           | 0.000006 |
| init                           | 0.000012 |
| Opening tables                 | 0.000183 |
| setup                          | 0.000051 |
| creating table                 | 0.000076 |
| After create                   | 0.014540 |
| System lock                    | 0.000018 |
| copy to tmp table              | 0.000133 |
| rename result table            | 0.000799 |
| waiting for handler commit     | 0.000011 |
| waiting for handler commit     | 0.001753 |
| waiting for handler commit     | 0.000009 |
| waiting for handler commit     | 0.009314 |
| waiting for handler commit     | 0.000015 |
| waiting for handler commit     | 0.002635 |
| waiting for handler commit     | 0.000010 |
| waiting for handler commit     | 0.001726 |
| end                            | 0.000372 |
| query end                      | 0.001345 |
| closing tables                 | 0.000009 |
| waiting for handler commit     | 0.001833 |
| freeing items                  | 0.002656 |
| cleaning up                    | 0.000022 |
+--------------------------------+----------+
27 rows in set, 1 warning (0.00 sec)
```
  
4. Конфиг my.cnf:  
[итоговый конфиг](https://github.com/Serg2123/devops-netology/blob/main/my.cnf)  
Скорость IO важнее надежности данных: innodb_flush_method = O_DSYNC.  
По сжатию, сначала включаем innodb_file_per_table = 1 чтоб каждую таблицу вести в отдельном файле, потом можно при необходимости отдельные таблицы пожать.  
Размер буфера незаконченных транзакций - innodb_log_buffer_size = 1M.  
Размер буфера кеширования в 30%: сейчас виртуалке в контейнере определен всего 1G, 30% от 1GB это 300MB, но на виртуалке уже сейчас сводобного только 82MB, т.е. это 8,2%, предлагается выставить хотя бы 10%: innodb_buffer_pool_size = 10M  
Размер файла логов операций innodb_log_file_size = 100M.  
По идее чем больше innodb_log_file_size тем выше IO, но и делать бесконечно большим данный лог так же нет смысла. В инете есть хорошие исследования и расчеты с разными алгоритмами как правильно вычислить innodb_log_file_size, например, эта статья: https://blog.programs74.ru/how-to-change-innodb_log_file_size-safely/   
Текущее значение до изменения около 50 МБ:  
```
mysql> show variables like 'innodb_log_file_size';
+----------------------+----------+
| Variable_name        | Value    |
+----------------------+----------+
| innodb_log_file_size | 50331648 |
+----------------------+----------+
1 row in set (0.00 sec)
```
