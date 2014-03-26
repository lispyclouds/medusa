#include <exec.h>

void Exec::run(QString code, QString fileName) {
    QFile out(fileName);
    out.open(QIODevice::WriteOnly | QIODevice::Text);
    out.write(code.toStdString().c_str());
    out.close();

    QString command = "dart " + fileName;
    system(command.toStdString().c_str());
}