1. telnet route-server.opentransit.net  
rviews|Rviews  
  
OAKRS1#show ip route 109.252.138.35 255.255.255.255  
% Subnet not in table  
OAKRS1#show ip route 109.252.138.35  
Routing entry for 109.252.0.0/16  
  Known via "bgp 5511", distance 200, metric 100  
  Tag 3356, type internal  
  Last update from 193.251.245.252 2w3d ago  
  Routing Descriptor Blocks:  
  * 193.251.245.252, from 193.251.245.252, 2w3d ago  
      Route metric is 100, traffic share count is 1  
      AS Hops 3  
      Route tag 3356  
      MPLS label: none  
      MPLS Flags: NSF  
  
OAKRS1#show bgp 109.252.138.35  
BGP routing table entry for 109.252.0.0/16, version 347670  
Paths: (10 available, best #8, table default)  
Multipath: eBGP  
  Not advertised to any peer  
  Refresh Epoch 1  
  3356 8359 25513  
    4.68.73.153 from 193.251.245.7 (172.25.4.81)  
      Origin IGP, metric 100, localpref 85, valid, internal  
      Community: 5511:515 5511:666 5511:710  
      rx pathid: 0, tx pathid: 0  
      Updated on Sep 15 2021 20:26:23 EDT  
  Refresh Epoch 1  
  3356 8359 25513  
    4.68.73.109 from 193.251.245.196 (172.25.4.87)  
      Origin IGP, metric 100, localpref 85, valid, internal  
      Community: 5511:521 5511:666 5511:710  
      rx pathid: 0, tx pathid: 0  
      Updated on Sep 15 2021 20:26:10 EDT  
  Refresh Epoch 1  
  3356 8359 25513  
    4.68.73.97 from 193.251.245.36 (172.25.4.104)  
      Origin IGP, metric 100, localpref 85, valid, internal  
      Community: 5511:518 5511:666 5511:710  
      rx pathid: 0, tx pathid: 0  
      Updated on Sep 15 2021 20:26:06 EDT  
  Refresh Epoch 1  
  3356 8359 25513  
    4.68.70.173 from 193.251.245.237 (172.25.4.176)  
      Origin IGP, metric 100, localpref 85, valid, internal  
 --More--  
  
2. создадим новый конфиг для netplan /etc/netplan/02-dummy.yaml:  
```
network:  
  version: 2  
  renderer: networkd  
  bridges:  
    dummy0:  
      dhcp4: no  
      dhcp6: no  
      accept-ra: no  
      interfaces: [ ]  
      addresses:  
        - 169.254.1.1/32  
```
Применим его чезер netplan generate и apply.  
Проверим наличие:  
vagrant@vagrant:~/devops-netology$ ip -c a  
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000  
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00  
    inet 127.0.0.1/8 scope host lo  
       valid_lft forever preferred_lft forever  
    inet6 ::1/128 scope host  
       valid_lft forever preferred_lft forever  
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000  
    link/ether 08:00:27:73:60:cf brd ff:ff:ff:ff:ff:ff  
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0  
       valid_lft 85871sec preferred_lft 85871sec  
    inet6 fe80::a00:27ff:fe73:60cf/64 scope link  
       valid_lft forever preferred_lft forever  
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000  
    link/ether 08:00:27:7f:da:64 brd ff:ff:ff:ff:ff:ff  
    inet 192.168.200.189/24 brd 192.168.200.255 scope global dynamic eth1  
       valid_lft 85871sec preferred_lft 85871sec  
    inet6 fe80::a00:27ff:fe7f:da64/64 scope link  
       valid_lft forever preferred_lft forever  
4: dummy0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default qlen 1000  
    link/ether a6:da:c9:0d:b6:94 brd ff:ff:ff:ff:ff:ff  
    inet 169.254.1.1/32 scope global dummy0  
       valid_lft forever preferred_lft forever  
    inet6 fe80::a4da:c9ff:fe0d:b694/64 scope link  
       valid_lft forever preferred_lft forever  
Создадим пару статических маршрутов:  
vagrant@vagrant:~/devops-netology$ sudo ip route add 169.254.1.1 via 192.168.200.1  
vagrant@vagrant:~/devops-netology$ sudo ip route add 169.254.1.0/24 dev eth1 metric 50  
Проверим маршруты:  
vagrant@vagrant:~/devops-netology$ ip route list  
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100  
default via 192.168.200.1 dev eth1 proto dhcp src 192.168.200.189 metric 100  
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15  
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100  
169.254.1.0/24 dev eth1 scope link metric 50  
169.254.1.1 via 192.168.200.1 dev eth1  
192.168.200.0/24 dev eth1 proto kernel scope link src 192.168.200.189  
192.168.200.1 dev eth1 proto dhcp scope link src 192.168.200.189 metric 100  
  
Еще можно так:  
vagrant@vagrant:~/devops-netology$ netstat -r  
Kernel IP routing table  
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface  
default         _gateway        0.0.0.0         UG        0 0          0 eth0  
default         router.asus.com 0.0.0.0         UG        0 0          0 eth1  
10.0.2.0        0.0.0.0         255.255.255.0   U         0 0          0 eth0  
_gateway        0.0.0.0         255.255.255.255 UH        0 0          0 eth0  
169.254.1.0     0.0.0.0         255.255.255.0   U         0 0          0 eth1  
vagrant         router.asus.com 255.255.255.255 UGH       0 0          0 eth1  
192.168.200.0   0.0.0.0         255.255.255.0   U         0 0          0 eth1  
router.asus.com 0.0.0.0         255.255.255.255 UH        0 0          0 eth1  
  
3. vagrant@vagrant:~/devops-netology$ netstat -atlpn  
(Not all processes could be identified, non-owned process info  
 will not be shown, you would have to be root to see it all.)  
Active Internet connections (servers and established)  
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name  
tcp        0      0 127.0.0.1:8125          0.0.0.0:*               LISTEN      -  
tcp        0      0 0.0.0.0:19999           0.0.0.0:*               LISTEN      -  
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN      -  
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -  
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -  
tcp        0      0 10.0.2.15:22            10.0.2.2:52522          ESTABLISHED -  
tcp        0     72 10.0.2.15:22            10.0.2.2:58536          ESTABLISHED -  
tcp        0      0 127.0.0.1:43822         127.0.0.1:9090          ESTABLISHED -  
tcp        0      0 10.0.2.15:56236         204.59.3.38:23          ESTABLISHED 3505/telnet  
tcp6       0      0 ::1:8125                :::*                    LISTEN      -  
tcp6       0      0 :::9090                 :::*                    LISTEN      -  
tcp6       0      0 :::9100                 :::*                    LISTEN      -  
tcp6       0      0 :::111                  :::*                    LISTEN      -  
tcp6       0      0 :::22                   :::*                    LISTEN      -  
tcp6       0      0 ::1:9100                ::1:46480               ESTABLISHED -  
tcp6       0      0 ::1:55780               ::1:9090                ESTABLISHED -  
tcp6       0      0 ::1:46480               ::1:9100                ESTABLISHED -  
tcp6       0      0 ::1:9090                ::1:55780               ESTABLISHED -  
tcp6       0      0 127.0.0.1:9090          127.0.0.1:43822         ESTABLISHED -  
Запущен телнет с пид 3505 подключенный на 204.59.3.28.  
23 - стандартный порт для подключения по Telnet  
22 - стандартный порт для подключения по ssh  
53 - стандантный порт для DNS  
111 - порт для удаленного вызова SUNRPC  
  
4. vagrant@vagrant:~/devops-netology$ netstat -aulpn  
(Not all processes could be identified, non-owned process info  
 will not be shown, you would have to be root to see it all.)  
Active Internet connections (servers and established)  
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name  
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -  
udp        0      0 192.168.200.189:68      0.0.0.0:*                           -  
udp        0      0 10.0.2.15:68            0.0.0.0:*                           -  
udp        0      0 0.0.0.0:111             0.0.0.0:*                           -  
udp        0      0 127.0.0.1:8125          0.0.0.0:*                           -  
udp6       0      0 :::111                  :::*                                -  
udp6       0      0 ::1:8125                :::*                                -  
приложений использующих UDP - нет.
  
5. https://drive.google.com/file/d/1_AxHYypAUPF8T6Uslc69m2IXbmJRwZAN/view?usp=sharing  
