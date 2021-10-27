#!/usr/bin/env bash
rm curl_*.log

array_str=("10.0.2.15" "192.168.200.189" "169.254.1.1")
echo ${array_str[@]}
for ip in ${array_str[@]} 
    do
	echo "начинаем тестировать узел: "$ip
	testUrl="https://"$ip":443"
	echo $testUrl

	for ((i=1; i < 6; i++))
	    do
		echo "попытка: "$i
    		curl --connect-timeout 2 --insecure -I $testUrl >> curl_$ip.log
	    done
    done

