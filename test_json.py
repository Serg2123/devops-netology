#!/usr/bin/env python3
import sys
import os
import socket
import json
import yaml

host_list = ('drive.google.com', 'mail.google.com', 'google.com')
host_for_tests = {}
host_for_tests2 = {}

for host_site in host_list: # выполним первую проверку и заполним словать с элементами сайт:IP
    ip_site = socket.gethostbyname(host_site)
    host_for_tests [host_site] = ip_site
    host_for_tests2 [host_site] = [ip_site, 'default']

with open ('host_for_tests.json','w') as json_log:
    json_log.write (json.dumps(host_for_tests2, indent=2))

with open ('host_for_tests.yaml','w') as yaml_log:
    yaml_log.write (yaml.dump(host_for_tests2, indent=2, explicit_start=True, explicit_end=True))



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
            host_for_tests = {host_site: ip_current}
            host_for_tests2 [host_site] = [ip_current, 'new']

            #print ('\n')
            #print (host_for_tests2)

            #перезапишем файлики с обновленным словарем
            # в идеале конечно нужно было:
		#	1. загрузить в словарь данные из json и yaml файлов;
		#	2. обновить по ключу сбойный IP или даже удалить элемент из словаря со сбойным IP и добавить обратно новый
		#	3. записать словать обратно в 2 файла
		#	4. но т.к. мы все равно записываем словарь целиком, то думаю можно и так, заново записав словарь поверх текущих данных.
		#	5. значения в словаре представлены ввиде списка, так что бы наглядно было видно какой именно IP изменился.
            with open ('host_for_tests.json','w') as json_log:
                 json_log.write (json.dumps(host_for_tests2, indent=2))

            with open ('host_for_tests.yaml','w') as yaml_log:
                 yaml_log.write (yaml.dump(host_for_tests2, indent=2, explicit_start=True, explicit_end=True))

            exit ()


