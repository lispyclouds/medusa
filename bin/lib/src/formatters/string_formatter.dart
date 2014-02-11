part of sprintf;

class StringFormatter extends Formatter {
  String _arg;

  StringFormatter(this._arg, var fmt_type, var options) : super(fmt_type, options) {
    options['padding_char'] = ' ';
  }

  String asString() {
    String ret = _arg;

    if (options['precision'] > -1 && options['precision'] <= ret.length) {
      ret = ret.substring(0, options['precision']);
    }

    if (options['width'] > -1) {
      int diff = (options['width'] - ret.length);

      if (diff > 0) {
        String padding = Formatter.get_padding(diff, options['padding_char']);
        if (!options['left_align']) {
          ret = "${padding}${ret}";
        }
        else {
          ret = "${ret}${padding}";
        }
      }
    }
    return ret;
  }
}