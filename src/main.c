#include <globals.h>
#include <stdio.h>
#include <cache.h>

char* buffer;

int main(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    if (cached(argv[1])) {
        printf("Cached, Skipping Compilation... :D\n");
    } else {
    }

    free(buffer);
    return 0;
}