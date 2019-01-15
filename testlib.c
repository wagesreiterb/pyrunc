#include <stdio.h>
#include <unistd.h>


void void_and_void() {
   printf("void_and_void\n");
}

int int_and_void() {
    printf("int_and_void\n");

    return 3;
}

int void_and_int(int arg) {
    printf("void_and_int: %d\n", arg);
}

int void_and_char_pointer(char* arg) {
    printf("void_and_char_pointer: %s\n", arg);
}

void void_and_void_pointer(void* arg) {
    printf("void_and_void_pointer: %p\n", arg);
    printf("after type cast: %s\n", (char*)arg);
}

void sleeper(int sleeptime) {
    printf("sleep 5 Seconds\n");
    for(int i=0; i < sleeptime; i++) {
        printf("%d\n", i);
        sleep(1);
    }
}

