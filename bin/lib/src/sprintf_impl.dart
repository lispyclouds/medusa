part of sprintf;

typedef PrintFormatFormatter(arg, options);

class PrintFormat {
  static final RegExp specifier = new RegExp(r'%(?:(\d+)\$)?([\+\-\#0 ]*)(\d+|\*)?(?:\.(\d+|\*))?([a-z%])', caseSensitive : false);
  static final RegExp uppercase_rx = new RegExp(r'[A-Z]', caseSensitive: true);

  var _formatters = {
    'i' : (arg, options) => new IntFormatter(arg, 'i', options),
    'd' : (arg, options) => new IntFormatter(arg, 'd', options),
    'x' : (arg, options) => new IntFormatter(arg, 'x', options),
    'X' : (arg, options) => new IntFormatter(arg, 'x', options),
    'o' : (arg, options) => new IntFormatter(arg, 'o', options),
    'O' : (arg, options) => new IntFormatter(arg, 'o', options),

    'e' : (arg, options) => new FloatFormatter(arg, 'e', options),
    'E' : (arg, options) => new FloatFormatter(arg, 'e', options),
    'f' : (arg, options) => new FloatFormatter(arg, 'f', options),
    'F' : (arg, options) => new FloatFormatter(arg, 'f', options),
    'g' : (arg, options) => new FloatFormatter(arg, 'g', options),
    'G' : (arg, options) => new FloatFormatter(arg, 'g', options),

    's' : (arg, options) => new StringFormatter(arg, 's', options),
  };

  String call(String fmt, var args) {
    String ret = '';


    int offset = 0;
    int arg_offset = 0;

    if (args is! List) {
      throw new ArgumentError('Expecting list as second argument');
    }

    for (Match m in specifier.allMatches(fmt)) {
      String _parameter = m[1];
      String _flags = m[2];
      String _width = m[3];
      String _precision = m[4];
      String _type = m[5];

      String _arg_str = '';
      Map _options = {
        'is_upper' : false,
        'width' : -1,
        'precision' : -1,
        'length' : -1,
        'radix' : 10,
        'sign' : '',
        'specifier_type' : _type,
      };

      _parse_flags(_flags).forEach((var K, var V) { _options[K] = V; });

      // The argument we want to deal with
      var _arg = _parameter == null ? null : args[int.parse(_parameter)];

      // parse width
      if (_width != null) {
        _options['width'] = (_width == '*' ? args[arg_offset++] : int.parse(_width));
      }

      // parse precision
      if (_precision != null) {
        _options['precision'] = (_precision == '*' ? args[arg_offset++] : int.parse(_precision));
      }

      // grab the argument we'll be dealing with
      if (_arg == null && _type != '%') {
        _arg = args[arg_offset++];
      }

      _options['is_upper'] = uppercase_rx.hasMatch(_type);

      if (_type == '%') {
        if (_flags.length > 0 || _width != null || _precision != null) {
          throw new Exception('"%" does not take any flags');
        }
        _arg_str = '%';
      }
      else if (this._formatters.containsKey(_type)) {
        _arg_str = _formatters[_type](_arg, _options).asString();
      }
      else {
        throw new ArgumentError("Unknown format type ${_type}");
      }

      // Add the pre-format string to the return
      ret += fmt.substring(offset, m.start);
      offset = m.end;

      ret += _arg_str;
    }

    return ret += fmt.substring(offset);
  }

  register_specifier(String specifier, PrintFormatFormatter formatter) {
    this._formatters[specifier] = formatter;
  }

  unregistier_specifier(String specifier) {
    this._formatters.remove(specifier);
  }

  Map _parse_flags(String flags) {
    return {
      'sign' : flags.indexOf('+') > -1 ? '+' : '',
      'padding_char' : flags.indexOf('0') > -1 ? '0' : ' ',
      'add_space' : flags.indexOf(' ') > -1,
      'left_align' : flags.indexOf('-') > -1,
      'alternate_form' : flags.indexOf('#') > -1,
    };
  }
}
