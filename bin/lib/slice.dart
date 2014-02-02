library slice;

import "dart:collection";

slice(list, lower, higher, step) {
    var c = [];
    var i = 0;

    if (higher < 0)
        higher = list.length + higher;

    if (lower < 0)
        lower = list.length + lower;

    if (step < 0) {
        for (i = lower; i > higher; i += step)
            c.add(list[i]);
    } else {
        for(i = lower; i < higher; i += step)
            c.add(list[i]);
    }

    return c;
}