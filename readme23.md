1.Более менее все понятно. Образ создался без проблем.  
[образ centos](https://github.com/Serg2123/devops-netology/blob/main/pics/centos-image.png)    

2.Теоретически тоже все было понятно, только никто нигде не упомянул ;) что нужно заранее создать сервисную учетную запись, выдать ей роли и потом сгенерировать для нее ключи.  
[terraform](https://github.com/Serg2123/devops-netology/blob/main/pics/terraform.png)  

3.Тут тоже все понятно было как настраивать, но почему-то начали сыпаться ошибки при выполнении плейбука, а точнее при установке разных пакетов, пришлось чуть скорректировать плейбук.  
[grafana](https://github.com/Serg2123/devops-netology/blob/main/pics/grafana.png)  
В плейбуке чуть упрошены конструкци установки пакетов,  было:  
```
      - name: Installing tools  
        yum: >  
          package={{ item }}  
          state=present  
          update_cache=yes  
        with_items:  
          - git  
          - curl  

```
стало:  
```
      - name: Installing tools  
        package:  
          name:  
          - git  
          - curl  

```
[скорректированный плейбук](https://github.com/Serg2123/devops-netology/blob/main/pics/provision.yml)  
