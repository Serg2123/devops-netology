1.  
•  основные преимущества применения на практике IaaC паттернов:  
    o	ускорение подготовки инфраструктуры для разработки, тестирования и масштабирования по мере необходимости;  
    o	обеспечение стабильности среды, предотвращение «дрейфа» конфигураций;  
    o	повышение скорости разработки в целом (более быстрое развертывание всех необходимых сред);  
•  идемпотентность – обеспечение идентичного результата при повторном и следующих повторениях.  

2.  
•  стал почти стандартом ввиду того что работает на без агентной модели подключаясь к хостам по ssh, не нужно ставить ни агентов, ни отдельную PKI инфраструктуру;  
•  считается что pull-модель распространения конфигураций более надежна, но под пулл модель нужно отдельно заранее готовить образ ОС или какой-то внешний инициализирующий скрипт, который установит агента который уже и будет pull-ить основной сервер конфигураций.  

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
