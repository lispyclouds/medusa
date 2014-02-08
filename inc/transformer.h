#ifndef TRANSFORMER_H
#define TRANSFORMER_H

#include <globals.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sqlite3.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/ioctl.h>

#define _GNU_SOURCE

int transform();

#endif
