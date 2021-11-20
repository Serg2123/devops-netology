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
Мобильное приложение c версиями для Android и iOS - если это просто веб-приложение то в докере, если это одновременно и сервер/студия для отладки с кучей специального - то вирутальная софта под android/iOS - тогда выделенная вирт.машина (могу ошибаться, с данной темой не знаком);  
Шина данных на базе Apache Kafka - docker, т.к. одна из задач в таком решении масштабирование по запросу;  
Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana - вполне можно использовать контейнеры (не в чистом виде докер), например, под управлением кубера, для задач автоматизации развертывания, управления балансировкой   
Мониторинг-стек на базе Prometheus и Grafana - так же можно запускать в докере. В общем все что поиграться, потестировать, посмотреть, без серьезной нагрузки и балансировки - в докере. Как только серьезная нагрузка требующая балансировки (какими-то штатными инструментами) - тогда сверху кубер или все в виртуалки.   
MongoDB, как основное хранилище данных для java-приложения - отдельная виртуальная машина или физическая машина (все зависит еще от типа кластера и количества нод в нем, объемов данных, дисками которыми располагают серверы. Ссли нужно будет масштабировать по запросу - то виртуалки лучше, если сохранность данных - то сокрее однотипные физические серверы с кучей дисков или распределенной "СХД").  
Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry - отдельная виртуальная машина   

3.  
```
C:\Ubuntu.Netology>vagrant --version  
Vagrant 2.2.18  
```
```
 vagrant@vagrant:~$ ansible --version  
ansible [core 2.11.5]  
  config file = /etc/ansible/ansible.cfg  
  configured module search path = ['/home/vagrant/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']  
  ansible python module location = /usr/lib/python3/dist-packages/ansible  
  ansible collection location = /home/vagrant/.ansible/collections:/usr/share/ansible/collections  
  executable location = /usr/bin/ansible  
  python version = 3.8.10 (default, Sep 28 2021, 16:10:42) [GCC 9.3.0]  
  jinja version = 2.10.1  
  libyaml = True  
```
```
C:\Program Files\Oracle\VirtualBox>VBoxManage.exe -version  
6.1.26r145957  
```
4.  
Повторить в точности конфигурацию не получилось, т.к. основная рабочая станция под Windows, как из одной VM под Vagran-том создать дургую такую же рядом и осуществить ее провижининг я пока не понял :(  
Но автоматизировать установку docker-а через локальный запуск playbook-a (который размещается на виндовс-хост машине) получилось:  
[Playbook файл](https://github.com/Serg2123/devops-netology/blob/main/provision.yml)  
[Vagrant конфиг файл](https://github.com/Serg2123/devops-netology/blob/main/Vagrantfile)  
[Vagrant up - лог файл](https://github.com/Serg2123/devops-netology/blob/main/vagrant_up.log)  
```
vagrant@server4:~$ sudo -i  
root@server4:~# docker ps  
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES  
root@server4:~# docker --version  
Docker version 20.10.10, build b485636  
root@server4:~#  
```
