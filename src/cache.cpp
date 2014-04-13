#include <cache.h>

Cache::Cache() {
    QString medusaHome = QDir::homePath() + "/.medusa/";

    db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName(medusaHome + "medusa.cache");

    QFile dbFile(medusaHome + "medusa.cache");
    if (!dbFile.exists()) {
        db.open();
        QSqlQuery query(db);
        query.exec("CREATE TABLE MedusaCache (InFile TEXT PRIMARY KEY, Hash VARCHAR(64), GenCode TEXT)");
    }
    else
        db.open();
}

Cache::~Cache() {
    db.close();
}

QString Cache::hashFile(QString path) {
    sha256_ctx ctx;
    FILE *inFile = fopen(path.toStdString().c_str(), "rb");
    char buffer[BUFFER_SIZE], output[2 * SHA256_DIGEST_SIZE + 1];
    unsigned char digest[SHA256_DIGEST_SIZE];
    int bytes;

    sha256_init(&ctx);
    while ((bytes = fread(buffer, 1, BUFFER_SIZE, inFile)) != 0)
        sha256_update(&ctx, (const unsigned char *) buffer, bytes);
    sha256_final(&ctx, digest);

    fclose(inFile);
    output[2 * SHA256_DIGEST_SIZE] = 0;

    for (int i = 0; i < SHA256_DIGEST_SIZE ; i++)
        sprintf(output + 2 * i, "%02X", digest[i]);

    return QString(output);
}

bool Cache::tryInsert(QString path, QString hash) {
    QSqlQuery query(db);
    return query.exec("INSERT INTO MedusaCache VALUES ('" + path + "', '" + hash + "', '')");
}

bool Cache::changed(QString path, QString hash, QString &code) {
    QSqlQuery query(db);

    query.exec("SELECT Hash, GenCode FROM MedusaCache WHERE InFile='" + path + "'");
    QSqlRecord rec = query.record();
    query.next();

    if (query.value(0).toString() != hash)
        return query.exec("UPDATE MedusaCache SET Hash='" + hash + "' WHERE InFile='" + path + "'");

    code = query.value(1).toString();
    return false;
}

bool Cache::isCached(QString path, QString &code) {
    QString hash = hashFile(path);

    if (!tryInsert(path, hash))
        return changed(path, hash, code) ? false : true;
    else
        return false;
}