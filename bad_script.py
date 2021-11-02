#!/usr/bin/env python3
import sys
import os

local_changed_files = ''
untracked_files = ''
full_path_to_git = ''

if len(sys.argv) > 1: # реализуем обработку параметров, если параметры точно были - то читаем их
    full_path_to_git = sys.argv[1]
    if (full_path_to_git [len(full_path_to_git)-1]) != '/': # добавили обработку символа '/' в конце строки чтоб все было однообразно (если вдруг ее не ввели)
        full_path_to_git = full_path_to_git + '/'
    print (f'Путь пришел из параметра: {full_path_to_git}')
else:                 # если нет, то считаем что работаем в локальной директории    
    full_path_to_git = os.getcwd() + '/'
    print (f'Путь взяли локальный: {full_path_to_git}')

if not os.access((full_path_to_git + '.git/config'), os.F_OK):  # делаем простейшую проверку на предмет является ли искомая директория гитовой
    print ('Скорее всего это не гит директория')
    exit () 

print (f'Изменения в гите ищем здесь: {full_path_to_git}')
print ('')

bash_command = ['cd ' + full_path_to_git, 'git status -s']  # упроситили вывод гита для более простой обработки
result_os = os.popen(' && '.join(bash_command)).read()


for result in result_os.split('\n'):

    if result.find(' M') != -1:
        prepare_result = result.replace (' M','')
        local_changed_files = local_changed_files + full_path_to_git + '/' + prepare_result + '\n'
        local_changed_files = local_changed_files.replace ('/ ','')
    if result.find('??') != -1:
        prepare_result = result.replace ('??','')
        untracked_files = untracked_files + full_path_to_git + '/' + prepare_result + '\n'
        untracked_files = untracked_files.replace ('/ ', '')


print ('Локально измененные файлы:')
print (local_changed_files)

print ('Новые или неотслеживаемые файлы:')
print (untracked_files)
