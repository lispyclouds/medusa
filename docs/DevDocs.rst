Developers Corner
=================

We'd love to have your help in making Medusa better and Python faster. Any and all contributions are welcome. Frankly speaking there's still a hell lot to do.

How Medusa works
----------------

Running python faster has been a major challenge since the very start. Python brought with it the joy of flexibility
and simpler prototyping. What Medusa intends to do is run the same python scripts you wrote faster.
Medusa takes the python file and creates its equivalent dart code. This Dart code can be run on the DartVM.

The challenge here is converting python to dart. Medusa tokenizes the python file and creates an Abstract Syntax Tree.
As we traverse this tree from one node to another, the equivalent Dart code is emitted and at the end all this code is stitched , optimized and run on the DartVM.



Development Workflow
--------------------
    * :ref:`Creating the environment`
    * :ref:`Workflow process`
    * :ref:`How to submit a patch`
    * :ref:`Coding Conventions`
