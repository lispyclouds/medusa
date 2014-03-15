import "dart:math";
import "inbuilts.dart";

class $PyRandom {
    var _rng;

    $PyRandom([s]) {
        seed(s);
    }

    seed([value]) {
        if (value == null)
            _rng = new Random();
        else
            _rng = new Random(value);
    }

    randrange(start, [stop, step = 1]) {
        var space;

        if (stop == null)
            space = range(start);
        else if (step != 1)
            space = range(start, stop, step);
        else
            space = range(start, stop);

        return space.toList()[_rng.nextInt(space.length - 1)];
    }

    randint(a, b) => range(a, b).toList()[_rng.nextInt((b - a) - 1)];
    choice(seq) => seq[_rng.nextInt(seq.length - 1)];
    shuffle(x, [rand]) => x.shuffle();
    random() => _rng.nextDouble();
}

var random = new $PyRandom();
