library input;

import 'dart:io';

String input([message]) {
    if (message != null)
        print(message);
    return stdin.readLineSync(encoding: SYSTEM_ENCODING);
}