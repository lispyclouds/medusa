QT          += core sql
QT          -= gui

TARGET       = medusa

CONFIG      += console
CONFIG      -= app_bundle

TEMPLATE     = app

INCLUDEPATH += inc

SOURCES     += src/main.cpp      \
               src/cache.cpp     \
               src/sha256.cpp    \
               src/transform.cpp \
               src/exec.cpp

target.path = bin
INSTALLS += target
