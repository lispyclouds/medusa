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

QMAKE_CXXFLAGS_RELEASE -= -O
QMAKE_CXXFLAGS_RELEASE -= -O1
QMAKE_CXXFLAGS_RELEASE -= -O2

win32 {
  QMAKE_CXXFLAGS += -arch:x64
  QMAKE_CXXFLAGS += -D "_CRT_SECURE_NO_WARNINGS"
  QMAKE_CXXFLAGS_RELEASE *= /O2
}

linux {
  QMAKE_CXXFLAGS += -m64
  QMAKE_CXXFLAGS_RELEASE *= -O3
}