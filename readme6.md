1. HTTP/1.1 301 Moved Permanently, стандартный код ответа HTTP, получаемый в ответ от сервера в ситуации, 
когда запрошенный ресурс был на постоянной основе перемещён в новое месторасположение, и указывающий на то, что текущие ссылки, 
использующие данный URL, должны быть обновлены.  
Предложено перейти на URL https://stackoverflow.com/questions  
  
2. первый ответ в Firefox такой же 301 (только не успел заголовки скопировать), а вот в хроме первый ответ уже 200 (видимо кеш где-то по дороге сработал), и в FF все ответы уже 200 (тут уже локальный кеш видимо работает).  
Ответы для кода 200:  
HTTP/2 200 OK  
cache-control: private  
content-type: text/html; charset=utf-8  
content-encoding: gzip  
strict-transport-security: max-age=15552000  
x-frame-options: SAMEORIGIN  
x-request-guid: 0fdb8f55-a87b-430d-8f50-f5d1539a212d  
feature-policy: microphone 'none'; speaker 'none'  
content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com  
accept-ranges: bytes  
date: Mon, 04 Oct 2021 11:31:17 GMT  
via: 1.1 varnish  
x-served-by: cache-fra19179-FRA  
x-cache: MISS  
x-cache-hits: 0  
x-timer: S1633347078.562141,VS0,VE89  
vary: Accept-Encoding,Fastly-SSL  
x-dns-prefetch-control: off  
X-Firefox-Spdy: h2  
  
Дольше всего обрабатывался этот запрос (58мс), видимо получения анимации с CDN:  
GET https://cdn.sstatic.net/Js/product-animations.en.js?v=225ab94481a4  
скриншоты в файлах 301.png (первый запрос) 200.png (второй запрос)  
  
3. 91.78.85.238 (мгтс/мтс, через https://2ip.ru/)  
ZAO MTU-Intel's Moscow Region Network (по факту это MTS backbone NOC), AS8359  
  
vagrant@vagrant:~/devops-netology$ whois -h whois.radb.net 91.78.85.238  
route:          91.76.0.0/14  
descr:          ZAO MTU-Intel's Moscow Region Network  
descr:          ZAO MTU-Intel  
descr:          Moscow, Russia  
origin:         AS8359  
mnt-by:         MTU-NOC  
created:        2006-09-13T10:51:37Z  
last-modified:  2006-09-13T10:51:37Z  
source:         RIPE  
  
4. AS8402, AS8359, AS15169  
vagrant@vagrant:~$ sudo traceroute -nAi eth1 8.8.8.8  
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets  
 1  192.168.200.1 [*]  34.083 ms  33.982 ms  33.953 ms  
 2  192.168.100.1 [*]  33.893 ms  33.855 ms  33.825 ms  
 3  192.168.10.1 [*]  33.909 ms  33.673 ms 78.107.125.205 [AS8402]  33.691 ms  
 4  91.77.64.1 [AS8359]  33.792 ms 78.107.1.214 [AS8402]  33.479 ms  33.580 ms  
 5  212.188.1.106 [AS8359]  33.619 ms  33.579 ms 10.2.254.82 [*]  33.536 ms  
 6  212.188.1.105 [AS8359]  33.490 ms 195.14.54.139 [AS8402]  6.700 ms 212.188.1.105 [AS8359]  7.290 ms  
 7  212.188.56.13 [AS8359]  7.733 ms 213.234.224.131 [AS8402]  5.721 ms 213.234.224.150 [AS8402]  5.645 ms  
 8  85.21.93.129 [AS8402]  7.153 ms 85.21.224.191 [AS8402]  5.422 ms  5.319 ms  
 9  108.170.250.99 [AS15169]  6.801 ms 108.170.250.83 [AS15169]  6.022 ms 212.188.29.82 [AS8359]  6.611 ms  
10  10.23.140.126 [*]  16.990 ms * 10.23.140.190 [*]  16.793 ms  
11  216.239.51.32 [AS15169]  38.942 ms 209.85.255.136 [AS15169]  38.757 ms 108.170.250.83 [AS15169]  5.115 ms  
12  209.85.254.20 [AS15169]  27.936 ms 108.170.235.204 [AS15169]  27.872 ms 172.253.65.82 [AS15169]  27.809 ms  
13  216.239.62.13 [AS15169]  27.741 ms 172.253.66.116 [AS15169]  27.676 ms 209.85.251.63 [AS15169]  27.572 ms  
14  108.170.235.64 [AS15169]  27.446 ms 72.14.237.199 [AS15169]  27.384 ms *  
15  * * *  
16  * * *  
17  * * *  
18  * * *  
19  * * *  
20  * * *  
21  * * *  
22  8.8.8.8 [AS15169]  27.253 ms * *  
  
5.  на 14-м шаге (216.239.62.9)  
vagrant@vagrant:~$ mtr -w -c 10 8.8.8.8 > rep3  
vagrant@vagrant:~$ cat rep3  
Start: 2021-10-04T15:32:24+0000  
HOST: vagrant                                Loss%   Snt   Last   Avg  Best  Wrst StDev  
  1.|-- _gateway                               70.0%    10    0.4   0.5   0.4   0.7   0.2  
  2.|-- router.asus.com                        90.0%    10    2.3   2.3   2.3   2.3   0.0  
  3.|-- 192.168.100.1                          70.0%    10    2.5   4.0   2.5   6.4   2.0  
  4.|-- 192.168.10.1                           90.0%    10    3.7   3.7   3.7   3.7   0.0  
  5.|-- ppp91-77-64-1.pppoe.mtu-net.ru         70.0%    10   12.0   8.4   6.3  12.0   3.1  
  6.|-- mpts-a197-51.msk.mts-internet.net      90.0%    10    6.0   6.0   6.0   6.0   0.0  
  7.|-- a197-cr04-be12.51.msk.mts-internet.net 70.0%    10    7.3   7.6   7.3   7.8   0.3  
  8.|-- a197-cr01-ae31.77.msk.mts-internet.net 90.0%    10    8.3   8.3   8.3   8.3   0.0  
  9.|-- mag9-cr02-be10.77.msk.mts-internet.net 70.0%    10    7.2   8.2   6.8  10.5   2.0  
 10.|-- mag9-cr01-be16.77.msk.mts-internet.net 90.0%    10    7.9   7.9   7.9   7.9   0.0  
 11.|-- 108.170.250.51                         70.0%    10    7.4  11.2   7.4  17.5   5.4  
 12.|-- 142.251.49.158                         90.0%    10   22.3  22.3  22.3  22.3   0.0  
 13.|-- 74.125.253.94                          70.0%    10   22.6  24.4  22.6  26.7   2.1  
 14.|-- 216.239.62.9                           90.0%    10   24.6  24.6  24.6  24.6   0.0  
 15.|-- ???                                    100.0    10    0.0   0.0   0.0   0.0   0.0  
 16.|-- ???                                    100.0    10    0.0   0.0   0.0   0.0   0.0  
 17.|-- ???                                    100.0    10    0.0   0.0   0.0   0.0   0.0  
 18.|-- ???                                    100.0    10    0.0   0.0   0.0   0.0   0.0  
 19.|-- ???                                    100.0    10    0.0   0.0   0.0   0.0   0.0  
 20.|-- ???                                    100.0    10    0.0   0.0   0.0   0.0   0.0  
 21.|-- ???                                    100.0    10    0.0   0.0   0.0   0.0   0.0  
 22.|-- ???                                    100.0     9    0.0   0.0   0.0   0.0   0.0  
 23.|-- ???                                    100.0     9    0.0   0.0   0.0   0.0   0.0  
 24.|-- dns.google                             88.9%     9   24.3  24.3  24.3  24.3   0.0  
  
6. 8.8.8.8, 8.8.4.4  
и 2 A-записи:  
dns.google.             856     IN      A       8.8.4.4  
dns.google.             856     IN      A       8.8.8.8  
  
vagrant@vagrant:~/devops-netology$ nslookup dns.google  
Non-authoritative answer:  
Name:   dns.google  
Address: 8.8.8.8  
Name:   dns.google  
Address: 8.8.4.4  
Name:   dns.google  
Address: 2001:4860:4860::8844  
Name:   dns.google  
Address: 2001:4860:4860::8888  

vagrant@vagrant:~/devops-netology$ dig dns.google  
; <<>> DiG 9.16.1-Ubuntu <<>> dns.google  
;; global options: +cmd  
;; Got answer:  
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 2019  
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1  
  
;; OPT PSEUDOSECTION:  
; EDNS: version: 0, flags:; udp: 65494  
;; QUESTION SECTION:  
;dns.google.                    IN      A  
  
;; ANSWER SECTION:  
dns.google.             598     IN      A       8.8.8.8  
dns.google.             598     IN      A       8.8.4.4  
  
;; Query time: 0 msec  
;; SERVER: 127.0.0.53#53(127.0.0.53)  
;; WHEN: Mon Oct 04 15:42:46 UTC 2021  
;; MSG SIZE  rcvd: 71  

7.  
4.4.8.8.in-addr.arpa.   7176    IN      PTR     dns.google.  
8.8.8.8.in-addr.arpa.   3491    IN      PTR     dns.google.  

vagrant@vagrant:~/devops-netology$ dig -x 8.8.8.8  
; <<>> DiG 9.16.1-Ubuntu <<>> -x 8.8.8.8  
;; global options: +cmd  
;; Got answer:  
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 34391  
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1  
  
;; OPT PSEUDOSECTION:  
; EDNS: version: 0, flags:; udp: 65494  
;; QUESTION SECTION:  
;8.8.8.8.in-addr.arpa.          IN      PTR  
  
;; ANSWER SECTION:  
8.8.8.8.in-addr.arpa.   3441    IN      PTR     dns.google.  
  
;; Query time: 0 msec  
;; SERVER: 127.0.0.53#53(127.0.0.53)  
;; WHEN: Mon Oct 04 16:03:35 UTC 2021  
;; MSG SIZE  rcvd: 73  
