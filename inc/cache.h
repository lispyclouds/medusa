#ifndef CACHE_H
#define CACHE_H

#include <globals.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sqlite3.h>
#include <openssl/sha.h>

void makeDiffIndex();
char* hashFile();
int tryInsert(char* hash);
int changed(char* hash);
int cached();

#endif