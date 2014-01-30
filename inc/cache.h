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
char* hashFile(char* path);
int tryInsert(char* fileName, char* hash);
int changed(char* fileName, char* hash);
int cached(char* fileName);

#endif