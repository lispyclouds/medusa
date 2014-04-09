#include <QFileInfo>
#include <QtCore/QCoreApplication>
#include <iostream>
#include <cache.h>
#include <transform.h>
#include <exec.h>

using namespace std;

string helpText = "\nMessers Heisenberg, AppuDB and Giri, The Purveyors of Speed\n\n<< PRESENTS >>\n\n\
Medusa 2.7.3 beta\nCopyright (c) 2013-2014, Rahul De, Apoorv Agarwal and Aakash Giri, VIT University\n\
Licensed under BSD 3-Clause\n\nUsage: medusa [options] file\n\nOptions:\n\
-install\tInstall External Python module\n--help, -h\tDispaly this information\n-c\t\tCompile to Dart only\n";

int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    Cache cache;
    Transform transformer;
    Exec exec;
    QStringList args = app.arguments();
    bool cStop = false, install = false;
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
        if (arg == "--help" || arg == "-h") {
            artFile.open(QIODevice::ReadOnly | QIODevice::Text);
            art = artFile.readAll();
            artFile.close();

            cout << helpText << art.toStdString();
            return 0;
        }
        else if (arg == "-c")
            cStop = true;
        else if (arg == "-install")
            install = true;
        else {
            QFileInfo pyFile(arg);
            path = pyFile.absoluteFilePath();
            name = pyFile.completeBaseName();
        }
    }

    if (install) {
        if (QFile::copy(path, "lib/" + name + ".py"))
            cout << QString(name + ".py").toStdString() + " successfully Installed into Medusa!" << endl;
        else
            cerr << "Couldn't Install!" + QString(name + ".py").toStdString() << endl;
        return 0;
    }

    if (cache.isCached(path, code) || transformer.transform(path, code))
        exec.run(code, name + ".dart", cStop);

    return 0;
}