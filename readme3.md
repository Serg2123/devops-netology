#devops-netology
с исправлениями  


1. chdir (в самом конце лога strace)  
    fork - создание нового дочернего процесса;  
    read - попытка читать из файлового дескриптора;  
    write - попытка записи в файловый дескриптор;  
    open - открыть файл для чтения или записи;  
    close - закрыть файл после чтения или записи;  
    chdir - изменить текущую директорию;  
    execve - выполнить исполняемый файл;  
    stat - получить информацию о файле;  
    mknod - создать специальный файл, например, файл устройства или сокет.  
  
2. strac-ом соберем данные по тому какие открываются файлы, перенаправив вывод в файлы отчетов,  
   например, так: strace file /dev/sda 2>sda-rep.txt  
   далее через сравнение файлов посмотрим сходства и отличия:  
   diff -y tty-rep.txt sda-rep.txt | more
   В работе утилиты file в основном открываютя либы, но либы не редко бывают "справочниками"  
   В конце работы strace file идет несколько попыток открыть magic или magic.mgc, после чего magic.mgc успешно открывается  
   читаем ман по magic и узнаем что это база данных "магических чисел" для определения типов файлов  
   magic.mgc открывается по пути /usr/share/misc/magic.mgc, но тут ссылка на /usr/lib/file/magic.mgc  
  
3. Сначала глазами найдем предполагаемый удаленный файл, который ест место  
    sudo lsof | grep deleted  
   далее найдем (отфильтровав по искомому файлу) pid процесса, дескриптор и полный путь файла  
    sudo lsof | grep deleted | grep искомый_файл   
   далее убьем процесс по его пиду и файл должен сам "освободиться" и место высвободить.  
   Если вдруг место не высвободилось или процесс нельзя убивать, то тогда удаленный файл можно усеч до 0.  
   Полный путь к дескриптору можно либо составить самому ("/proc/<pid>/fd/указатель_из_lsoft"), либо еще раз его найти через найденый pid:  
    "sudo ls -l /proc/<pid>/fd"  /# ищем строку с (deleted), нужный указатель на файл после fd  
   далее усекаем файл по полному пути файла указателя  
    "cat /dev/null > /proc/<pid>/fd/указатель_на_файл"  
  
4. сами зомби процессы ресурсы уже не потребляют, они их уже высвободили т.к. процесс завершился, а его родитель нет или потерялся. Не большое кол-во зомби не так страшно, большое кол-во зомби начинает поедать записи в таблице процессов   
  
5. opensnoop показывает какие процессы какие файлы открывают, сначала показываютя файлы процесса vminfo, потом dbus-daemon (шина DBus). Знакомая утилита, мы так работу DBus трейсили что бы через DBus повесить доп.обработчик на событие вставки смарт-карты в карт-ридер, что бы в дальнейшем пользователь вводил только пароль (как в Windows), а не логин + пароль как по умолчанию подразумевается в Linux   
  
6. Вызывается одноименный системный вызов uname  
    Из man 2 uname:  
       Part of the utsname information is also accessible via /proc/sys/kernel/{ostype,  hostname,  
       osrelease, version, domainname}. 
   Соотвтественно часть информации можно найти в путем вызова:  
   cat /proc/sys/kernel/osrelease  
   cat /proc/sys/kernel/version  
   
7. ; - это разделитель последовательного выполнения команд, && - логическое И, т.е. вторая команда выполнится только при успешном выполнении первой.  
   Использование "set -e" все же ориентировано скорее на использование внутри скрипта, а не в составе выражения в одной строке, и при "set -e" происходит полная принудительная остановка сценария c любым кодом выхода не равным 0.  
   В одной строке && и "set -e" скорее всего нет смысла использовать.  

8. set -euxo pipifail
    -e  Exit immediately if a command exits with a non-zero status.
    -u  Treat unset variables as an error when substituting.
    -x  Print commands and their arguments as they are executed.
    -o option-name
    	pipefail     the return value of a pipeline is the status of
                     the last command to exit with a non-zero status,
                     or zero if no command exited with a non-zero status
Дает расширенную построчную отладочную информацию о работе скрипта.
9. Наиболее частые процессы Ss и R+, основные значения S (прерывистый сон,ожидание завершения события) и R (работает или запускается). 
   + и s это расширяющие допзначения: + (находится в группе процессов переднего плана), s (является лидером сеанса).
    







