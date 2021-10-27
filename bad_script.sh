#!/usr/bin/env bash
rm curl.log
declare -i error_code=0
declare -i down_time=0
declare -i crash_time=0
declare -i current_time=0
declare -i last_current_time=0
declare -i uniq_crash_code=0

while ((1==1))
    do
	curl --insecure -I https://localhost:443
	    if (($? != 0))
		then
		    if [ $error_code -eq 0 ] # т.е. до этого момента все работало
			then
			    echo " " >> curl.log
			    echo "Время падения:" >> curl.log
			    date >> curl.log
			    crash_time=$(date +%s)
			    error_code=1
			    uniq_crash_code=$RANDOM  # это нам нужно что бы при замене в cult.log строчки с временим зависания заменять нужную строчку текущего падения сервиса

			    #и тут же запишем первый раз нулевое значение которое потом будем переписывать
			    current_time=$(date +%s)
			    let " down_time = ( current_time - crash_time ) / 60 " #перевели в минуты
			    string_to_out="Висим: "$down_time" минут (уникальный код падения "$uniq_crash_code")"
			    echo $string_to_out >> curl.log
			    string_to_replace=$string_to_out
			else
			    current_time=$(date +%s)
			    let " down_time = ( current_time - crash_time ) / 60 " #перевели в минуты
			    string_to_out="Висим: "$down_time" минут (уникальный код падения "$uniq_crash_code")"
			    sed -i "s/$string_to_replace/$string_to_out/g" curl.log # обновили в curl.log время которое мы висим, файл лога не растет
			    string_to_replace=$string_to_out
		    fi
		else
		    if [ $error_code -eq 1 ]
			then 
			    echo " " >> curl.log
			    echo "Время восстановления:" >> curl.log
			    date >> curl.log
			    error_code=0 #сбросим код события об ошибке
			    uniq_crash_code=0 #сбросим уникальный код падения по которому мы ищем время в curl.log
			else
			    echo "Всё ок! можно спать"
		    fi
	    fi
    done