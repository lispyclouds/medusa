#include <exec.h>

void Exec::run(QString code, QString fileName, bool cStop) {
    QFile out(fileName);
    QString command = "dart " + fileName;

    out.open(QIODevice::WriteOnly | QIODevice::Text);
    out.write(code.toStdString().c_str());
    out.close();

    if (cStop)
        return;

    if (system(command.toStdString().c_str()) != 0)
        cerr << "[Medusa Error] Dart not found in PATH. Make sure its installed and is accesible via PATH" << endl;

    out.remove();
}
