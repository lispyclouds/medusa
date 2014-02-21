library formatted;

import "inbuilts.dart";
import "sprintf.dart";

$getFormattedString(string, collection) {
    if(collection is TupleClass){
        RegExp exp = new RegExp(r"%\s?[diuoxXeEfFgGcrs]");
        Iterable<Match> matches = exp.allMatches(string);
        var i = 0;
        var List = collection.getList();
        for(var m in matches) {
            String match = m.group(0);
            if(match == "%s" || match == "% s")
                List[i] = List[i].toString();
            if((match == "%d" || match == "% d") && List[i] is bool){
                if(List[i])
                    List[i] = 1;
                else
                    List[i] = 0;
            }
            i++;
        }
        return sprintf(string, List);
    } else if(collection is Map) {
        RegExp exp = new RegExp(r"%(\([a-zA-Z_]+\))*\s?[diuoxXeEfFgGcrs]");
        var List = [];
        Iterable<Match> matches = exp.allMatches(string);
        var i = 0;
        var currentIndex = 0;
        var newString = "";
        var key = "";
        for(var m in matches){
            String match = m.group(0);
            while(currentIndex <= m.start)
                newString += string[currentIndex++];

            currentIndex = m.start + 2;
            while(string[currentIndex] != ")")
                key += string[currentIndex++];

            currentIndex = m.end - 1;
            if(string[currentIndex] == "s")
                List.add(collection[key].toString());
            else if(string[currentIndex] == "d" && collection[key] is bool){
                if(collection[key])
                    List.add(1);
                else
                    List.add(0);
            }
            else
                List.add(collection[key]);
            key = "";
            newString += string[currentIndex++];
        }
        return sprintf(newString, List);
    }
}

$withFormat(string, list, dictionary) {
    RegExp exp = new RegExp(r"{\d+}|{[a-zA-Z0-9_]+}");
    Iterable<Match> matches = exp.allMatches(string);
    var i = 0;
    var currentIndex = 0;
    var newString = "";
    var key;
    for(var m in matches){
        String match = m.group(0);
        key = "";
        while(currentIndex < m.start)
            newString += string[currentIndex++];

        currentIndex++;
        while(string[currentIndex] != "}")
            key += string[currentIndex++];

        exp = new RegExp(r"{\d+}");
        if(exp.hasMatch(match))
            newString += list[int.parse(key)].toString();
        else
            newString += dictionary[key].toString();

        currentIndex = m.end;
    }
    return newString;
}