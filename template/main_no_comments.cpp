#include <iostream>
#include <sstream>
#include <vector>
#include <queue>
#include <set>
#include <list>
#include <algorithm>

using namespace std;

int main(int argc, char *argv[])
{
    int debug_print = 0;



    if (argc > 1)
        debug_print = 1;

    if (debug_print)
        cout << "DEBUG PRINT" << endl;

    cout << "1 2 3 4 5";

    cout << endl;

    if (debug_print)
        cout << "DEBUG PRINT" << endl;

    return 0;
}
