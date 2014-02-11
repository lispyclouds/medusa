part of sprintf;

class IntFormatter extends Formatter {
  int _arg;
  static const int MAX_INT = 0xffffffffffffffff; // 64bit
  IntFormatter(this._arg, var fmt_type, var options) : super(fmt_type, options);

  String asString() {
    String ret = '';
    String prefix = '';

    int radix = fmt_type == 'x' ? 16 : (fmt_type == 'o' ? 8 : 10);

    if (_arg < 0) {
      _arg = _arg.abs();
      if (radix == 10) {
        options['sign'] = '-';
      }
      else {
        _arg = (MAX_INT - (_arg % MAX_INT) + 1) & MAX_INT;
      }
    }

    ret = _arg.toRadixString(radix);

    if (options['alternate_form']) {
      if (radix == 16 && _arg != 0) {
        prefix = "0x";
      }
      else if (radix == 8 && _arg != 0) {
        prefix = "0";
      }
      if (options['sign'] == '+' && radix != 10) {
        options['sign'] = '';
      }
    }

    // space "prefixes non-negative signed numbers with a space"
    if ((options['add_space'] && options['sign'] == '' && _arg > -1 && radix == 10)) {
      options['sign'] = ' ';
    }

    if (radix != 10) {
      options['sign'] = '';
    }

    String padding = '';
    var min_digits = options['precision'];
    var min_chars = options['width'];
    int num_length = ret.length;
    var sign_length = options['sign'].length;
    num str_len = 0;

    if (radix == 8 && min_chars <= min_digits) {
      num_length += prefix.length;
    }

    if (min_digits > num_length) {
      padding = Formatter.get_padding(min_digits - num_length, '0');
      ret = "${padding}${ret}";
      num_length = ret.length;
      padding = '';
    }

    str_len = num_length + sign_length + prefix.length;
    if (min_chars > str_len) {
      if (options['padding_char'] == '0' && !options['left_align']) {
        padding = Formatter.get_padding(min_chars - str_len, '0');
      }
      else {
        padding = Formatter.get_padding(min_chars - str_len, ' ');
      }
    }

    if (options['left_align']) {
      ret ="${options['sign']}${prefix}${ret}${padding}";
    }
    else if (options['padding_char'] == '0') {
      ret = "${options['sign']}${prefix}${padding}${ret}";
    }
    else {
      ret = "${padding}${options['sign']}${prefix}${ret}";
    }

    if (options['is_upper']) {
      ret = ret.toUpperCase();
    }

    return ret;
  }
}
