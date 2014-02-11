part of sprintf;

class Formatter {

  var fmt_type;
  var options;

  Formatter(this.fmt_type, this.options);

  static String get_padding(int count, String pad) {
    String padding_piece = pad;
    StringBuffer padding = new StringBuffer();

    while (count > 0) {
      if ((count & 1) == 1) { padding.write(padding_piece); }
      count >>= 1;
      padding_piece = "${padding_piece}${padding_piece}";
    }

    return padding.toString();
  }
}
