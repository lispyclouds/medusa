class $PyTime {
    var _tobj;

    $PyTime() {
        _tobj = new DateTime.now();
    }

    time() => _tobj.millisecondsSinceEpoch / 1000.0;
}