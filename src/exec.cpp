#include <exec.h>
#include <QFile>
#include <iostream>

void Exec::run(QString code, QString fileName, bool cStop) {
    QFile out(fileName);
    QString command = "dart " + fileName;

    out.open(QIODevice::WriteOnly | QIODevice::Text);
    out.write(code.toStdString().c_str());
    out.close();

    if (cStop)
        return;

    if (system(command.toStdString().c_str()) == 32512)
        cerr << "\x1b[31m[Medusa Error] Dart not found in PATH. Make sure its installed and is accesible via PATH\x1b[0m" << endl;

    out.remove();
}
