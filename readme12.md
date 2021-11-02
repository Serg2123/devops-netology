1. починенный json формат:  
```
{ "info" : "Sample JSON output from our service\\t",
    "elements" : [
        { "name" : "first",
        "type" : "server",
        "ip" : "7175" 
        },
        { "name" : "second",
        "type" : "proxy",
        "ip" : "71.78.22.43"
        }
    ]
}
```
  
2. Cкрипт который проверяет IP трех сайтов из ДЗ и сверяет их с результатами самой первой проверки,  
скрипт останавливается при первом несовадении результатов проверки с первой проверкой.  
Стандартный вывод "ошибки" через stdout.  
Результаты первичной проверки, результаты работы скрипта записываются/перезаписывабтся в файлы:   
[json](https://github.com/Serg2123/devops-netology/blob/main/host_for_tests.json)
[yaml](https://github.com/Serg2123/devops-netology/blob/main/host_for_tests.yaml)
[питон скрипт](https://github.com/Serg2123/devops-netology/blob/main/test_json.py)  
 