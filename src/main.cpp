#include <QFileInfo>
#include <QtCore/QCoreApplication>
#include <cache.h>
#include <transform.h>
#include <exec.h>

int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    Cache cache;
    Transform transformer;
    Exec exec;

    QFileInfo pyFile(app.arguments().at(1));
    QString path = pyFile.absoluteFilePath(), name = pyFile.completeBaseName() + ".dart", code;

    if (cache.isCached(path, code) || transformer.transform(path, code))
        exec.run(code, name);

    return 0;
}