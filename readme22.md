1.  
Скачал контейнер, зашел внутрь, нашел index.html, заменил, сделал коммит, переименовал репозитарий на локальный и совпадающий с тем что создал в https://hub.docker.com/, залогинился с консоли, сделал push.  
Остановил работающий контейнер, удалил контейнер, удалил образ контейнера, сказал заново образ, запустил контейнер - и изменений нет, и так раза 3 ((.  
Так и не понял в какой момент измения таки закомитились и нормально отправили в hub.docker.com.
Правильный докер образ (правда распухший от того что поставил туда nano и mc) туперь тут: 
[докер образ](https://hub.docker.com/layers/178419876/serg2123/repo-netology/new5.html/images/sha256-674764a7c40b8466158d9e3fe62b8e635bddc4a13436e17a6b782fff40763ad8?context=repohttps://hub.docker.com/layers/178419876/serg2123/repo-netology/new5.html/images/sha256-674764a7c40b8466158d9e3fe62b8e635bddc4a13436e17a6b782fff40763ad8?context=repo)

2. 
    Высоконагруженное монолитное java веб-приложение - раньше были явные проблемы запуска java приложений в контейнерах,
т.к. JVM не имела средств, позволяющих определить, что она выполняется в контейнеризированной среде и соотвественно это не позволяло учесть ограничения по памяти и процессору, из-за это невозможно было использовать механизм автоматического определения кучи.  
Были разные обходные решения, в том числе кастомные образы - Fabric8 Base. В последних версиях Java включили поддержку контейнеров, тем не менее я бы все равно тяжелы Java приложения запускал бы только на виртуалках.  
    
    Nodejs веб-приложение - docker.  
    
    Мобильное приложение c версиями для Android и iOS - если это просто веб-приложение то в докере, если это одновременно и сервер/студия для отладки с кучей специального ПО под android/iOS - тогда выделенная вирт.машина (могу ошибаться, с данной темой не знаком);  
    
    Шина данных на базе Apache Kafka - docker, точнее в кубере, т.к. одна из задач в таком решении масштабирование по запросу;  

    Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana - вполне можно использовать контейнеры (не в чистом виде докер), например, под управлением кубера, для задач автоматизации развертывания, управления балансировкой   
    
    Мониторинг-стек на базе Prometheus и Grafana - так же можно запускать в докере. В общем все что поиграться, потестировать, посмотреть, без серьезной нагрузки и балансировки - в докере. Как только серьезная нагрузка требующая балансировки (какими-то штатными инструментами) - тогда сверху кубер или все в виртуалки.  

    MongoDB, как основное хранилище данных для java-приложения - отдельная виртуальная машина или физическая машина (все зависит еще от типа кластера и количества нод в нем, объемов данных, дисков которыми располагают серверы. Если нужно будет масштабировать по запросу - то виртуалки лучше, если сохранность данных приоритетнее - то сокрее однотипные физические серверы с кучей дисков).  

    Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry - отдельная виртуальная машина   

3.  
Создадим и запустим 2 контейнера в фоне на базе голых OS debian и centos, применим команду слип что бы контейнеры продолжали работать в фоне и не завершались автоматически будучи отцепленными и без назначенных к выполнению скриптов.  
```
root@server4:/# docker images
REPOSITORY               TAG         IMAGE ID       CREATED        SIZE
serg2123/repo-netology   new5.html   b01d0a454ef0   12 hours ago   241MB
debian                   latest      827e5611389a   4 days ago     124MB
centos                   latest      5d0da3dc9764   2 months ago   231MB
root@server4:/# docker run --rm -d -v /vagrant_data:/data --name cent_container centos:latest /bin/sh -c 'exec sleep 300
00'
b48d5db61155229bfbe51e475596d844281b74600fb3620b1b5dc53412e947cd
root@server4:/# docker run --rm -d -v /vagrant_data:/data --name deb_container debian:latest /bin/sh -c 'exec sleep 30000'
486af5d4b3c564db8a38289326f028df6b5af8c9a60f70b8978c361372d90760
root@server4:/# docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS     NAMES
486af5d4b3c5   debian:latest   "/bin/sh -c 'exec sl…"   23 seconds ago   Up 23 seconds             deb_container
b48d5db61155   centos:latest   "/bin/sh -c 'exec sl…"   41 seconds ago   Up 40 seconds             cent_container
```
Подключитмся в первый контейнер и создадим тестовый файлик на подключенном диске:  
```
root@server4:/# docker exec -it cent_container bash
[root@b48d5db61155 /]# cd data
[root@b48d5db61155 data]# ls
Vagrantfile  bad_script.sh  id_rsa.pub       provision.yml  readme8.md  vagrant.ppk
ansible      id_rsa         key_genegate.md  readme10.md    readme9.md  vagrant_up.log
t_os_container.log data]# echo 'Тестовый вывод в файл на внешнем диске' > from.cen
[root@b48d5db61155 data]# ls
Vagrantfile  bad_script.sh               id_rsa      key_genegate.md  readme10.md  readme9.md   vagrant_up.log
ansible      from.cent_os_container.log  id_rsa.pub  provision.yml    readme8.md   vagrant.ppk
[root@b48d5db61155 data]# cat from.cent_os_container.log
Тестовый вывод в файл на вг�нешнем диске � �
[root@b48d5db61155 data]# exit
exit
```
Перейдем в хостовую ОС, проверим наличие файлика из первого контейнера:   
```
vagrant@server4:/vagrant_data$ ls
ansible        from.cent_os_container.log  id_rsa.pub       provision.yml  readme8.md  Vagrantfile  vagrant_up.log
bad_script.sh  id_rsa                      key_genegate.md  readme10.md    readme9.md  vagrant.ppk
vagrant@server4:/vagrant_data$ cat from.cent_os_container.log
Тестовый вывод в файл на вг�нешнем диске � �
```
создадим тестовый файлик для второго контейнера:
```
vagrant@server4:/vagrant_data$ echo 'временные данные для debian контейнера' > for.debian_container.log
vagrant@server4:/vagrant_data$ ls
ansible        for.debian_container.log    id_rsa      key_genegate.md  readme10.md  readme9.md   vagrant.ppk
bad_script.sh  from.cent_os_container.log  id_rsa.pub  provision.yml    readme8.md   Vagrantfile  vagrant_up.log
vagrant@server4:/vagrant_data$ cat for.debian_container.log
временные данные для debian контейнера
vagrant@server4:/vagrant_data$
```
Подключимся во второй контейнер и проверим наличите второго тестового файлика:
```
root@server4:/# docker exec -it deb_container bash
root@486af5d4b3c5:/# cd data
root@486af5d4b3c5:/data# ls
Vagrantfile    for.debian_container.log    id_rsa.pub       readme10.md  vagrant.ppk
ansible        from.cent_os_container.log  key_genegate.md  readme8.md   vagrant_up.log
bad_script.sh  id_rsa                      provision.yml    readme9.md
root@486af5d4b3c5:/data# cat for.debian_container.log
временные данные для debian контейнера
```
4.  
Использованный Dockerfile для локальной сборки образа:  
[Dockerfile](https://github.com/Serg2123/devops-netology/blob/main/ansible/Dockerfile)  
Лог вывода сборки:  
[лог](https://github.com/Serg2123/devops-netology/blob/main/ansible/build_ansible_2.9.24.log)  
опубликованный ansible образ:  
[Ansible образ](https://hub.docker.com/layers/178460184/serg2123/ansible/2.9.24/images/sha256-2000ed8b21937e5c19e2219d388e64312e31afef636f4ded95dbe18ce54643ca?context=repo)  
