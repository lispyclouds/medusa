#ifndef CACHE_H
#define CACHE_H

#include<QString>
#include <QtSql/QSqlDatabase>

using namespace std;

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
