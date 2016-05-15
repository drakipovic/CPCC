#include <cstdio>
#include <iostream>
#include <string>

using namespace std;

string pancakes;

int main(){
    int t;
    scanf("%d", &t);
    for(int c = 1; c <= t; ++c){
        cin >> pancakes;
        int ret = 0;
        for(int i = pancakes.size()-1; i >= 0; --i){
            while(pancakes[i] == '+' && i >= 0) --i;
            if(i < 0) break;
            for(int j = i; j >= 0; --j){
                if(pancakes[j] == '-') pancakes[j] = '+';
                else pancakes[j] = '-';
            }
            ++ret;
        }

        printf("Case #%d: %d\n", c, ret);
    }

    return 0;
}
