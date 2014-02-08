#include <globals.h>
#include <stdio.h>
#include <cache.h>
#include <transformer.h>
#include <exec.h>

char *buffer, *home;

int main(int argc, char** argv) {

    if (argc != 2) {
        printf("Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    home = getenv("HOME");
    buffer = realpath(argv[1], NULL);

    if (cached()) {
        printf("Cached, Skipping Compilation... :D\n");
    } else {
        if (transform()) {
            fprintf(stderr, "Parse Failed... :(\n");
            fprintf(stderr, buffer);
        } else {
            if (exec()) {
                fprintf(stderr, "Dart Error:\n");
                fprintf(stderr, buffer);
            }
        }
    }

    free(absPath);
    free(buffer);

    return 0;
}