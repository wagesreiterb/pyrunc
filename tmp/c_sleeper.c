#include <stdio.h>
#include <unistd.h>

// compiler flags for linking statically
// https://www.systutorials.com/5217/how-to-statically-link-c-and-c-programs-on-linux-with-gcc/
// gcc -static -static-libstdc++ -static-libgcc

int main() {
    int sleep_time = 60;

    printf("start sleeping...\n");
    for(int i = 0; i < sleep_time; i++) {
        sleep(1);
        printf(".");
        fflush(stdout);
    }
    printf("\n...sleeping finished\n");
}