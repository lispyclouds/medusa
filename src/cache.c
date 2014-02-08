#include <cache.h>

sqlite3 *handle;
char hexString[128];

void makeDiffIndex() {
    char query[125] = "CREATE TABLE DiffIndex(InFile VARCHAR(256) PRIMARY KEY, ContentHash VARCHAR(128), OutFile VARCHAR(256))";

    sqlite3_open("DiffIndex", &handle);
    sqlite3_exec(handle, query, 0, 0, 0);
}

char* hashFile() {
    int i, bytes;
    FILE *inFile = fopen(buffer, "rb");
    SHA512_CTX context;
    unsigned char digest[SHA512_DIGEST_LENGTH + 1], buffer[BUFSIZ];
    char *bufPtr;

    SHA512_Init(&context);
    while ((bytes = fread (buffer, 1, BUFSIZ, inFile)) != 0)
        SHA512_Update(&context, buffer, bytes);
    SHA512_Final(digest, &context);

    bufPtr = hexString;
    for (i = 0; i < SHA512_DIGEST_LENGTH; i++)
        bufPtr += sprintf(bufPtr, "%02X", digest[i]);
    *(bufPtr + 1) = 0;

    fclose (inFile);
    return hexString;
}

int tryInsert(char* hash) {
    char *query = (char *) malloc(strlen(buffer) + strlen(hash) + 41);
    int ret;

    sprintf(query, "INSERT INTO DiffIndex VALUES('%s', '%s', '')", buffer, hash);
    ret = sqlite3_exec(handle, query, 0, 0, 0);

    free(query);
    return ret;
}

int changed(char* hash) {
    char *query = (char *) malloc(strlen(buffer) + 50);
    sqlite3_stmt *stmt;

    sprintf(query, "SELECT ContentHash FROM DiffIndex WHERE InFile='%s'", buffer);
    sqlite3_prepare_v2(handle, query, -1, &stmt, 0);

    sqlite3_step(stmt);
    char *value = (char*) sqlite3_column_text(stmt, 0);
    free(query);

    if (strcmp(value, hash) != 0) {
        query = (char *) malloc(strlen(buffer) + strlen(hash) + 52);
        sprintf(query, "UPDATE DiffIndex SET ContentHash='%s' WHERE InFile='%s'", hash, buffer);
        sqlite3_exec(handle, query, 0, 0, 0);

        free(query);
        return 1;
    }

    return 0;
}

int cached() {
    char *hash;

    if (access("DiffIndex", 0) == -1)
        makeDiffIndex();
    else
        sqlite3_open("DiffIndex", &handle);

    hash = hashFile();

    if (tryInsert(hash)) {
        if (changed(hash))
            return 0;
        else
            return 1;

        sqlite3_close(handle);
    }
    else
        return 0;

    sqlite3_close(handle);
}