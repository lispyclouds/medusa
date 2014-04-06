library PyTime;

import "inbuilts.dart";

class $PyTime {
    var _tobj;

    $PyTime() {
        _tobj = new DateTime.now();
    }

    time() => new $PyNum(_tobj.millisecondsSinceEpoch);
}