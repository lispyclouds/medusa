QT                       += core sql
QT                       -= gui

TARGET                    = medusavm

CONFIG                   += console release
CONFIG                   -= app_bundle

TEMPLATE                  = app

INCLUDEPATH              += inc

SOURCES                  += src/main.cpp      \
                            src/cache.cpp     \
                            src/sha256.cpp    \
                            src/transform.cpp \
                            src/exec.cpp

INSTALLS                 += target

QMAKE_CXXFLAGS_RELEASE   -= -O
QMAKE_CXXFLAGS_RELEASE   -= -O1
QMAKE_CXXFLAGS_RELEASE   -= -O2

win32 {
  target.path              = .
  QMAKE_CXXFLAGS          -= -FS
  QMAKE_CXXFLAGS          += -D "_CRT_SECURE_NO_WARNINGS"
  QMAKE_CXXFLAGS_RELEASE  *= /O2
  QMAKE_LFLAGS            += /MACHINE:x64
}

linux {
  target.path             = /usr/bin
  QMAKE_CXXFLAGS         += -m64
  QMAKE_CXXFLAGS_RELEASE *= -O3
}