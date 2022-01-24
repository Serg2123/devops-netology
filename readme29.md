1.  
[докер образ](https://hub.docker.com/repository/docker/serg2123/elastic-custom)  
[Dockerfile](https://github.com/Serg2123/devops-netology/blob/main/elastic/Dockerfile)  
[elasticsearch конфиг](https://github.com/Serg2123/devops-netology/blob/main/elastic/elasticsearch.yml)  
[elastic ответ в json](https://github.com/Serg2123/devops-netology/blob/main/elastic/elastic.json)  
[elastic ответ в jpg](https://github.com/Serg2123/devops-netology/blob/main/elastic/elastic.jpg)  
запускается так:  
```
docker run --rm -it --ulimit nofile=65535:65535 -p 9200:9200 elastic-custom
```
пришлось немного повоевать с этим:  
```
sysctl -w vm.max_map_count=262144
```
2.  
список всех индексов (глобальный запрос по кластеру):  
```
 curl -X GET "192.168.200.163:9200/_aliases?pretty=true"
{
  "ind-2" : {
    "aliases" : { }
  },
  "ind-1" : {
    "aliases" : { }
  },
  "ind-3" : {
    "aliases" : { }
  }
}
```
Тоже список всех индексов (со статусами и здоровьем):  
```
vagrant@server4:~/Elastic$ curl -X GET "192.168.200.163:9200/_cat/indices?v&pretty"
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases JI03Qgv9SPmkz0-tbNDzfw   1   0         42            0     40.4mb         40.4mb
green  open   ind-1            l2PKXnmqTaWrPmVIWXIgBA   1   0          0            0       226b           226b
yellow open   ind-3            X2iuMfSCRpqSOXAiFeCPvw   4   2          0            0       904b           904b
yellow open   ind-2            mpKTELojRHyUfZ9iiA02iw   2   1          0            0       452b           452b
```
Health - желтый, т.к. 2 и 3 индексы имеют более чем по 1 шарду и они не распределены.  
Статус кластера:  
```
curl -XGET 'http://localhost:9200/_cluster/health?pretty=true'
{
  "cluster_name" : "elastic-cluster",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 10,
  "active_shards" : 10,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
```
Удаление индексов:  
```
vagrant@server4:~/Elastic$ curl -X DELETE "localhost:9200/ind-1?pretty"
{
  "acknowledged" : true
}
vagrant@server4:~/Elastic$ curl -X DELETE "localhost:9200/ind-2?pretty"
{
  "acknowledged" : true
}
vagrant@server4:~/Elastic$ curl -X DELETE "localhost:9200/ind-3?pretty"
{
  "acknowledged" : true
}
```
проверка что индексов нет:  
```
vagrant@server4:~/Elastic$ curl -X GET "192.168.200.163:9200/_cat/indices?v&pretty"
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases JI03Qgv9SPmkz0-tbNDzfw   1   0         42            0     40.4mb         40.4mb
```
3.  
Добавим в конфиг elasticsearch.yml:  
```
path.repo: /elasticsearch/snapshots
```
далее заново сбилдим и запустим образ.  
Зарегистрируем snapshot repository:  
```
curl -X PUT "localhost:9200/_snapshot/netology_backup?pretty" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/elasticsearch/snapshots"
  }
}
'
{
  "acknowledged" : true
}
```
Создадим индекс тест:  
```
curl -X PUT "192.168.200.163:9200/test?pretty" -H 'Content-Type: application/json' -d'
 {
   "settings": {
     "index": {
       "number_of_shards": 1,
       "number_of_replicas": 0
     }
   }
 }
 '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test"
}

curl -X GET http://localhost:9200/_cat/indices
green open .geoip_databases 14i21zyERx22S7JTyuUWTQ 1 0 42 0 40.4mb 40.4mb
green open test             weNbPe7FQ8CYS6Ek5tdT8A 1 0  0 0   226b   226b
```
Создам снепшот:  
```
 curl -X PUT "localhost:9200/_snapshot/netology_backup/%3Cmy_snapshot2_%7Bnow%2Fd%7D%3E?pretty
&wait_for_completion=true"
{
  "snapshot" : {
    "snapshot" : "my_snapshot2_2022.01.24",
    "uuid" : "G1qoTfFPRl2ftHTa1KoRXA",
    "repository" : "netology_backup",
    "version_id" : 7160399,
    "version" : "7.16.3",
    "indices" : [
      "test",
      ".ds-ilm-history-5-2022.01.24-000001",
      ".geoip_databases",
      ".ds-.logs-deprecation.elasticsearch-default-2022.01.24-000001"
    ],
    "data_streams" : [
      "ilm-history-5",
      ".logs-deprecation.elasticsearch-default"
    ],
    "include_global_state" : true,
    "state" : "SUCCESS",
    "start_time" : "2022-01-24T21:16:27.813Z",
    "start_time_in_millis" : 1643058987813,
    "end_time" : "2022-01-24T21:16:28.014Z",
    "end_time_in_millis" : 1643058988014,
    "duration_in_millis" : 201,
    "failures" : [ ],
    "shards" : {
      "total" : 4,
      "failed" : 0,
      "successful" : 4
    },
    "feature_states" : [
      {
        "feature_name" : "geoip",
        "indices" : [
          ".geoip_databases"
        ]
      }
    ]
  }
}
```
Посмотрим на созданный снепшот:  
```
vagrant@server4:~/Elastic$ curl -X GET "localhost:9200/_snapshot/netology_backup/my_snapshot2_2022.01.24?pretty"
{
  "snapshots" : [
    {
      "snapshot" : "my_snapshot2_2022.01.24",
      "uuid" : "G1qoTfFPRl2ftHTa1KoRXA",
      "repository" : "netology_backup",
      "version_id" : 7160399,
      "version" : "7.16.3",
      "indices" : [
        "test",
        ".ds-ilm-history-5-2022.01.24-000001",
        ".geoip_databases",
        ".ds-.logs-deprecation.elasticsearch-default-2022.01.24-000001"
      ],
      "data_streams" : [
        "ilm-history-5",
        ".logs-deprecation.elasticsearch-default"
      ],
      "include_global_state" : true,
      "state" : "SUCCESS",
      "start_time" : "2022-01-24T21:16:27.813Z",
      "start_time_in_millis" : 1643058987813,
      "end_time" : "2022-01-24T21:16:28.014Z",
      "end_time_in_millis" : 1643058988014,
      "duration_in_millis" : 201,
      "failures" : [ ],
      "shards" : {
        "total" : 4,
        "failed" : 0,
        "successful" : 4
      },
      "feature_states" : [
        {
          "feature_name" : "geoip",
          "indices" : [
            ".geoip_databases"
          ]
        }
      ]
    }
  ],
  "total" : 1,
  "remaining" : 0
}
```
список файлов с индексами:  
```
[elasticsearch@8b00bdff1304 snapshots]$ ls -l
total 84
-rw-r--r-- 1 elasticsearch elasticsearch  1982 Jan 24 21:16 index-1
-rw-r--r-- 1 elasticsearch elasticsearch     8 Jan 24 21:16 index.latest
drwxr-xr-x 6 elasticsearch elasticsearch  4096 Jan 24 21:01 indices
-rw-r--r-- 1 elasticsearch elasticsearch 29189 Jan 24 21:16 meta-G1qoTfFPRl2ftHTa1KoRXA.dat
-rw-r--r-- 1 elasticsearch elasticsearch 29189 Jan 24 21:01 meta-W-jtRJwcSkujqF0DZAUPwA.dat
-rw-r--r-- 1 elasticsearch elasticsearch   722 Jan 24 21:16 snap-G1qoTfFPRl2ftHTa1KoRXA.dat
-rw-r--r-- 1 elasticsearch elasticsearch   721 Jan 24 21:01 snap-W-jtRJwcSkujqF0DZAUPwA.dat
[elasticsearch@8b00bdff1304 snapshots]$
```
удалим текущий индекс и создадим новый:  
```
curl -X DELETE "localhost:9200/test?pretty"
{
  "acknowledged" : true
}

curl -X PUT "192.168.200.163:9200/test-2?pretty" -H 'Content-Type: application/json' -d'
 {
   "settings": {
     "index": {
       "number_of_shards": 1,
       "number_of_replicas": 0
     }
   }
 }
 '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test-2"
}

curl -X GET "localhost:9200/_cat/indices"
green open .geoip_databases 14i21zyERx22S7JTyuUWTQ 1 0 42 0 40.4mb 40.4mb
green open test-2           SyQYWC4EScagQJMi-pPNBg 1 0  0 0   226b   226b
```
Последовательно выполним 6 шагов (так по инструкции) по восстановлению состояния кластера.  
1. Выключаем индексирование и разные фичи:  
```
curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
> {
>   "persistent": {
>     "ingest.geoip.downloader.enabled": false
>   }
> }
> '
{
  "acknowledged" : true,
  "persistent" : {
    "ingest" : {
      "geoip" : {
        "downloader" : {
          "enabled" : "false"
        }
      }
    }
  },
  "transient" : { }
}

curl -X POST "localhost:9200/_ilm/stop?pretty"
{
  "acknowledged" : true
}

curl -X POST "localhost:9200/_ml/set_upgrade_mode?enabled=true&pretty"
{
  "acknowledged" : true
}

curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
> {
>   "persistent": {
>     "xpack.monitoring.collection.enabled": false
>   }
> }
> '
{
  "acknowledged" : true,
  "persistent" : {
    "xpack" : {
      "monitoring" : {
        "collection" : {
          "enabled" : "false"
        }
      }
    }
  },
  "transient" : { }
}

curl -X POST "localhost:9200/_watcher/_stop?pretty"
{
  "acknowledged" : true
}
```
2. Снимаем блокироваки для удаления данных:  
```
vagrant@server4:~/Elastic$ curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
> {
>   "persistent": {
>     "action.destructive_requires_name": false
>   }
> }
> '
{
  "acknowledged" : true,
  "persistent" : {
    "action" : {
      "destructive_requires_name" : "false"
    }
  },
  "transient" : { }
}
```
3. удаляем все данные:  
```
vagrant@server4:~/Elastic$ curl -X DELETE "localhost:9200/_data_stream/*?expand_wildcards=all&pretty"
{
  "acknowledged" : true
}
vagrant@server4:~/Elastic$ curl -X DELETE "localhost:9200/*?expand_wildcards=all&pretty"
{
  "acknowledged" : true
}
```
4. Восстанавливаем состояние кластера:  
```
vagrant@server4:~/Elastic$ curl -X POST "localhost:9200/_snapshot/netology_backup/my_snapshot2_2022.01.24/_restore?pretty" -H 'Content-Type: application/json' -d'
> {
>   "indices": "*",
>   "include_global_state": true
> }
> '
{
  "accepted" : true
}
```
5. включаем обратно индексирование и разные фичи:  
```
vagrant@server4:~/Elastic$ curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
tent": {
    "ingest.geoip.downloader.enabled": true
  }
}
'
> {
>   "persistent": {
>     "ingest.geoip.downloader.enabled": true
>   }
> }
> '
{
  "acknowledged" : true,
  "persistent" : {
    "ingest" : {
      "geoip" : {
        "downloader" : {
          "enabled" : "true"
        }
      }
    }
  },
  "transient" : { }
}
vagrant@server4:~/Elastic$ curl -X POST "localhost:9200/_ilm/start?pretty"
{
  "acknowledged" : true
}
vagrant@server4:~/Elastic$ curl -X POST "localhost:9200/_ml/set_upgrade_mode?enabled=false&pretty"
{
  "acknowledged" : true
}
vagrant@server4:~/Elastic$ curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
> {
>   "persistent": {
>     "xpack.monitoring.collection.enabled": true
>   }
> }
> '
{
  "acknowledged" : true,
  "persistent" : {
    "xpack" : {
      "monitoring" : {
        "collection" : {
          "enabled" : "true"
        }
      }
    }
  },
  "transient" : { }
}
vagrant@server4:~/Elastic$ curl -X POST "localhost:9200/_watcher/_start?pretty"
{
  "acknowledged" : true
}
```
6. Смотрим что получилось и какие индексы в наличии:  
```
vagrant@server4:~/Elastic$ curl -X GET "localhost:9200/_cat/indices"
green open .geoip_databases            0UcTo0_TST-Im2RhO54PSg 1 0 42  0  40.4mb  40.4mb
green open test                        bnGcLJi5Rq-oft49m-aqJg 1 0  0  0    226b    226b
green open .monitoring-es-7-2022.01.24 hFHJOwJtTl6D8Z4fHLpsaQ 1 0 40 10 299.3kb 299.3kb
```
test-2 - нет, в наличии только test, плюс появился мониторинговый индекс который мы включи в составе фич и внутренних сервисов после восставновления.  