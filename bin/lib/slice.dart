library slice;

import "dart:collection";
import "dart:mirrors";

$slice(list, lower, higher, step) {
    var c = [];
    var i = 0;

    lower = lower.value();
    higher = higher.value();
    step = step.value();

    if (higher < 0)
        higher = list.length.value() + higher;

    if (lower < 0)
        lower = list.length.value() + lower;

    if (lower > list.length.value() - 1)
        lower = list.length.value() - 1;

    if (higher > list.length.value() - 1)
        higher = list.length.value() - 1;

    if (step < 0) {
        for (i = lower; i >= higher; i += step)
            c.add(list[i]);
    } else {
        for (i = lower; i < higher; i += step)
            c.add(list[i]);
    }

    return c;
}