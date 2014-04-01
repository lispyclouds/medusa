#include <exec.h>

void Exec::run(QString code, QString fileName, bool cStop) {
    QFile out(fileName);
    QString command = "dart " + fileName;

    out.open(QIODevice::WriteOnly | QIODevice::Text);
    out.write(code.toStdString().c_str());
    out.close();

    if (cStop)
        return;

    system(command.toStdString().c_str());
    out.remove();
}