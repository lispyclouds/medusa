#ifndef CACHE_H
#define CACHE_H

#include <QDir>
#include <QtSql/QSqlDatabase>
#include <QtSql/QSqlRecord>
#include <QtSql/QSqlQuery>
#include <QVariant>
#include <sha256.h>

#define BUFFER_SIZE 512

class Cache {
public:
    Cache();
    ~Cache();
    bool isCached(QString path, QString &code);
private:
    QSqlDatabase db;
    inline QString hashFile(QString path);
    inline bool changed(QString path, QString hash, QString &code);
    inline bool tryInsert(QString path, QString hash);
};

#endif