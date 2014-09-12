=============
Installation
=============

Medusa is currently supported only on debian. Windows and Mac builds will soon be available

Debian Users
============

Simply run ./INSTALL after cloning this `repo <https://github.com/rahul080327/medusa>`_ on your Debian
 based Linux distro.
Thats it. All dependencies are installed, code compiled and paths setup automatically.

Mac OSX Users (building from source)
====================================

    * Install XCode if not installed (Sorry for the bandwidth hogging...)
    * Install python 2.7.x if not installed and add it to PATH
    * Download and Install latest Qt5 for Mac from `here <http://qt-project.org/downloads>`_ and add qmake and moc to PATH
    * Download the latest Dart SDK from `here <https://storage.googleapis.com/dart-archive/channels/stable/release/latest/sdk/dartsdk-macos-ia32-release.zip>`_, unzip and add the dart executable to PATH
    * Clone this repo and simply run ./INSTALL.mac
    * After a successful compile medusavm binary is available in /usr/bin/ for use
    * For updates and subsequent builds, fetch changes and just run ./INSTALL.mac

Others
======
    * Install C++ compilers and Make tools
    * Install Qt5 build tools and libs
    * Install Dart SDK
    * Install Python 2.7.x
    * Rum moc on inc/transform.h to inc/transform_moc.h
    * Run qmake on medusa.pro
    * Run make
    * Use the medusavm executable

Using Medusa
============
    * Medusa is available as medusavm after a successful buid and install
    * Python programs can be run by passing them as parameters: medusavm hello.py
    * Medusa can be stopped after the Dart compile phase by passing a -c switch: medusavm -c hello.py. The Dart code is obtained in hello.dart in the same directory.
    * Python files can be globally installed into Medusa for imports by other files: medusavm -install python_file
    * Help is at: medusavm --help
