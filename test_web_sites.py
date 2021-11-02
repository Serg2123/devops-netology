#!/usr/bin/env python3
import sys
import os
import socket

host_list = ('drive.google.com', 'mail.google.com', 'google.com')
host_for_tests = {}

for host_site in host_list: # выполним первую проверку и заполним словать с элементами сайт:IP
    ip_site = socket.gethostbyname(host_site)
    host_for_tests [host_site] = ip_site
#    print (ip_site)
print ('Будем мониторить данные сайты и их дефолтные IP полученные в результе первой проверки:' + '\n' + str(host_for_tests))

#print (type(list_ip))
print ('\n'+'\n'+'Погнали, проверяем доступность сайтов в цикле')
while True: # запустим бесконечный цикл проверок внутри которого будем проверять сайты из словаря
    for host_site, ip_site in host_for_tests.items():  # цикл проверки по словарю в котором элементы состоят из сайт:IP
        ip_current = socket.gethostbyname(host_site)
        #ip_current = '192.168.1.1' # ручной "стоп-кран" чтоб не гонять долго цикл
        if ip_current == ip_site: 
            print (host_site + ':  текущий IP - ' +ip_current + ', IP из первой проверки - '+ ip_site )
        else: 
            print ('Для '+host_site + ' IP не сходятся, было - ' + ip_site + ', стало - '+ ip_current)
            
            #print (f'[ERROR] {host_site} IP mismatch: {ip_site} {ip_current}')
            print ('\n')
            my_error_to_stdout = sys.stdout
            my_error_to_stdout.write(f'[ERROR] {host_site} IP mismatch: {ip_site} {ip_current}')

            exit ()


