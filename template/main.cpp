#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
    int debug_print = 0;

    // cout << "argc:" << argc << endl;

    // for (int i = 0; i < argc; i++)
    // {
    //     cout << "argv[" << i << "]" << argv[i] << endl;
    // }

    // если запускаем с доп. ключом, то включаем отладочный вывод
    if (argc > 1)
        debug_print = 1;

    // отладочный вывод (должен быть отключен)
    if (debug_print)
        cout << "DEBUG PRINT" << endl;

    // вывод результата
    cout << "1 2 3 4 5";

    // рекомендуется после вывода результата в конце добавлять конец строки, если его нет
    cout << endl;

    // отладочный вывод (должен быть отключен)
    if (debug_print)
        cout << "DEBUG PRINT" << endl;

    return 0;
}
