#ifndef EXEC_H
#define EXEC_H

#include <QString>

using namespace std;

class Exec {
public:
    void run(QString code, QString fileName, bool cStop);
};

#endif
