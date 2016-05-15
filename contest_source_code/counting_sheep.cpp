#include <cstdio>

bool seen_all(int a[]){
    for(int i = 0; i < 10; ++i){
        if(!a[i]) return false;
    }

    return true;
}

int main(){
    int n, t;
    scanf("%d", &t);
    int c = 1;
    while(t--){
        int digits[10];
        for(int i = 0; i < 10; ++i) digits[i] = 0;
        scanf("%d", &n);
        if(n == 0){
            printf("Case #%d: INSOMNIA\n", c);
            ++c;
            continue;
        }
        int N = n;
        for(int i = 2; ; ++i){
            int tmp = n;
            while(tmp > 0){
                digits[tmp%10] = 1;
                tmp /= 10;
            }
            if(seen_all(digits)) {
                printf("Case #%d: %d\n", c, n);
                break;
            }
            n = N * i;
        }
        
        ++c;
    }



    return 0;
}
