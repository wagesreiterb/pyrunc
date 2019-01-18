#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

// FILE *freopen(const char *restrict filename, const char *restrict mode,
//       FILE *restrict stream);


int main() {
    printf("Hello World!\n");
    freopen("/dev/pts/4","w",stdout);
    printf("World of Warcraft!\n");

    char* tty;
    tty = ttyname(0);
    printf("tty name is %s\n", tty);
}
