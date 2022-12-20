# informatics-msk-template

Шаблон проекта и вспомогательные скрипты для решения задач по С++ на сайте informatics.msk.ru

## Использование:

В папку tests добавить файлы с названиями:

``tests\<xxxx\>.txt `` - входные данные

``tests\<xxxx\>.txt.expected`` - ожидаемые выходные данные

##### Запуск всех тестов:
``./test``
Будет выведен сводный результат по всем тестам.

>     >./test
>     ./tests/test1.txt RESULT:       TRUE
>     ./tests/test2.txt RESULT:       FALSE
>     
>     TOTAL FAILS: 1

##### Запуск теста \<xxxx\>:
``./test xxxx``
Весь вывод, включая отладочный, будет выведен в файл out.txt и на экран.
>     >./test 2
>     see full output in out.txt
>     --- START ---
>     DEBUG PRINT
>     1 2 3 4 5
>     DEBUG PRINT
>     
>     ---- END ----



Репозиторий пересоздан 20.12.2022
