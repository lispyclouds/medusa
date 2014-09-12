#include <cache.h>

Cache::Cache() {
    QString medusaHome = QDir::homePath() + "/.medusa/";

    if (!QFile(medusaHome).exists()) {
        cerr << "[Medusa Error] What?! Medusa Home folder not found or unreadable. Please Reinstall." << endl;
        exit(-1);
    }

    db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName(medusaHome + "medusa.cache");

    if (!QFile(medusaHome + "medusa.cache").exists()) {
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
    FILE *inFile;
    char buffer[BUFFER_SIZE], output[2 * SHA256_DIGEST_SIZE + 1];
    unsigned char digest[SHA256_DIGEST_SIZE];
    int bytes;

    if (!(inFile = fopen(path.toStdString().c_str(), "rb"))) {
        cerr << "Error: Couldn't read "
            << path.toStdString().c_str()
            << ". Please check if it exists and is readable."
            << endl;
        exit(-1);
    }

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
