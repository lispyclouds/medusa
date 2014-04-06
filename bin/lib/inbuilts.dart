library inbuilts;

import "dart:io";
import "dart:collection";
import "dart:math";
import "sprintf.dart";

class $PyFile {
    File handle;
    bool closed, softspace;
    String mode, name;

    $PyFile(name, [mode = 'r']) {
        this.closed = false;
        this.name = name.toString();
        this.mode = mode.toString();
        this.softspace = true;

        switch (this.mode) {
            case "r":
                handle = new File(name).openSync(mode: FileMode.READ);
                break;
            case "w":
                handle = new File(name).openSync(mode: FileMode.WRITE);
                break;
        }
    }

    read([bytes]) {
        if (bytes == null)
            bytes = handle.lengthSync();
        else
            bytes = bytes.value;

        return new $PyString(new String.fromCharCodes(handle.readSync(bytes)));
    }

    readline() {
        // do something here please
    }

    readlines() => new $PyString(new File(name).readAsLinesSync());
    write(data) => handle.writeStringSync(data.toString());
    tell() => handle.positionSync();

    writelines(lines) {
        for (int i = 0; i < lines.length; i++)
            handle.writeStringSync(lines[i] + "\n");
    }

    seek(position, [whence]) {
        if (whence == null)
            whence = 0;
        else
            whence = whence.value;
        position = position.value;

        switch(whence) {
            case 0:
                handle.setPositionSync(position);
                break;

            case 1:
                handle.setPositionSync(handle.positionSync() + position);
                break;

            case 2:
                handle.setPositionSync(handle.lengthSync() + position);
                break;
        }
    }

    close() {
        closed = true;
        handle.closeSync();
    }
}

open(name, [mode = 'r']) {
    name = name.toString();

    $PyFile file = new $PyFile(name, mode);
    if ((mode == "r" || mode == "rb") && !new File(name).existsSync())
        throw new FileSystemException();

    return file;
}

file(path, [mode = 'r']) {
    return open(path, mode);
}

class $PyNone {
    static final $PyNone _inst = new $PyNone._internal();

    factory $PyNone() => _inst;
    $PyNone._internal();
    toString() => "None";

    operator ==(other) {
        switch ($getType(other)) {
            case 0: return true;
            default: return false;
        }
    }

    operator <(other) {
        switch ($getType(other)) {
            case 0: return false;
            default: return true;
        }
    }

    operator >(other) => false;
    operator <=(other) => true;

    operator >=(other) {
        switch ($getType(other)) {
            case 0: return true;
            default: return false;
        }
    }
}

class $PyNum {
    final num _value;

    const $PyNum(this._value);
    get value => _value;
    toString() => _value.toString();

    static num toNum(x) {
        if (x is $PyNum)
            return x.value;
        else if (x is num)
            return x;
        else
            throw "Invalid Operands for numeric operations";
    }

    operator +(other) => new $PyNum(_value + toNum(other));
    operator -(other) => new $PyNum(_value - toNum(other));
    operator *(other) => new $PyNum(_value * toNum(other));
    operator /(other) {
        num result;
        other = toNum(value);
        if (_value is double || other is double)
            result = _value / other;
        else
            result = _value ~/ other;
        return new $PyNum(result);
    }

    operator |(other) => new $PyNum(_value | toNum(other));
    operator &(other) => new $PyNum(_value & toNum(other));
    operator ^(other) => new $PyNum(_value ^ toNum(other));
    operator %(other) => new $PyNum(_value % toNum(other));
    operator <<(other) => new $PyNum(_value << toNum(other));
    operator >>(other) => new $PyNum(_value >> toNum(other));

    operator ==(other) {
        switch ($getType(other)) {
            case 5:
            case 6: return _value == toNum(other);
            default: return false;
        }
    }

    operator <(other) {
        switch ($getType(other)) {
            case 0: return false;
            case 5:
            case 6: return _value < toNum(other);
            default: return true;
        }
    }

    operator >(other) {
        switch ($getType(other)) {
            case 0: return true;
            case 5:
            case 6: return !(this < other) && (this != other);
            default: return false;
        }
    }

    operator <=(other) {
        switch ($getType(other)) {
            case 5:
            case 6: return (this < other) || (this == other);
            default: return false;
        }
    }

    operator >=(other) {
        switch ($getType(other)) {
            case 5:
            case 6: return (this > other) || (this == other);
            default: return false;
        }
    }
}

$PyNum int([x]) {
    if (x == null)
        x = 0;
    else  if (x is $PyNum)
        x = x._value;
    else if (x is $PyString) {
        try {
            x = num.parse(x.toString());
        } catch (ex) {
            print("Invalid string literal for numeric parsing");
            exit(1);
        }
    }
    else if (x is! num)
        throw "Invalid numeric data";
    return new $PyNum(x);
}
$PyNum float([x]) => int(x);

class $PyBool {
    final bool _boo;

    const $PyBool(this._boo);
    get value => _boo;
    toString() => _boo.toString();
    compareTo(other) => this < other ? this : other;

    operator ==(other) {
        switch($getType(other)) {
            case 1: return _boo == other.value;
            case 0:
            case 2:
            case 3:
            case 4:
            case 5:
            case 6:
            case 7:
            case 8: return false;
        }
    }

    operator <(other) {
        switch($getType(other)) {
            case 0: return false;
            case 1: return _boo == false && other.value == true ? true : false;
            case 2:
            case 3:
            case 4:
            case 5:
            case 6:
            case 7:
            case 8: return true;
        }
    }

    operator >(other) => !(this < other) && (this != other);
    operator <=(other) => (this < other) || (this == other);
    operator >=(other) => (this > other) || (this == other);
}

bool([value]) {
    if (value == null)
        value = false;
    else {
        switch ($getType(value)) {
            case 0:
                value = false;
                break;
            case 1:
                value = value.value;
                break;
            case 5:
                value = (value.value == 0 ? false : true);
                break;
            case 6:
                value = (value == 0 ? false : true);
                break;
            case 2:
            case 3:
            case 4:
            case 7:
            case 8:
                value = (value.length == 0 ? false : true);
                break;
        }
    }
    return new $PyBool(value);
}

class $PyTuple extends IterableBase {
    final List _tuple;

    const $PyTuple(this._tuple);
    get length => new $PyNum(_tuple.length);
    compareTo(other) => this < other ? this : other;

    toString() {
        int i = 0;
        String str = "(";

        for (i = 0; i < _tuple.length; i++) {
            str += _tuple[i].toString();
            if (i < _tuple.length - 1 || _tuple.length == 1)
                str += ", ";
        }
        str += ")";

        return str;
    }

    operator [](index) {
        if (index is num)
            return _tuple[index];
        else if (index is $PyNum)
            return _tuple[index.value];
        else
            throw "Invalid Tuple Key";

    }

    operator []=(i, j) => throw "Assignment not possible in Tuple";
    operator +(tupleObj) {
        if (tupleObj is $PyTuple) {
            $PyTuple newTupObj = new $PyTuple(this._tuple);
            for (var item in tupleObj._tuple)
                newTupObj._tuple.add(item);
            return newTupObj;
        }
        else
            throw "Invalid operand for concatenation";
    }

    operator *(integer) {
        $PyTuple newTupObj = new $PyTuple(this._tuple);
        for (int i = 0; i < integer.value; i++) {
            for (var item in this._tuple)
                newTupObj._tuple.add(item);
        }
        return newTupObj;
    }

    operator ==(other) {
        switch($getType(other)) {
            case 8:
                if (this.length != other.length)
                    return false;
                for (var i = 0; i < this.length; i++) {
                    if (_tuple[i] != other._tuple[i])
                        return false;
                }
                return true;
            default:
                return false;
        }
    }

    operator <(other) {
        switch($getType(other)) {
            case 0:
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
            case 6:
            case 7: return false;
            case 8:
                for (var i = 0; i < (this.length <= other.length ? this.length : other.length); i++) {
                    if (_tuple[i] > other._tuple[i])
                        return false;
                    else if (_tuple[i] < other._tuple[i])
                        return true;
                }
                return other.length < this.length ? false : true;
            default: break;
        }
    }

    operator >(other) => !(this < other) && (this != other);
    operator <=(other) => (this < other) || (this == other);
    operator >=(other) => (this > other) || (this == other);

    getList() => _tuple;
    contains(comparator) => _tuple.contains(comparator);
    get iterator => _tuple.iterator;
}

$PyTuple tuple([iterable]) {
    List holder = [];
    if (iterable != null && iterable is $PyTuple)
        holder = iterable._tuple;
    else {
        for (var item in iterable)
            holder.add(item);
    }
    return new $PyTuple(holder);
}

class $PyString extends IterableBase {
    final String _str;

    const $PyString(this._str);
    get iterator => this.toList().iterator;
    get length => new $PyNum(_str.length);

    capitalize() {
        String capzed = _str.toLowerCase();
        if (capzed.length > 0)
            return new $PyString(capzed.replaceFirst(capzed[0], capzed[0].toUpperCase()));
        else
            return this;
    }

    center(width, [fillChar = " "]) {
        if ($getType(width.value) != 6 || fillChar.length > 1)
            throw "Invalid Arguments";

        fillChar = fillChar.toString();
        int extra = width.value - _str.length;

        if (extra <= 0)
            return this;
        else {
            int left = extra ~/ 2, right = width.value - left - _str.length, i;
            String finalStr = "";
            for (i = 0; i < left; i++) finalStr += fillChar;
            finalStr += _str;
            for (i = 0; i < right; i++) finalStr += fillChar;
            return new $PyString(finalStr);
        }
    }

    compareTo(other) =>  this < other ? this : other;
    join(list) => new $PyString(list.join(_str));
    replace(target, value) => new $PyString(_str.replaceAll(target.toString(), value.toString()));
    strip() => new $PyString(_str.trim());

    split(sep) {
        var parts = _str.split(sep.toString()), list = new $PyList([]);
        for (var p in parts)
            list.append(new $PyString(p));
        return list;
    }

    zfill(width) {
        int toPad = width.value - _str.length, pad = "";
        for (int i = 0; i < toPad; i++)
            pad += "0";
        return new $PyString(pad + _str);
    }

    toString() => _str;
    get hashCode => _str.hashCode;

    toList() {
        List list = [];
        for (var i in _str.split(''))
            list.add(new $PyString(i));
        return list;
    }

    operator +(str) => new $PyString(_str + str.toString());
    operator %(collection) {
        var string = this.toString();

        if (collection is $PyTuple) {
            RegExp exp = new RegExp(r"%\s?[diuoxXeEfFgGcrs]");
            Iterable<Match> matches = exp.allMatches(string);
            int i = 0;
            var List = collection.getList();

            for (var m in matches) {
                String match = m.group(0);
                if (match == "%s" || match == "% s")
                    List[i] = List[i].toString();
                if (match == "%d" || match == "% d" || match == "%f" || match == "% f") {
                    if (List[i] is $PyBool)
                        (List[i] == true) ? List[i] = 1 : List[i] = 0;
                    else
                        List[i] = List[i].value;
                }
                i++;
            }
            return new $PyString($sprintf(string, List));
        } else if (collection is $PyDict) {
            RegExp exp = new RegExp(r"%(\([a-zA-Z_]+\))*\s?[diuoxXeEfFgGcrs]");
            var List = [];
            Iterable<Match> matches = exp.allMatches(string);
            int i = 0, currentIndex = 0;
            var newString = "";
            var key = "";

            for (var m in matches) {
                String match = m.group(0);
                while(currentIndex <= m.start)
                    newString += string[currentIndex++];

                currentIndex = m.start + 2;
                while(string[currentIndex] != ")")
                    key += string[currentIndex++];

                currentIndex = m.end - 1;
                if (string[currentIndex] == "s")
                    List.add(collection[key].toString());
                else if (string[currentIndex] == "d" && collection[key] is bool) {
                    if (collection[key])
                        List.add(1);
                    else
                        List.add(0);
                }
                else
                    List.add(collection[key]);
                key = "";
                newString += string[currentIndex++];
            }
            return new $PyString($sprintf(newString, List));
        }
    }

    format(list, dictionary) {
        var string = this.toString();
        RegExp exp = new RegExp(r"{\d+}|{[a-zA-Z0-9_]+}");
        Iterable<Match> matches = exp.allMatches(string);
        int i = 0, currentIndex = 0;
        var newString = "";
        var key;

        for (var m in matches) {
            String match = m.group(0);
            key = "";
            while(currentIndex < m.start)
                newString += string[currentIndex++];

            currentIndex++;
            while(string[currentIndex] != "}")
                key += string[currentIndex++];

            exp = new RegExp(r"{\d+}");
            if (exp.hasMatch(match))
                newString += list[int.parse(key)].toString();
            else
                newString += dictionary[key].toString();

            currentIndex = m.end;
        }
        return new $PyString(newString);
    }

    operator *(mul) {
        String pdt = "";
        for (int i = 0; i < mul.value; i++)
            pdt += _str;

        return new $PyString(pdt);
    }

    operator [](index) => new $PyString(_str[index.value]);
    operator ==(other) {
        switch ($getType(other)) {
            case 0:
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
            case 8: return false;
            case 6:
            case 7: return (_str.compareTo(other.toString()) == 0) ? true : false;
        }
    }

    operator <(other) {
        switch ($getType(other)) {
            case 0:
            case 1:
            case 2:
            case 3:
            case 4:
            case 5: return false;
            case 6:
            case 7: return (_str.compareTo(other.toString()) < 0) ? true : false;
            case 8: return true;
        }
    }

    operator >(other) => !(this < other) && (this != other);
    operator <=(other) => (this < other) || (this == other);
    operator >=(other) => (this > other) || (this == other);
}

$PyString str([data]) {
    if (data == null)
        data = "";
    return new $PyString(data.toString());
}

class $PyList extends IterableBase {
    final List _list;

    const $PyList(this._list);
    get iterator => _list.iterator;
    get first => _list.first;
    get last => _list.last;
    get length => new $PyNum(_list.length);

    extend(list) {
        for (var item in list)
            _list.add(item);
    }

    pop([pos]) {
        var v;
        if (pos == null) {
            v = _list.last;
            _list.removeLast();
        } else {
            v = _list[pos.value];
            _list.removeAt(pos.value);
        }
        return v;
    }

    count(item) {
        var c = 0;
        for (var elem in _list) {
            if (elem == item)
                c++;
        }
        return new $PyNum(c);
    }

    compareTo(other) => this < other ? this : other;
    shuffle() => new $PyList(_list.shuffle());
    toList() => _list;
    append(item) => _list.add(item);
    insert(pos, item) => _list.insert(pos.value, item);
    remove(item) => _list.remove(item);
    index(item) => _list.indexOf(item);
    sort() => new $PyList(_list.sort());
    reverse() => _list = _list.reversed.toList();
    toString() => _list.toString();
    contains(elem) => _list.contains(elem);

    operator +(iterable) {
        extend(iterable);
        return this;
    }

    operator [](index) {
        if (index is num)
            return _list[index];
        else if (index is $PyNum)
            return _list[index.value];
        else
            throw "Invalid List Key";
    }

    operator []=(pos, item) {
        if (pos is num)
            _list[pos] = item;
        else if (pos is $PyNum)
            _list[pos.value] = item;
        else
            throw "Invalid List Key";
    }

    operator *(mul) {
        var pdt = new $PyList([]);
        for (var i = 0; i < mul; i++)
            pdt += this;

        return pdt;
    }

    operator ==(other) {
        switch($getType(other)) {
            case 2:
                if (this.length != other.length)
                    return false;
                for (int i = 0; i < this.length; i++) {
                    if (_list[i] != other._list[i])
                        return false;
                }
                return true;
            default:
                return false;
        }
    }

    operator <(other) {
        switch($getType(other)) {
            case 0:
            case 1:
            case 2:
            case 5:
            case 6: return false;
            case 3:
                for (int i = 0; i < (this.length <= other.length ? this.length : other.length); i++) {
                    if (_list[i] > other._list[i])
                        return false;
                    else if (_list[i] < other._list[i])
                        return true;
                }
                return other.length < this.length ? false : true;
            case 7:
            case 8: return true;
            default: break;
        }
    }

    operator >(other) => !(this < other) && (this != other);
    operator <=(other) => (this < other) || (this == other);
    operator >=(other) => (this > other) || (this == other);
}

list([iterable]) {
    if (iterable == null)
        iterable = [];
    else {
        switch ($getType(iterable)) {
            case 7:
            case 3:
                iterable = iterable.toList();
                break;
            case 2:
                iterable = iterable.keys;
                break;
            case 8:
                iterable = iterable._tuple;
                break;
            case 4:
                break;
            default: throw "Invalid parameter";
        }
    }
    return new $PyList(iterable);
}

class $PySet extends IterableBase {
    final Set _set;

    const $PySet(iterable);
    get iterator => this._set.iterator;
    get length => _set.length;
    add(var elem) => this._set.add(elem);

    isdisjoint(iterable) {
        $PySet other = new $PySet(iterable);
        if (this._set.intersection(other._set).length == 0)
            return true;
        else
            return false;
    }

    issubset(iterable) {
        $PySet other = new $PySet(iterable);
        return other._set.containsAll(this._set);
    }

    issuperset(iterable) {
        $PySet other = new $PySet(iterable);
        return this._set.containsAll(other._set);
    }

    union(iterable) {
        $PySet other = new $PySet(iterable);
        return new $PySet(this._set.union(other._set));
    }

    intersection(iterable) {
        $PySet other = new $PySet(iterable);
        return new $PySet(this._set.intersection(other._set));
    }

    difference(iterable) {
        $PySet other = new $PySet(iterable);
        return new $PySet(this._set.difference(other._set));
    }

    symmetric_difference(iterable) {
        $PySet other = new $PySet(iterable);
        return new $PySet(this._set.union(other._set).difference(this._set.intersection(other._set)));
    }

    update(iterable) {
        $PySet other = new $PySet(iterable);
        this._set = this._set.union(other._set);
    }

    intersection_update(iterable) {
        $PySet other = new $PySet(iterable);
        this._set = this._set.intersection(other._set);
    }

    difference_update(iterable) {
        $PySet other = new $PySet(iterable);
        this._set = this._set.difference(other._set);
    }

    symmetric_difference_update(iterable) {
        $PySet other = new $PySet(iterable);
        this._set = this._set.union(other._set).difference(this._set.intersection(other._set));
    }

    remove(element) => this._set.remove(element);

    discard(element) {
        if (this._set.contains(element))
            this._set.remove(element);
    }

    toString() => "set([" + this._set.join(",") + "])";
    clear() => this._set.clear();

    operator -(other) {
        if (other is $PySet)
            return new $PySet(this._set.difference(other._set));
        else
            throw "Invalid Arguments";
    }

    operator ==(other) {
        if (other is $PySet) {
            if (other._set.length == this._set.length)
                return this._set.difference(other._set).length == 0;
            return false;
        }
        else
            throw "Invalid Arguments";
    }

    operator <=(other) {
        if (other is $PySet)
            return other._set.containsAll(this._set);
        else
            throw "Invalid Arguments";
    }

    operator <(other) {
        if (other is $PySet)
            return (this <= other && this != other);
        else
            throw "Invalid Arguments";
    }

    operator >=(other) {
        if (other is $PySet)
            return this._set.containsAll(other._set);
        else
            throw "Invalid Arguments";
    }

    operator >(other) {
        if (other is $PySet)
            return (other <= this && other != this);
        else
            throw "Invalid Arguments";
    }

    operator |(other) {
        if (other is $PySet)
            return new $PySet(this._set.union(other._set));
        else
            throw "Invalid Arguments";
    }

    operator &(other) {
        if (other is $PySet)
            return new $PySet(this._set.intersection(other._set));
        else
            throw "Invalid Arguments";
    }

    operator ^(other) {
        if (other is $PySet)
            return new $PySet(this._set.union(other._set).difference(this._set.intersection(other._set)));
        else
            throw "Invlaid Arguments";
    }
}

set([iterable]) {
    if (iterable != null)
        iterable = new Set.from(iterable);
    else
        iterable = new Set();

    return new $PySet(iterable);
}

class $PyDict extends IterableBase {
    final Map _dict;

    const $PyDict(this._dict);
    get length => _dict.length;

    fromKeys(seq, [values]) {
        _dict.clear();

        for (var value in seq)
            _dict[value] = null;

        if (values != null) {
            for (var value in values)
                _dict[value] = value;
        }
    }

    get(key, [fallback]) {
        if (_dict.containsKey(key))
            return _dict[key];
        else
            return fallback;
    }

    items() {
        $PyList items = new $PyList([]);
        for (var key in this)
            items.append(_tuple([key, _dict[key]]));
        return items;
    }

    pop(key, [fallback]) {
        if (_dict.containsKey(key)) {
            var value = _dict[key];
            _dict.remove(key);
            return value;
        } else
            return fallback;
    }

    popitem() {
        if (_dict.length == 0)
            return;

        Random rng = new Random();
        var key = _dict.keys[rng.nextInt(_dict.length)];
        var value = tuple([keys, _dict[key]]);

        _dict.remove(key);
        return value;
    }

    setdefault(key, [value]) {
        if (_dict.containsKey(key))
            return _dict[key];
        else {
            _dict[key] = value;
            return value;
        }
    }

    update([other]) {
        for (var pair in other)
            _dict[pair[0]] = pair[1];
    }

    compareTo(other) => this < other ? this : other;
    iteritems() => items();
    iterkeys() => new $PyList(_dict.keys);
    itervalues() => new $PyList(_dict.values);
    keys() => new $PyList(_dict.keys.toList());
    values() => new $PyList(_dict.values.toList());
    has_key(key) => _dict.hasKey(key);
    contains(key) => has_Key(key);
    copy() => this;
    clear() => _dict.clear();
    get iterator => _dict.keys.iterator;
    toString() => _dict.toString();
    viewitems() => _dict.items();
    viewkeys() => _dict.keys;
    viewvalues() => _dict.values;
    operator [](index) => _dict[index];
    operator []=(pos, item) => _dict[pos.value] = item;

    operator ==(other) {
        switch($getType(other)) {
            case 2:
                var thisKeys = this.keys();
                var otherKeys = other.keys();
                var thisValues = this.values();
                var otherValues = other.values();
                thisKeys.sort();
                otherKeys.sort();
                thisValues.sort();
                otherValues.sort();
                if (thisKeys != otherKeys || thisValues != otherValues)
                    return false;
                for (var key in thisKeys) {
                    if (_dict[key] != other._dict[key])
                        return false;
                }
                return true;
            default:
                return false;
        }
    }

    operator <(other) {
        switch($getType(other)) {
            case 0:
            case 1:
                return false;
            case 2:
                var thisKeys = this.keys();
                var otherKeys = other.keys();
                thisKeys.sort();
                otherKeys.sort();
                if (thisKeys < otherKeys)
                    return true;

                else if (thisKeys == otherKeys) {
                    for (var key in this.keys()) {
                        if (_dict[key] < other._dict[key])
                            return true;
                        else if (_dict[key] > other._dict[key])
                            return false;
                    }
                    return false;
                }
                else
                    return false;
            case 3:
            case 4:
            case 5:
            case 6:
            case 7:
            case 8: return true;
        }
    }

    operator >(other) => !(this < other) && (this != other);
    operator <=(other) => (this < other) || (this == other);
    operator >=(other) => (this > other) || (this == other);
}

dict([pairs]) {
    Map dict = {};
    if (pairs != null) {
        $PyNum key = new $PyNum(0), key1 = new $PyNum(1);

        if (pairs is $PyList) {
            for (var pair in pairs)
                dict[pair[key]] = pair[key1];
        }
        else if (pairs is! $PyDict)
            throw "Invalid parameter";
    }
    return new $PyDict(dict);
}

abs(n) {
    if (n < 0)
        return n * -1;
    else
        return n;
}

all(iterable) {
    var i;
    for (i in iterable) {
        if (!$checkValue(i))
            return false;
    }
    return true;
}

any(iterable) {
    for (var i in iterable) {
        if ($checkValue(i))
            return true;
    }
    return false;
}

bin(integer) {
    integer = integer.value;
    int num1, x = 0;
    while (integer > 0) {
        x = integer % 2;
        num1 = num1 * 10 + x;
        integer ~/= 2;
    }
    return new $PyNum(num1);
}

len(target) => new $PyNum(target.length);

raw_input([message]) {
    if (message != null)
        stdout.write(message);
    return new $PyString(stdin.readLineSync(encoding: SYSTEM_ENCODING));
}

input([message]) {
    if (message != null)
        stdout.write(message);

    try {
        var value = num.parse(stdin.readLineSync(encoding: SYSTEM_ENCODING));
        return new $PyNum(value);
    } catch (ex) {
        print("Fatal Error: Non numeric characters in input; Try raw_input()");
        exit(1);
    }
}

sum(var iterable, [start]) {
    if (start is $PyString) {
        print("TypeError: sum() can't sum strings [use ''.join(seq) instead]");
        exit(1);
    }
    if (start == null)
        start = new $PyNum(0);

    var total = start;
    for (var i in iterable) {
        if (i == true)
            i = new $PyNum(1);
        else if (i == false)
            i = new $PyNum(0);
        total += i;
    }
    return total;
}

zip([list, starArgs]) {
    int i, j, length = 0;
    $PyList finalList = new $PyList([]);
    List tempList = [];

    if (list.length == 0 && starArgs == null)
        return new $PyList([]);
    else if (list.length != 0 && starArgs != null)
        print("This should not print.");
    else {
        if (list.length == 0 && starArgs != null)
            list = starArgs;

        if (list.length > 0)
            length = list[0].length;

        for (i = 1; i < list.length; i++) {
            if (list[i].length < length)
                length = list[i].length;
        }

        for (i = 0; i < length; i++) {
            tempList.clear();
            for (j = 0; j < list.length; j++)
                tempList.add(list[j][i]);
            $PyTuple tuple = new $PyTuple(tempList);
            finalList.append(tuple);
        }
        return finalList;
    }
}

$getType(variable) {
    if (variable is $PyNone)
        return 0;
    else if (variable is $PyBool)
        return 1;
    else if (variable is $PyDict)
        return 2;
    else if (variable is $PyList)
        return 3;
    else if (variable is List)
        return 4;
    else if (variable is $PyNum)
        return 5;
    else if (variable is num)
        return 6;
    else if (variable is $PyString || variable is String)
        return 7;
    else if (variable is $PyTuple)
        return 8;
    else
        return -1;
}

$checkValue(i) {
    switch($getType(i)) {
        case 0: return false;
        case 4:
        case 5:
            if (i != 0)
                return true;
            break;
        case 6:
            if (i != "")
                return true;
            break;
        case 2:
            if (i.length != 0)
                return true;
            break;
        case 1:
            if (i.value == true)
                return true;
            break;
        case 2:
            var keys = i.keys();
            if (keys.length != 0)
                return true;
            break;
    }
    return false;
}

$and(list) {
    var item;
    for (int i = 0; i < list.length - 1; i++) {
        item = list[i];
        if (!$checkValue(item)) {
            if (list[i] == null)
                return "None";
            return item;
        }
    }
    return list.last;
}

$or(list) {
    for (int i = 0; i < list.length; i++) {
        if ($checkValue(list[i]))
            return list[i];
    }
    if (list[list.length - 1] == null)
        return "None";
    return list.last;
}

$generator(var function) => function();
$pow(base, exp) => pow(base.value, exp.value);

max(values) {
    values.sort();
    return values.last;
}

min(values) {
    values.sort();
    return values.first;
}

class $Range extends Object with IterableMixin<int> {
    int start, stop, step;

    $Range(this.start, [this.stop, this.step]) {
        if (stop == null) {
            stop = start.value;
            start = new $PyNum(0);
        }
        else
            stop = stop.value;

        if (step == null)
            step = new $PyNum(1);

        start = start.value;
        step = step.value;

        if (step == 0)
            throw new ArgumentError("step must not be 0");
    }

    Iterator<int> get iterator {
        return new $RangeIterator(start, stop, step);
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

    String toString() => step == 1 ? "xrange($start, $stop)" : "xrange($start, $stop, $step)";

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

    toList() {
        var l = new $PyList([]);
        for (var e in this)
            l.append(e);
        return l;
    }

    bool operator == (Range other) {
        return (other != null && start == other.start && stop == other.stop && step == other.step);
    }
}

class $RangeIterator implements Iterator<int> {
    var _pos;
    final _stop, _step;

    $RangeIterator(pos, stop, step) : _stop = stop, _pos = pos - step, _step = step;
    get current => new $PyNum(_pos);

    bool moveNext() {
        if (_step > 0  ? _pos + _step> _stop - 1 : _pos + _step < _stop + 1)
            return false;

        _pos += _step;
        return true;
    }
}

range(start_inclusive, [stop_exclusive, step]) => new $Range(start_inclusive, stop_exclusive, step).toList();
xrange(start_inclusive, [stop_exclusive, step]) => new $Range(start_inclusive, stop_exclusive, step);
indices(lengthable) => new $Range(0, lengthable.length);