1. Про Docker Swarm:  
    1.1. Реплицированные service - указанное количество реплицируемых контейнеров распределяются между узлами на основе выбранной вручную или автоматически стратегии планированния.  
    Глобальные service - один контейнер запускается на каждом доступном узле в кластере.  

    1.2. алгоритмом распределённого консенсуса Raft (алгоритм бунтарей ;) т.е. нод, которые не получая некоторое время данных от лидера сами объявляют выборы).  

    1.3. Overlay Network - тип изолированной виртуальной сети, строящейся на изолированых виртуальных интерфейсах для либо для внутренних коммуникаций в кластере либо для организации специального общения между собой узлов в кластере (обеспечение изолированного потока прикладного/инфраструктурного/менеджмент трафика).  

2. Docker Swarm кластер в Яндекс.Облаке:  
[скриншот кластера](https://github.com/Serg2123/devops-netology/blob/main/pics/swarm.png)    

3.кластер мониторинга:  
[скриншот кластера мониторинга](https://github.com/Serg2123/devops-netology/blob/main/pics/monitoring.png)  

4. docker swarm update --autolock=true  
Это включение функционала шифрования чувствительных данных, есть только в docker swarm, просто в докере нет.  
К чувствительным данным относятся журналы Raft, а так же данные (имена пользователей и пароли, TLS-сертификаты и ключи, SSH-ключи, другие важные данные,такие как имя базы данных или внутреннего сервера), которые могут быть защинены новой фунцией Docker Secret.  
При включении шифрования docker swarm при перезагрузке будет требовать разблокировки с ключем (сгенерированным при включении данной функции), что бы открыть доступ к данным.  

