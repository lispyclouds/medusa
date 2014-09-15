#include <QFileInfo>
#include <QByteArray>
#include <QtCore/QCoreApplication>
#include <iostream>
#include <cache.h>
#include <transform.h>
#include <exec.h>
#include <static_data.h>

using namespace std;

int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    Cache cache;
    Transform transformer;
    Exec exec;
    QStringList args = app.arguments();
    bool cStop = false, install = false;
    QString path, name, code;

    if (app.arguments().size() == 1) {
        cout << help << QString(QByteArray::fromBase64(art)).toStdString();
        return 0;
    }

    foreach (QString arg, args) {
        if (arg == "--help" || arg == "-h") {
            cout << help << QString(QByteArray::fromBase64(art)).toStdString();
            return 0;
        }
        else if (arg == "moo") {
            cout << QString(QByteArray::fromBase64(mooData)).toStdString() << endl;
            return 0;
        }
        else if (arg == "-c")
            cStop = true;
        else if (arg == "-install")
            install = true;
        else if (arg == "--version" || arg == "-v") {
            cout << version << " running on Qt " << qVersion() << endl;
            return 0;
        }
        else {
            QFileInfo pyFile(arg);
            path = pyFile.absoluteFilePath();
            name = pyFile.completeBaseName();
        }
    }

    if (install) {
        if (QFile::copy(path, QDir::homePath() + "/.medusa/lib/" + name + ".py"))
            cout << QString(name + ".py").toStdString() + " successfully Installed into Medusa!" << endl;
        else
            cerr << "\x1b[31mCouldn't Install: " + QString(name + ".py").toStdString() + "\x1b[0m" << endl;
        return 0;
    }

    if (cache.isCached(path, code) || transformer.transform(path, code))
        exec.run(code, name + ".dart", cStop);

    return 0;
}
