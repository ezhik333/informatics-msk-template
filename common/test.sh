#!/bin/bash

mkdir -p backups
date=$(date '+%Y-%m-%d_%H-%M-%S')
cp main.cpp "./backups/main$date.cpp"
awk '$0 !~ /\/\// {print}' main.cpp > main_no_comments.cpp
g++ main_no_comments.cpp -o main_no_comments.out
chmod +x main_no_comments.out
res=$?

if [[ $res != 0 ]]; then
    exit
fi


RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

fails=0
totalfails=0

if [[ $1 == "" ]]; then
    for test in ./tests/*.txt; do
        expected="$test.expected"
        echo -n "$test RESULT:"
        mapfile -t result < <(cat "$test" | ./main_no_comments.out)

        if [ -f "$expected" ]; then
            mapfile -t check < <(cat "$expected")

            fails=0

            for i in "${!check[@]}"; do
                if [[ ${check[i]} != "${result[i]}" ]]; then
                    fails=1
                fi
            done

            for i in "${!result[@]}"; do
                if [[ ${check[i]} != "${result[i]}" ]]; then
                    fails=1
                fi
            done


            if [[ $fails == 0 ]]; then
                    echo -e "${GREEN}\tTRUE${NC}"
            else
                    echo -e "${RED}\tFALSE${NC}"
            fi

            if [[ $fails != 0 ]]; then
                totalfails=${totalfails+1}
            fi
        else
            echo -e "${BLUE}\tUNKNOWN${NC}"
        fi
    done

    echo ""
    if [[ $totalfails == 0 ]]; then
        echo -e "${GREEN}TESTS PASSED${NC}"
    else
        echo -e "${RED}TOTAL FAILS: ${totalfails}${NC}"
    fi
    

else
    mytest="./tests/test$1.txt"
    cat "$mytest" | ./main_no_comments.out debug > out.txt
    echo "see full output in out.txt"
    
    echo "--- START ---"
    cat ./out.txt
    echo ""
    echo "---- END ----"
fi