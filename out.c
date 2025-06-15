#include <stdio.h>

int main() {
    int x = 2;
    switch (x) {
    case 1:
    printf("%d\n", 100);
        break;
    case 2:
    printf("%d\n", 200);
        break;
    case 3:
    printf("%d\n", 300);
        break;
    default:
    printf("%d\n", 999);
    }
    return 0;
}