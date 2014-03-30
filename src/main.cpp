#include <QFileInfo>
#include <QtCore/QCoreApplication>
#include <iostream>
#include <cache.h>
#include <transform.h>
#include <exec.h>

using namespace std;

string helpText = "\nMedusa 2.7.3 beta\nCopyright (c) 2013-2104, Rahul De, Apoorv Agarwal and Aakash Giri, VIT University\n\
Licensed under BSD 3-Clause\n\nUsage: medusa [options] file\n\nOptions:\n\
--help\tDispaly this information\n-c\tCompile to Dart only\n";

int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    Cache cache;
    Transform transformer;
    Exec exec;
    QStringList args = app.arguments();
    bool cStop = false;
    QString path, name, code, art;
    QFile artFile("art.txt");

    if (app.arguments().size() == 1) {
        artFile.open(QIODevice::ReadOnly | QIODevice::Text);
        art = artFile.readAll();
        artFile.close();

        cout << helpText << art.toStdString();
        return 0;
    }

    foreach (QString arg, app.arguments()) {
        if (arg == "--help") {
            artFile.open(QIODevice::ReadOnly | QIODevice::Text);
            art = artFile.readAll();
            artFile.close();

            cout << helpText << art.toStdString();
            return 0;
        } else if (arg == "-c")
            cStop = true;
        else {
            QFileInfo pyFile(arg);
            path = pyFile.absoluteFilePath();
            name = pyFile.completeBaseName() + ".dart";
        }
    }

    if (cache.isCached(path, code) || transformer.transform(path, code))
        exec.run(code, name, cStop);

    return 0;
}