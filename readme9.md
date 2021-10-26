1 и 2  в картинке:  
![answer in picture](https://github.com/Serg2123/devops-netology/blob/main/bitwarden.png)
  
3.  
поправим конфиг /etc/ss/openssl.cnf:  
добавимим расширенные параметры что браузеры не ругались на самоподписанные сертификаты:  
```
[ v3_req ]  
subjectAltName = @alt_names  
[ alt_names ]  
DNS.1 = some.moscow  
DNS.2 = www.some.moscow  
IP.1 = 192.168.200.189  
```
сгенерим ключи c расширенными параметрами:  
```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt -extensions v3_req'  
```
включим ssl в конфигах апача добавив ssl-params.conf (параметры и протоколы шифрования) и default-ssl.conf добавив в него пути к сгенеренным ключам.  
результат в аттаче на картинке apach2:  
![answer in picture](https://github.com/Serg2123/devops-netology/blob/main/apache2.png)
  
4. проверим на уязвимости сами себя, т.к. у многих сайтов в DNS зарегистрированно много IP адресов и эта утилина начинает сканить по всем адресам:  
```
./testssl.sh -e --fast --parallel https://some.moscow > report.txt  
```
[Сам отчет о тестировании](https://github.com/Serg2123/devops-netology/blob/main/report.txt)

5.снегерировали ключи командой:  
```
 ssh-keygen -t rsa -b 2048  
```
скопировали содержимое id_rsa.pub в конец файла /home/vagrant/.ssh/authorized_keys..
разрешили использование входа по ключам в /etc/ssh/sshd_config, основные параметры:
```
PubkeyAuthentication yes
AuthorizedKeysFile	%h/ .ssh/authorized_keys .ssh/authorized_keys2
```
Все, дале можно подключаться к самому себе командой: ssh vagrant@vagrant  
Для путти пришлось поменять формат ключа утилитой путти на более старый, иначе путти новый ключ не понимала, и выдавала ошибку с невозможностью подключить ругаясь на новый формат ключа.  
  
6. Переименуем /home/vagrant/.ssh/id_rsa в /home/vagrant/.ssh/id_rsa.bak  
Добавим в файл /etc/ssh/ssh_config в конец:  
``
Host some.moscow  
    IdentityFile /home/vagrant/.ssh/id_rsa.bak  
``
и далее в итоге:  
```
vagrant@vagrant:~$ ssh some.moscow
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-81-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue 26 Oct 2021 05:29:46 PM UTC

  System load:  0.15              Users logged in:         1
  Usage of /:   6.1% of 61.31GB   IPv4 address for dummy0: 169.254.1.1
  Memory usage: 43%               IPv4 address for eth0:   10.0.2.15
  Swap usage:   0%                IPv4 address for eth1:   192.168.200.189
  Processes:    134


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Tue Oct 26 17:26:42 2021 from 192.168.200.189
vagrant@vagrant:~$
```
7. Захватим 100 пакетов в файл:  
```
sudo tcpdump -c 100 -nn -v -w trafic.pcap  
```
откроем дамп консольным вариантом Wireshark:  
```
tshark -r trafic.bin.pcap  
```


