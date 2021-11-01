#!/usr/bin/env python3
import sys
import os

local_changed_files = ''
untracked_files = ''
full_path_to_git = ''

if len(sys.argv) > 1: # реализуем обработку параметров, если параметры точно были - то читаем их
    full_path_to_git = sys.argv[1]
    #print (full_path_to_git)
else:                 # если нет, то считаем что работаем в локальной директории    
    full_path_to_git = os.getcwd()
    print (full_path_to_git)

if not os.access((full_path_to_git + '/.git/config'), os.F_OK):  # делаем простейшую проверку на предмет является ли искомая директория гитовой
    print ('Скорее всего это не гит директория')
    exit () 

print (f'Изменения в гите ищем здесь: {full_path_to_git}')
print ('')

bash_command = ['cd ' + full_path_to_git, 'git status -s']  # упроситили вывод гита для более простой обработки
result_os = os.popen(' && '.join(bash_command)).read()


for result in result_os.split('\n'):

    if result.find(' M') != -1:
        prepare_result = result.replace (' M','')
        local_changed_files = local_changed_files + prepare_result + '\n'
    if result.find('??') != -1:
        prepare_result = result.replace ('??','')
        untracked_files = untracked_files + prepare_result + '\n'


print ('Локально измененные файлы:')
print (local_changed_files)

print ('Новые или неотслеживаемые файлы:')
print (untracked_files)
