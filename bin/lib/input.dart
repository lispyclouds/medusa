library input;

import 'dart:io';

String raw_input([message]) {
    if (message != null)
        stdout.write(message);

    return stdin.readLineSync(encoding: SYSTEM_ENCODING);
}

num input([message]) {
    if (message != null)
        stdout.write(message);

    num value;

    try {
        value = num.parse(stdin.readLineSync(encoding: SYSTEM_ENCODING));
        return value;
    } catch (ex) {
        print("Fatal Error: Non numeric characters in input");
        exit(1);
    }
}