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
    bool cStop = false;
    QString path, name, code, medusa = QByteArray::fromBase64(art);

    if (app.arguments().size() == 1) {
        cout << help << medusa.toStdString();
        return 0;
    }

    foreach (QString arg, app.arguments()) {
        if (arg == "--help" || arg == "-h") {
            cout << help << medusa.toStdString();
            return 0;
        }
        else if (arg == "-c")
            cStop = true;
        else if (arg == "-install") {
            if (QFile::copy(path, "lib/" + name + ".py"))
                cout << QString(name + ".py").toStdString() + " successfully Installed into Medusa!" << endl;
            else
                cerr << "Couldn't Install: " + QString(name + ".py").toStdString() << endl;
            return 0;
        }
        else {
            QFileInfo pyFile(arg);
            path = pyFile.absoluteFilePath();
            name = pyFile.completeBaseName();
        }
    }

    if (cache.isCached(path, code) || transformer.transform(path, code))
        exec.run(code, name + ".dart", cStop);

    return 0;
}