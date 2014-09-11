## Medusa

An attempt at making Python stronger and faster like Medusa herself!

Python being an interpreted language has its pros and cons and the aim is to fix one of the most obvious cons of Python: its execution speed.
We all love Python for its simplicity and flexibility but when it comes to writing large volumes of code involving complex operations and recursions Python somewhat falls short compared to the other native/JIT languages.

In late 2011, Google came up with Dart, a language aiming for the unification of server and client side web development and scalable apps. Along with it came The Dart Virtual Machine. A hyper fast VM which builds upon the V8 js engine and even outperforms it. We decided why not let Python have a go on this?

The main aim behind creating the Medusa project is giving a typless and flexible language like Python a faster execution environment while still maintaining all its flexibility which we all love. Numerous projects such as the ShedSkin project which converts implicitly typed Python to C++ have tried doing it, but have put some or the other restriction on the input Python code. The Medusa project aims at running pre-existing Python code without any or minimal modification at a much faster rates compared to the usual implementations.

Still in its nascent stages and implemented using Qt/C++, Python and Dart, the project works by compiling Python code to a highly optimized Dart code in real time, persistently caching it and letting it rip on the Dart VM. The Dart VM like V8 compiles the dart code directly to machine code and using its vast array of runtime optimizations runs at a much higher speed compared to the CPython implementation and at times upto a 1000 - 1500% faster while maintaining all the features Python offers. Apart from this Python is further enriched with extra features provided by the Dart VM and you can do more stuff with Python which isn't possible with the vanilla Python.

## Installing

<b>Debian Derived Linux users:</b>

Simply run <b>./INSTALL</b> after cloning this repo on your Debian based Linux distro. Thats it. All dependencies are installed, code compiled and paths setup automatically.

<b>Mac OSX Users (packaged app):</b>
Coming Soon ;) Thanks for your patience.

<b>Mac OSX Users (building from source):</b>
* Install XCode (Sorry for the bandwidth hogging...)
* Install python 2.7.x and add it to PATH
* Download and Install latest Qt5 for Mac from [here](http://qt-project.org/downloads) and add qmake and moc to PATH
* Download the latest Dart SDK from [here](https://storage.googleapis.com/dart-archive/channels/stable/release/latest/sdk/dartsdk-macos-ia32-release.zip), unzip and add the dart executable to PATH
* Clone this repo and simply run <b>./INSTALL.mac</b>
* After a succesful compile medusavm binary is available in /usr/bin/ for use
* For updates and subsequent builds, fetch changes and just run <b>./INSTALL.mac</b>

<b>Yeah, I finally have a MacBook! ^_^</b>

<b>Others:</b>
* Install C++ compilers and Make tools
* Install Qt5 build tools and libs
* Install Dart SDK
* Install Python 2.7.x
* Rum moc on inc/transform.h to inc/transform_moc.h
* Run qmake on medusa.pro
* Run make
* Use the medusavm executable

## Running

<b>Using Medusa:</b>
* Medusa is available as <b>medusavm</b> after a successful buid and install
* Python programs can be run by passing them as parameters: <b>medusavm hello.py</b>
* Medusa can be stopped after the Dart compile phase by passing a -c switch: <b>medusavm -c hello.py</b>. The Dart code is obtained in hello.dart in the same directory.
* Python files can be globally installed into Medusa for imports by other files: <b>medusavm -install python_file</b>
* Help is at: <b>medusavm --help</b>

## Contributing

We'd love to have your help in making Medusa better and Python faster. Any and all contributions are welcome. Frankly speaking there's still a hell lot to do.

## License

<b>The BSD 3-Clause License</b>

<b>Copyright (c) 2013-2014, Rahul De, Apoorv Agarwal and Aakash Giri. VIT University
All rights reserved.</b>

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Fear and Respect her at the same time!

![alt tag](https://raw.github.com/rahul080327/medusa/master/icon.jpg)

## Just Kidding, Happy Pythoning Yo!
