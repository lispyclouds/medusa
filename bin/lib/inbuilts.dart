library pyinbuilts;

import "dart:io";
import "dart:collection";

String str(data) {
    return data.toString();
}

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

class Range extends Object with IterableMixin<int> {
    Range(int this.start, [int this.stop, int this.step = 1]) {
        if (stop == null ) {
            stop = start;
            start = 0;
        }

        if (step == 0)
            throw new ArgumentError("step must not be 0");
    }

    Iterator<int> get iterator {
        return new RangeIterator(start, stop, step);
    }

    int get length {
        if ((step > 0 && start > stop) || (step < 0 && start < stop))
            return 0;
        return ((stop - start) / step).ceil();
    }

    bool get isEmpty => length == 0;

    int get hashCode {
        int result = 17;
        result = 37 * result + start.hashCode;
        result = 37 * result + stop.hashCode;
        result = 37 * result + step.hashCode;
        return result;
    }

    String toString() {
        return step == 1 ? "Range($start, $stop)" : "Range($start, $stop, $step)";
    }

    bool every(bool f(int e)) {
        for (int e in this) {
            if (f(e) == false)
                return false;
        }
        return true;
    }

    bool some(bool f(int e)) {
        for (int e in this) {
            if (f(e))
                return true;
        }
        return false;
    }

    void forEach(void f(int e)) {
        for (int e in this)
            f(e);
    }

    List<int> filter(bool f(int e)) {
        var l = new List<int>();
        for (int e in this) {
            if (f(e))
                l.add(e);
        }
        return l;
    }

    bool operator == (Range other) {
        return (other != null && start == other.start && stop == other.stop && step == other.step);
    }

    int start;
    int stop;
    final int step;
}

class RangeIterator implements Iterator<int> {

    int _pos;
    final int _stop;
    final int _step;

    RangeIterator(int pos, int stop, int step) : _stop = stop, _pos = pos-step, _step = step;

    int get current {
        return _pos;
    }

    bool moveNext() {
        if (_step > 0  ? _pos + _step> _stop - 1 : _pos + _step < _stop + 1)
            return false;

        _pos += _step;
        return true;
    }
}

Range range(int start_inclusive, [int stop_exclusive, int step = 1]) => new Range(start_inclusive, stop_exclusive, step);
Range indices(lengthable) => new Range(0, lengthable.length);