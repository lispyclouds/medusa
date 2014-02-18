#!/usr/bin/python

"""authors: heisenberg, apoorv, akashgiri"""

import ast, _ast, sys, re

imports = []
funVars = []
symTab = []
classes = []
inbuilts = ["input", "len", "open", "range", "raw_input", "str", "xrange"]

funMode = False
expCall = False
broken = False
func = ""

debug_notification = "**** Medusa Notification ****"
debug_error = "**** Medusa Warning ****"
debugging_message = "**** Medusa Debug ****"
debug_error = "**** Medusa Error ****"

operators = dict()
operators['_ast.Add'] = " + "
operators['_ast.Sub'] = " - "
operators['_ast.Mult'] = " * "
operators['_ast.Div'] = " ~/ "
operators['_ast.RShift'] = " >> "
operators['_ast.LShift'] = " << "
operators['_ast.BitAnd'] = " & "
operators['_ast.BitXor'] = " ^ "
operators['_ast.BitOr'] = " | "
operators['_ast.Mod'] = " % "
operators['_ast.Eq'] = " == "
operators['_ast.Gt'] = " > "
operators['_ast.GtE'] = " >= "
operators['_ast.Lt'] = " < "
operators['_ast.LtE'] = " <= "
operators['_ast.NotEq'] = " != "

exceptions = dict()
exceptions['IOError'] = "FileSystemException"
exceptions['Exception'] = "Exception"

outFile = open("out.dart", 'w')
code = " void main() {"

class MyParser(ast.NodeVisitor):
    def __init__(self):
        pass

    def parse(self, code):
        tree = ast.parse(code)
        self.visit(tree)

    def escape(self, s):
        s = s.replace('\\', '\\\\')
        s = s.replace('\n', r'\n')
        s = s.replace('\t', r'\t')
        s = s.replace('\r', r'\r')
        s = s.replace('$', '\$')

        return s

    def addImport(self, module):
        global imports

        if imports.__contains__(module) == False:
            imports.append(module)

    def parseUnOp(self, stmt_unop):
        parsed = ""

        if isinstance(stmt_unop.op, _ast.UAdd):
            parsed = "+"
        elif isinstance(stmt_unop.op, _ast.USub):
            parsed = "-"
        else:
            parsed = "~"

        if isinstance(stmt_unop.operand, _ast.Name):
            parsed += str(stmt_unop.operand.id)
        elif isinstance(stmt_unop.operand, _ast.Num):
            parsed += str(stmt_unop.operand.n)
        else:
            print debug_error, "Bad operand for unary operator"
            exit(1)

        return parsed

    def subscriptHandle(self, stmt_Subscript):
        if str(type(stmt_Subscript.slice))[13:-2] == "Index":
            if str(type(stmt_Subscript.value))[13:-2] == "Subscript":
                data = self.subscriptHandle(stmt_Subscript.value)
            elif str(type(stmt_Subscript.value))[13:-2] == "Name":
                data = str(stmt_Subscript.value.id)
            else:
                print debug_error
                print "type not supported yet => ", str(type(stmt_Subscript.value))
                exit(1)
            if str(type(stmt_Subscript.slice.value))[13:-2] == "Num":
                num = stmt_Subscript.slice.value.n
                if num < 0:
                    if str(type(stmt_Subscript.value))[13:-2] == "Subscript":
                        data += "[" + self.subscriptHandle(stmt_Subscript.value) + ".length " + str(num) +" ]"
                    elif str(type(stmt_Subscript.value))[13:-2] == "Name":
                        data += "[" + stmt_Subscript.value.id + ".length" + str(num) + "]"
                    else:
                        print debug_error
                        print "Type not supported => ", str(type(stmt_Subscript.value))
                        exit(1)
                else:
                    data += "[" + str(stmt_Subscript.slice.value.n) + "]"
            elif str(type(stmt_Subscript.slice.value))[13:-2] == "Name":
                data += "[" + stmt_Subscript.slice.value.id + "]"
            else:
                print debug_error
                print "Type not recognized => ", type(stmt_Subscript.slice.value)
                exit(1)
        elif str(type(stmt_Subscript.slice))[13:-2] == "Slice":
            self.addImport('lib/slice.dart')

            if str(type(stmt_Subscript.value))[13:-2] == "Subscript":
                data = "slice(" + self.subscriptHandle(stmt_Subscript.value) + ", "
            elif str(type(stmt_Subscript.value))[13:-2] == "Name":
                data = "slice(" + stmt_Subscript.value.id + ", "
            else:
                print debug_error
                print "type not supported yet => ", str(type(stmt_Subscript.value))
                exit(1)
            if isinstance(stmt_Subscript.slice.lower, _ast.Num):
                data += str(stmt_Subscript.slice.lower.n) + ", "
            elif stmt_Subscript.slice.lower == None:
                if stmt_Subscript.slice.step.n < 0:
                    if str(type(stmt_Subscript.value))[13:-2] == "Subscript":
                        data += self.subscriptHandle(stmt_Subscript.value) + ".length, "
                    elif str(type(stmt_Subscript.value))[13:-2] == "Name":
                        data += stmt_Subscript.value.id + ".length, "
                    else:
                        print debug_error
                        print "type not supported yet => ", str(type(stmt_Subscript.value))
                        exit(1)
                else:
                    data += "0, "
            else:
                print debug_error
                print "Type not recognized => ", type(stmt_Subscript.slice.lower)
                exit(1)
            if isinstance(stmt_Subscript.slice.upper, _ast.Num):
                data += str(stmt_Subscript.slice.upper.n) + ", "
            elif stmt_Subscript.slice.upper == None:
                if stmt_Subscript.slice.step.n > 0:
                    if str(type(stmt_Subscript.value))[13:-2] == "Subscript":
                        data += self.subscriptHandle(stmt_Subscript.value) + ".length, "
                    elif str(type(stmt_Subscript.value))[13:-2] == "Name":
                        data += stmt_Subscript.value.id + ".length, "
                    else:
                        print debug_error
                        print "type not supported yet => ", str(type(stmt_Subscript.value))
                        exit(1)
                else:
                    data += "0, "
            else:
                print debug_error
                print "Type not recognized => ", type(stmt_Subscript.slice.upper)
                exit(1)
            if isinstance(stmt_Subscript.slice.step, _ast.Num):
                data += str(stmt_Subscript.slice.step.n) + ")"
            elif stmt_Subscript.slice.step == None:
                data += "1)"
            else:
                print debug_error
                print "Type not recognized => ", type(stmt_Subscript.slice.upper)
                exit(1)
        else:
            print debug_error
            print "Type not recognized => ", type(stmt_Subscript.slice)
            exit(1)

        return data

    def attrHandle(self, stmt_call):
        resolved = ""
        myList = list()
        myDict = dict()

        if hasattr(stmt_call, "args"):
            if isinstance(stmt_call.func.value, _ast.Str) and stmt_call.func.attr == "format":
                for i in stmt_call.args:
                    if isinstance(i, _ast.Num):
                        myList.append(i.n)
                    elif isinstance(i, _ast.Name):
                        myList.append("$" + str(i.id))
                    elif isinstance(i, _ast.Str):
                        myList.append(i.s)
                    else:
                        print "Type not implemented => ", type(i)
                        exit(1)

                for i in stmt_call.keywords:
                    if isinstance(i.value, _ast.Num):
                        myDict[str(i.arg)] = i.value.n
                    elif isinstance(i.value, _ast.Name):
                        myDict[str(i.arg)] = "$" + str(i.value.id)
                    elif isinstance(i.value, _ast.Str):
                        myDict[str(i.arg)] = i.value.s
                    else:
                        print "Type not implemented => ", type(i.value)
                        exit(1)

                string = stmt_call.func.value.s
                indices = [(m.start(), m.end()) for m in re.finditer("{\d}|{[a-zA-Z0-9_]+}", string)]
                offset = 0
                for (start, end) in indices:
                    start += offset
                    end += offset
                    if string[start+1:end-1].isdigit():
                        offset += len(str(myList[int(string[start+1:end-1])])) - len(str(string[start:end]))
                        string = string.replace(string[start:end], str(myList[int(string[start+1:end-1])]))
                    else:
                        offset += len(str(myDict[string[start+1:end-1]])) - len(str(string[start:end]))
                        string = string.replace(string[start:end], str(myDict[string[start+1:end-1]]))

                return "\"" + string + "\""
            else:
                if stmt_call.func.value.id == "self":
                    obj = " this"
                else:
                    obj = stmt_call.func.value.id

            resolved += " " + obj + "." + stmt_call.func.attr + "("

            alen = len(stmt_call.args)
            i = 0

            while (i < alen):
                resolved += self.reducto(stmt_call.args[i])

                if (i + 1) < alen:
                    resolved += ", "
                i += 1

            resolved += ")"

        else:
            if stmt_call.value.id == "self":
                obj = "this"
            else:
                obj = stmt_call.value.id

            resolved = " " + obj + "." + stmt_call.attr

        return resolved

    def parseList(self, theList, formats = None):
        global func, expCall
        strList = "["
        i = 0
        l = len(theList)

        while i < l:
            if formats is not None and formats[i] == "%s":
                strList += "(" + self.reducto(theList[i], True) + ").toString()"
            else:
                strList += self.reducto(theList[i], True)
            if (i + 1) < l:
                strList += ", "
            i += 1

        strList += "]"
        return strList

    def parseExp(self, expr):
        global expCall, func
        powFlag = False
        leftString = False
        formatString = False

        exp = ""
        myDict = dict()

        if isinstance(expr.left, _ast.Call):
            expCall = True
            self.visit_Call(expr.left, True)
            expCall = False
            exp += func
            func = ""
        else:
            if isinstance(expr.left, _ast.BinOp):
                exp += self.parseExp(expr.left)
            else:
                exp = self.reducto(expr.left)

                if isinstance(expr.left, _ast.Str):
                    leftString = True

        op = str(type(expr.op))[8:-2]

        if leftString is True and op == "_ast.Mod":
            self.addImport("lib/sprintf.dart")

            if not isinstance(expr.right, _ast.Dict):
                exp = "sprintf(" + exp + ","
            else:
                exp = "sprintf("

            formatString = True
        else:
            if op in operators:
                exp += operators[op]
            elif isinstance(expr.op, _ast.Pow):
                self.addImport('dart:math')
                exp = "pow(" + exp
                exp += ", "
                powFlag = True
            else:
                print debug_warning
                print "Operator not implemented => " + op
                exit(1)

        if isinstance(expr.right, _ast.Call):
            expCall = True
            self.visit_Call(expr.right, True)
            expCall = False
            exp += func
            func = ""
        else:
            if isinstance(expr.right, _ast.BinOp):
                if formatString is True:
                    data = self.parseExp(expr.right)
                    exp += " [(" + data + ").toString()])"
                else:
                    exp += self.parseExp(expr.right)
            else:
                if isinstance(expr.right, _ast.Num):
                    if formatString is False:
                        exp += str(expr.right.n)
                    else:
                        exp += " [\"" + str(expr.right.n) + "\"])"
                elif isinstance(expr.right, _ast.Name):
                    if formatString is False:
                        exp += str(expr.right.id)
                    else:
                        exp += " [" + str(expr.right.id) + ".toString()])"
                elif isinstance(expr.right, _ast.Str):
                    if formatString is False:
                        exp += "'" + self.escape(expr.right.s) + "'"
                    else:
                        exp += " ['" + self.escape(expr.right.s) + "'])"
                elif isinstance(expr.right, _ast.Attribute):
                    exp += self.attrHandle(expr.right)
                elif isinstance(expr.right, _ast.Tuple):
                    if formatString is True:
                        string = str(expr.left.s)
                        formats = [string[m.start():m.end()] for m in re.finditer("%\s?[diuoxXeEfFgGcrs]", string)]
                        exp += self.parseList(expr.right.elts, formats) + ")"
                    else:
                        exp += self.parseList(expr.right.elts) + ")"
                elif isinstance(expr.right, _ast.UnaryOp):
                    exp += self.parseUnOp(expr.right)
                elif isinstance(expr.right, _ast.Dict):
                    key = list()
                    values = list()
                    for k in expr.right.keys:
                        if isinstance(k, _ast.Str):
                            key.append(k.s)
                        else:
                            "type not implemented => ", type(k)

                    for v in expr.right.values:
                        values.append(self.reducto(v))

                    myDict = dict(zip(key, values))
                    string = str(expr.left.s)
                    indices = [(m.start(), m.end()) for m in re.finditer("%(\([a-zA-Z_]+\))*\s?[diuoxXeEfFgGcrs]", string)]
                    myList = list()
                    offset = 0

                    for (start, end) in indices:
                        space = 0
                        start += offset
                        end += offset
                        if string[start:end][-2] == " ":
                            space = 1
                        if string[start + 2 : end - 2 - space]  not in ("", " "):
                            if string[start:end][-1] == "s":
                                myList.append(str(myDict[string[start + 2 : end - 2 - space]]))
                            else:
                                myList.append(myDict[string[start + 2 : end - 2 - space]])
                        offset = -len(string[start+1:end-1])
                        string = string.replace(string[start+1:end-1], "")

                    formats = [string[m.start():m.end()] for m in re.finditer("%[diuoxXeEfFgGcrs]", string)]
                    i = 0

                    while i < len(formats):
                        if formats[i] == "%s":
                            myList[i] = "(" + myList[i] + ").toString()"
                        i += 1

                    exp += "\"" + string + "\", ["
                    i = 0

                    while i < len(myList):
                        if i == len(myList) - 1:
                            exp += str(myList[i])
                        else:
                            exp += str(myList[i]) + ", "
                        i += 1
                    exp += "])"
                else:
                    print "Type still not implemented => ", str(type(expr.right))
                    exit(1)
        if powFlag:
            exp += ")"

        return "(" + exp + ")" #Saxx

    def reducto(self, target, exp = False):
        global func

        reduced = ""

        if isinstance(target, _ast.Num):
            reduced = str(target.n)
        elif isinstance(target, _ast.Str):
            reduced = "'" + self.escape(target.s) + "'"
        elif isinstance(target, _ast.List):
            reduced = self.parseList(target.elts)
        elif isinstance(target, _ast.Name):
            if target.id == "False" or "True":
                reduced = target.id.lower()
            else:
                reduced = target.id
        elif isinstance(target, _ast.UnaryOp):
            reduced = self.parseUnOp(target)
        elif isinstance(target, _ast.BinOp):
            reduced = self.parseExp(target)
        elif isinstance(target, _ast.Subscript):
            reduced = self.subscriptHandle(target)
        elif isinstance(target, _ast.Attribute):
            reduced = self.attrHandle(target)
        elif isinstance(target, _ast.IfExp):
            self.parseTernary(target)
        elif isinstance(target, _ast.Call):
            if exp:
                expCall = True
                self.visit_Call(target, True)
                expCall = False
                reduced = func
                func = ""
            else:
                self.visit_Call(target, True)
        else:
            print debug_error
            print "Type not recognized => ", str(type(target))
            exit(1)

        return str(reduced)

    def makeTest(self, stmt_test):
        global code

        if hasattr(stmt_test, 'left'):
            varType = str(type(stmt_test.left))[13:-2]

            if varType == "Name":
                if stmt_test.left.id == 'True':
                    code += "true"
                elif stmt_test.left.id == 'False':
                    code += "false"
                else:
                    code += stmt_test.left.id
            elif varType == "Str":
                code += stmt_test.left.s
            elif varType == "Num":
                code += str(stmt_test.left.n)
            elif varType == "BinOp":
                code += self.parseExp(stmt_test.left)
            else:
                print debug_error
                print "Type not recognized => ", varType
                exit(1)
        else:
            if stmt_test.id == "True":
                code += "true"
            elif stmt_test.id == "False":
                code += "false"

        if hasattr(stmt_test, 'ops'):
            code += operators[str(type(stmt_test.ops[0]))[8:-2]]

        if hasattr(stmt_test, 'comparators'):
            varType = str(type(stmt_test.comparators[0]))[13:-2]
            if varType == "Name":
                if stmt_test.comparators[0].id == 'True':
                    code += "true"
                elif stmt_test.comparators[0].id == 'False':
                    code += "false"
                else:
                    code += stmt_test.comparators[0].id
            elif varType == "Str":
                code += stmt_test.comparators[0].s
            elif varType == "Num":
                code += str(stmt_test.comparators[0].n)
            elif varType == "BinOp":
                code += self.parseExp(stmt_test.comparators[0])
            else:
                print debug_error
                print "Type not recognized => ", varType
                exit(1)

    def parseTernary(self, stmt_ternary):
        global code

        self.makeTest(stmt_ternary.test)
        code += " ? " + self.reducto(stmt_ternary.body) + " : " + self.reducto(stmt_ternary.orelse)

    def visit_Print(self, stmt_print):
        global code

        self.addImport("dart:io")

        i = 0
        values = len(stmt_print.values)
        while (i < values):
            if (i + 1) < values:
                code += " stdout.write("
            else:
                code += " stdout.writeln("

            printee = self.reducto(stmt_print.values[i])

            if printee != "":
                code += printee
            code += ");"

            if (i + 1) < values:
                code += " stdout.write(' ');"

            i += 1

    def visit_Assign(self, stmt_assign):
        global code, funVars, funMode

        for target in stmt_assign.targets:
            if isinstance(target, _ast.Attribute):
                code += self.attrHandle(target) + " = "
            else:
                if funMode:
                    if not symTab.__contains__(target.id):
                        if not funVars.__contains__(target.id):
                            funVars.append(target.id)
                            code += " var"
                else:
                    if not symTab.__contains__(target.id):
                        symTab.append(target.id)

                code += " " + target.id + " = ";

            value = self.reducto(stmt_assign.value)

            if value != "":
                 code += value
            code += ";"

    def visit_If(self, stmt_if):
        global code, funMode

        funMode = True

        code += " if ("
        self.makeTest(stmt_if.test)
        code += ") {"

        for node in stmt_if.body:
            self.visit(node)

        code += " }"
        if len(stmt_if.orelse) > 0:
            code += " else {"
            for node in stmt_if.orelse:
                self.visit(node)
            code += " }"

        funMode = False

    def visit_For(self, stmt_For):
        global code, broken, funMode

        funMode = True
        broken = True
        code += " var def = false;"
        code += " for (var " + stmt_For.target.id + " in "

        if isinstance(stmt_For.iter, _ast.Call):
            self.visit_Call(stmt_For.iter, True)
        elif isinstance(stmt_For.iter, _ast.Name):
            code += stmt_For.iter.id
        else:
            print "This type of for loop not yet handled"
            exit(1)

        code += " ) {"

        for node in stmt_For.body:
            self.visit(node)

        code += "}"


        if len(stmt_For.orelse) > 0:
            code += "if(def == false){"
            for node in stmt_For.orelse:
                self.visit(node)

            code += "}"

        broken = False
        funMode = False

    def visit_While(self, stmt_while):
        global code

        funMode = True

        code += " while ("
        self.makeTest(stmt_while.test)
        code += ") {"

        for node in stmt_while.body:
            self.visit(node)

        code += "}"

        code += " if(!("
        self.makeTest(stmt_while.test)
        code += ")) {"

        for node in stmt_while.orelse:
            self.visit(node)

        code += "}"

        funMode = False

    def visit_AugAssign(self, stmt_aug_assign):
        global code
        powFlag = False

        if isinstance(stmt_aug_assign.target, _ast.Attribute):
            code += self.attrHandle(stmt_aug_assign.target)
        else:
            code += " " + stmt_aug_assign.target.id

        op = str(type(stmt_aug_assign.op))[8:-2]
        if op in operators:
            code += " " + operators[op].strip() + "= "
        elif isinstance(stmt_aug_assign.op, _ast.Pow):
            self.addImport('dart:math')
            code += " = pow("
            code += stmt_aug_assign.target.id
            code += ", "
            powFlag = True
        else:
            print debug_error
            print "Operator not implemented => " + op
            exit(1)

        code += self.reducto(stmt_aug_assign.value)

        if powFlag:
            code += ")"

        code += ";"

    def visit_FunctionDef(self, stmt_function):
        global code, funVars, funMode

        temp = code
        code = ""
        funMode = True

        if stmt_function.name == "__init__":
            code = " " + classes[-1] + "("
        else:
            code = " " + stmt_function.name + "("

        i = 0
        alen = len(stmt_function.args.args)
        while i < alen:
            if str(stmt_function.args.args[i].id) == "self":
                i += 1
                continue

            code += stmt_function.args.args[i].id
            funVars.append(stmt_function.args.args[i].id)

            if (i + 1) < alen:
                code += ", "
            i += 1
        code += ") {"

        for node in stmt_function.body:
            self.visit(node)

        funMode = False
        code += " }"
        funVars = []

        code = code + temp

    def visit_Call(self, stmt_call, myVar = False):
        global code, expCall, func, classes, inbuilts

        if isinstance(stmt_call.func, _ast.Attribute):
            if expCall:
                func += self.attrHandle(stmt_call)
            else:
                code += self.attrHandle(stmt_call)

            if myVar == False:
                if expCall:
                    func += ";"
                else:
                    code += ";"
            return

        if stmt_call.func.id in inbuilts:
            self.addImport("lib/inbuilts.dart")

        if classes.__contains__(stmt_call.func.id):
            if expCall:
                func += "new"
            else:
                code += "new"

        if expCall:
            func += " " + stmt_call.func.id + "("
        else:
            code += " " + stmt_call.func.id + "("

        alen = len(stmt_call.args)
        i = 0
        p = ""

        while i < alen:
            p = self.reducto(stmt_call.args[i])

            if p != "":
                if expCall:
                    func += p
                else:
                    code += p

            if (i + 1) < alen:
                if expCall:
                    func += ", "
                else:
                    code += ", "
            i += 1

        if expCall:
            func += ")"
        else:
            code += ")"

        if myVar == False:
            code += ";"

    def visit_Return(self, stmt_return):
        global code

        code += " return "
        v = ""

        if isinstance(stmt_return.value, _ast.Name):
            if stmt_return.value.id == "self":
                v = "this"
            else:
                v = stmt_return.value.id
        else:
            v = self.reducto(stmt_return.value)

        if v != "":
            code += v
        code += ";"

    def visit_ClassDef(self, stmt_class):
        global code, funMode

        main = code
        code = ""
        funMode = True

        code = " class " + stmt_class.name
        if classes.__contains__(stmt_class.name) == False:
            classes.append(stmt_class.name)

        if len(stmt_class.bases) == 1:
            code += " extends " + str(stmt_class.bases[0].id)
        elif len(stmt_class.bases) > 1:
            print "Multiple Inheritace is unsupported at the moment :( Sorry!"
            exit(1)
        code += " {"

        temp = code
        code = ""

        for node in stmt_class.body:
            self.visit(node)

        code = temp + code + " }" + main
        funMode = False
        funVars = []

    def visit_Raise(self, stmt_raise):
        global code

        code += " throw " + self.reducto(stmt_raise.type) + ";"

    def visit_TryExcept(self, stmt_tryexcept, final = False):
        global code, funMode, funVars

        funMode = True

        if not final:
            nodes = stmt_tryexcept
        else:
            nodes = stmt_tryexcept[0]

        code += " var from = true; try {"
        for node in nodes.body:
            self.visit(node)
        code += " }"

        for handler in nodes.handlers:
            if handler.type.id == "ZeroDivisionError":
                continue

            code += " on " + exceptions[handler.type.id]
            if isinstance(handler.name, _ast.Name):
                code += " catch(" + handler.name.id + ")"
                funVars.append(handler.name.id)

            code += " { from = false;"
            for node in handler.body:
                self.visit(node)
            code += " }"

        if not final and len(nodes.orelse) > 0:
            code += " if (from == true) {"
            for node in nodes.orelse:
                self.visit(node)
            code += " }"

        funMode = False

    def visit_TryFinally(self, stmt_tryfinally):
        global code

        self.visit_TryExcept(stmt_tryfinally.body, True)

        code += " finally {"
        for node in stmt_tryfinally.finalbody:
            self.visit(node)
        code += " }"

        if len(stmt_tryfinally.body[0].orelse) > 0:
            code += " if (from == true) {"
            for node in stmt_tryfinally.body[0].orelse:
                self.visit(node)
            code += " }"

    def visit_Break(self, stmt_break):
        global code, broken
        if broken:
            code += " def = true; break;"
        else:
            code += "break;"

MyParser().parse(open(sys.argv[1]).read())

code += " }"

if len(symTab) > 0:
    code = " var " + ", ".join(symTab) + ";" + code

impStr = ""
for imp in imports:
    impStr += "import '" + imp + "'; "
code = impStr.strip() + code

outFile.write(code)
outFile.close()