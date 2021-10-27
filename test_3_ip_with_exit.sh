#!/usr/bin/env bash
declare -i try_count=0

# фмнальную недоступность узла фиксируем только если все 5 попыток проверки узла не успешны

array_str=("10.0.2.15" "192.168.200.189" "169.254.1.1")
#echo ${array_str[@]}
while ((1==1)) # бесконечны цикл
    do
	for ip in ${array_str[@]} 
	    do
		echo " "
		echo "начинаем тестировать узел: "$ip
		sleep 1
		testUrl="https://"$ip":443"
		for ((i=1; i < 6; i++))
		    do
        		echo "попытка номер: "$i 
			curl --connect-timeout 2 --insecure -I $testUrl 
		            if (($? != 0))
				then
				    echo "попытка номер: "$i" не успешна"
				else
				    try_count=$((try_count+1))
			    fi 
		    done
	        if ((try_count > 0))
			then
			    echo "Для "$testUrl" количество успешных попыток "$try_count", что > 0 - считам что все ок"
			    sleep 1
			    try_count=0 #обнулим количество успешных попыток 
			else
		    echo "ошибка на сервере "$testUrl", наблюдение остановлено" >> error.log
		    exit 1
		fi 
		
	    done	
    done




