=================
Developers Corner
=================

We'd love to have your help in making Medusa better and Python faster. Any and all contributions are welcome. Frankly speaking there's still a hell lot to do.

How Medusa works
================

Python is one of the most widely used scripting languages and has immense deployment
and brought with it the joy of flexibility and simpler prototyping.One place where it falls short is development of very large scale software implementations primarily because the implementation is not fast enough.
|
What Medusa intends to do is run the same python code you wrote a lot faster.

The Concept
-----------
Medusa follows a six step procedure:
    1. Breaks the python source file into tokens
    2. Parse these tokens into an Abstract Syntax Tree while checking for errors
    3. Walk the tree and emit the equivalent Dart code at each node while optimizing it
    4. Cache the code in persistent SQLite3 Database
    5. Invoke the Dart virtual machine with Dart code
    6. Cache the generated machine code and provide output

Development Workflow
====================
Introduction
------------
Medusa encourages everyone to join and implement new features, fix some bugs,
review pull requests and suggest ideas, take part in general discussions etc.

Creating the environment
------------------------
Before you start contributing, you will have to follow the steps below to make
sure that there are no hiccups when you are working.

Install git
^^^^^^^^^^^
Installing git on linux-like systems can be done using the native package management systems.
::
    $ sudo apt-get install git

or.
::
    $ yum install git

Windows users may download the installer from
::
    http://python.org/download/

Then do not forget to add Python to the $PATH environment.

On Windows and Mac OS X, the easiest way to get git is to download GitHub’s
software, which will install git, and also provide a nice GUI (this tutorial
will be based on the command line interface). Note, you may need to go into the
GitHub preferences and choose the “Install Command Line Tools” option to get git
installed into the terminal.
If you do decide to use the GitHub GUI, you should make sure that any
“sync does rebase” option is disabled in the settings.

Cloning Medusa
^^^^^^^^^^^^^^
Clone medusa's repository on your machine to browse and work on the code locally.
::
    $ git clone https://github.com/rahul080327/medusa
    $ cd medusa

How to submit a patch
^^^^^^^^^^^^^^^^^^^^^
Coding Conventions
^^^^^^^^^^^^^^^^^^
