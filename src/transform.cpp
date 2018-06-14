#include <iostream>
#include <transform_moc.h>
#include <QDir>
#include <QVariant>
#include <QtSql/QSqlQuery>

using namespace std;

Transform::Transform() {
    reply = "";
    db.setDatabaseName(QDir::homePath() + "/.medusa/medusa.cache");
    db.open();
    python = new QProcess(this);
}

Transform::~Transform() {
    delete python;
    db.close();
}

void Transform::readStandardOutput() {
    reply += python->readAllStandardOutput();
}

void Transform::readStandardError() {
    reply += python->readAllStandardError();
}

void Transform::pythonFinished(int exitCode, QProcess::ExitStatus) {
    this->exitCode = exitCode;
    QSqlQuery query(db);

    if (exitCode == 0) {
        query.prepare("UPDATE MedusaCache SET GenCode=? WHERE InFile=?");
        query.addBindValue(reply);
        query.addBindValue(path);
        query.exec();
    } else {
        query.exec("DELETE FROM MedusaCache WHERE InFile='" + path + "'");
        cerr << "\x1b[31m" + reply.toStdString() + "\x1b[0m" << endl;
    }
}

void Transform::shitHappened(QProcess::ProcessError error) {
    if (error == QProcess::FailedToStart) {
        QSqlQuery query(db);
        query.exec("DELETE FROM MedusaCache WHERE InFile='" + path + "'");
        cerr << "\x1b[31m[Medusa Error] Python not found in PATH. Make sure its installed and is accesible via PATH\x1b[0m" << endl;
        exitCode = -1;
    }
}

bool Transform::transform(QString path, QString &code) {
    QStringList args;

    if (!QFile(QDir::homePath() + "/.medusa/transform.py").exists()) {
        QSqlQuery query(db);
        query.exec("DELETE FROM MedusaCache WHERE InFile='" + path + "'");
        cerr << "\x1b[31m[Medusa Error] What?! FPT Transformer not found. Please Reinstall.\x1b[0m" << endl;
        exit(-1);
    }

    args << QDir::homePath() + "/.medusa/transform.py" << path;
    this->path = path;

    connect(python, SIGNAL(finished(int, QProcess::ExitStatus)), this, SLOT(pythonFinished(int, QProcess::ExitStatus)));
    connect(python, SIGNAL(readyReadStandardError()), this, SLOT(readStandardError()));
    connect(python, SIGNAL(readyReadStandardOutput()), this, SLOT(readStandardOutput()));
    connect(python, SIGNAL(error(QProcess::ProcessError)), this, SLOT(shitHappened(QProcess::ProcessError)));

    python->start("python2.7", args);
    python->waitForFinished();
    code = reply;

    return exitCode ? false : true;
}
