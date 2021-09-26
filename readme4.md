Операционные системы, #2  
  
1.  т.к. в системе отсустсововал Node_explorer то выполним его доустановку, причем ставится он вместе с прометеус..
    sudo apt install prometheus-node-exporter  
    он конечно насоздавал кучу своих конфигураций(юнитов) и положил все сюда, в дефолтный каталог для юнитов сервисов установленных из готовых пакетов:..
    /usr/lib/systemd/system/  
    возьмем наиболее нужный нам с node_explorer и переложим его (переименовав заодно) в пользовательский/админский каталог юнитов:  
    /etc/systemd/system/node-exporter.service
	[Unit]  
	Description=Prometheus exporter for machine metrics  
	[Service]  
	Restart=always  
	User=prometheus  
	EnvironmentFile=/etc/default/prometheus-node-exporter  
	ExecStart=/usr/bin/prometheus-node-exporter -f $EXTRA_OPTS  
	ExecReload=/bin/kill -HUP $MAINPID  
	TimeoutStopSec=20s  
	SendSIGKILL=no  
	[Install]  
	WantedBy=multi-user.target  
    Порядок запуска службы определяется в разделе [Service], за старт отвечет параметр ExecStart  
    Включение в автозагрузку осуществляется через активацию самого юнита:  
    root@vagrant:/etc/systemd/system# systemctl enable node-exporter.service  
    Created symlink /etc/systemd/system/multi-user.target.wants/node-exporter.service → /etc/systemd/system/node-exporter.service.  
    Добавление опций к запускаемому сервису через внешний файл осуществляется через ключ -f $EXTRA_OPTS  
    Служба успешно запускается, перезагружается, а так же стартует (после деакцивации основной службы от которой мы скорировались) после запуска ОС:  
    vagrant@vagrant:~$ systemctl status node-exporter.service  
    ● node-exporter.service - Prometheus exporter for machine metrics  
         Loaded: loaded (/etc/systemd/system/node-exporter.service; enabled; vendor preset: enabled)  
         Active: active (running) since Fri 2021-09-24 20:07:24 UTC; 1 day 15h ago  
         Main PID: 589 (prometheus-node)  
         Tasks: 5 (limit: 1112)  
         Memory: 11.0M  
         CGroup: /system.slice/node-exporter.service  
                 └─589 /usr/bin/prometheus-node-exporter  
    Sep 24 20:07:24 vagrant prometheus-node-exporter[589]: time="2021-09-24T20:07:24Z" level=info msg="   
2. Исходя из примеров документации на prometheus можно взять следующие параметры для оперативного онлайн мониторинга:  
    rate(node_cpu_seconds_total{mode="system"}[1m]) # среднее кол-во процессорного времени, затраченного в системном режиме, в секунду за последнюю минуту  
    node_memory_MemTotal_bytes - node_memory_Buffers_bytes - node_memory_Cached_bytes - node_memory_MemFree_bytes  # вычисляемое значение используемой памяти  
    node_filesystem_avail_bytes # колво места доступного пользователям за исключеним root  
    node_disk_writes_completed и node_disk_reads_completed  # метрики для отслеживания операций ввода/вывода с дисковой подсистемой  
    rate(node_network_receive_bytes_total[1m]) # средний трафик в сек за последнюю минуту  
3. Красочно, но названия метрик не совпадает с метками node_exporter, видимо тут своим метки и свои сборщики.
4. полагаю что да, может по следующему выводу dmesg:  
[    0.000000] Hypervisor detected: KVM  
[    0.000000] kvm-clock: Using msrs 4b564d01 and 4b564d00  
[    0.000001] kvm-clock: cpu 0, msr 27201001, primary cpu clock  
[    0.000001] kvm-clock: using sched offset of 42760651803 cycles  
[    0.000003] clocksource: kvm-clock: mask: 0xffffffffffffffff max_cycles: 0x1cd42e4dffb, max_idle_ns: 881590591483 ns  
    кроме того, наличие виртуализации можно опередлить иными путями:  
	dmidecode -s system-product-name  
	ls -1 /dev/disk/by-id/  
5.  /sbin/sysctl -n fs.nr_open  
    1048576  
    Максимальное количество дескрипторов файлов, которые может использовать процесс. Значение по умолчанию 1024 *1024 (1048576), обычно достаточно для большинства машин. Фактический лимит зависит от лимита ресурсов RLIMIT_NOFILE.  
    ulimit -Hn  
    1048576 # тоже самое количество максимальных возможных дескрипторов открытых файлов (жесткое ограничение)  
    ulimit -Sn  
    1024 # мягкое ограничение на количество дескрипторов открытых файлов, он и не позволит в первую очередь достичь fs.nr_open, но его можно в рамках сессии скорректировать. 
6.  
    root        5912  0.0  0.2   9900  2736 ?        Ss   14:43   0:00 SCREEN  
    root        5913  0.0  0.3  10152  3920 pts/3    Ss   14:43   0:00 /bin/bash  
    root        5920  0.0  0.0   8396   592 pts/3    S+   14:43   0:00 unshare -f --pid --mount-proc sleeroot        5921  0.0  0.0   8392   528 pts/3    S+   14:43   0:00 sleep 1h  
    root        5928  0.0  0.4  12172  4552 pts/2    S    14:43   0:00 sudo -i  
    root        5930  0.0  0.3  10152  3996 pts/2    S    14:43   0:00 -bash  
    root        5939  0.0  0.3  11808  3472 pts/2    R+   14:43   0:00 ps aux  
    root@vagrant:~# nsenter --target 5921 --pid --mount  
    root@vagrant:/# ps aux  
    USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND  
    root           1  0.0  0.0   8392   528 pts/3    S+   14:43   0:00 sleep 1h  
    root           2  0.0  0.4  10152  4076 pts/2    S    14:47   0:00 -bash  
    root          11  0.0  0.3  11808  3232 pts/2    R+   14:47   0:00 ps aux  
7.  :(){ :|:& };: - "fork" или "вилочная бомба", ":()" определяет функцию, вызываемую ":" телом ":|:&", что означает «запустить: а также запустить: в фоновом режиме». ";" завершает определение функции и ":" вызывает заново функцию, которая бесконечно порождает новые версии самой себя, пока не будет достигнут предел по ресурсам.  
    f() {  
         f | f &  
        }  
        f  
    за 30 сек все стабилизировлось, dmesg написал:  
    cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-3.scope  
    cgroups (control groups) – механизм ядра, позволяющий ограничивать использование, вести учет и изолировать потребление системных ресурсов на уровне коллекций процессов, в общем специальная защита от зловредов или случайно упавшей на клавиатуру пачки с бумагой.  
    Все ресурсы поделены на группы/слайсы: группы ядра и отдельно подсистемы описанные в /sys/fs/cgroup/. 
    При необходимости можно менять ограничения и например выделять больше памяти или процессов тому или иному объекту в нужном слайсе через установку конкретного значения через systemctl:  
    примерно так: systemctl set-property [имя контейнера/объекта] "CPUShares=200" "CPUQuota=30%" "MemoryLimit=500M"  
    В нашем случае должно быть что-то подобное:  
    systemctl set-property user-1000.slice "CPUQuota=50%"  
