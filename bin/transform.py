#!/usr/bin/python

import ast, _ast, sys

imports = []
functions = []
symTab = []

#Testing Git
#sample comment

debug_notification = "**** Medusa Notification ****"
debug_warning = "**** Medusa Warning ****"
debugging_message = "**** Medusa Debug ****"
debug_error = "**** Medusa Error ****"

operators = dict()
operators['_ast.Eq'] = "=="
operators['_ast.Gt'] = ">"
operators['_ast.GtE'] = ">="
operators['_ast.Lt'] = "<"
operators['_ast.LtE'] = "<="
operators['_ast.NotEq'] = "!="

outFile = open("out.dart", 'w')
code = "void main() {"

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

        return s

    def parseList(self, theList):
        strList = "["
        i = 0
        l = len(theList)

        while i < l:
            item = theList[i]

            if isinstance(item, _ast.Num):
                v = item.n
            elif isinstance(item, _ast.Name):
                v = item.id
            elif isinstance(item, _ast.Str):
                v = "'" + item.s + "'"
            elif isinstance(item, _ast.List):
                v = self.parseList(item.elts)
            elif isinstance(item, _ast.BinOp):
                v = self.parseExp(item)

            strList += str(v)
            if (i + 1) < l:
                strList += ", "
            i += 1

        strList += "]"
        return strList

    def parseExp(self, expr):
        exp = ""

        if isinstance(expr.left, _ast.BinOp):
            exp += self.parseExp(expr.left)
        else:
            if hasattr(expr.left, 'n'):
                exp += str(expr.left.n)
            else:
                exp += str(expr.left.id)

        if isinstance(expr.op, _ast.Add):
            exp += " + "
        elif isinstance(expr.op, _ast.Sub):
            exp += " - "
        elif isinstance(expr.op, _ast.Mult):
            exp += " * "
        else:
            exp += " / "

        if isinstance(expr.right, _ast.BinOp):
            exp += self.parseExp(expr.right)
        else:
            if hasattr(expr.right, 'n'):
                exp += str(expr.right.n)
            else:
                exp += str(expr.right.id)

        return "(" + exp + ")" #Saxx

    def visit_Print(self, stmt_print):
        global code

        if imports.__contains__("dart:io") == False:
            imports.append("dart:io")

        data = ""
        i = 0
        values = len(stmt_print.values)
        while (i < values):
            code += " stdout.write("

            if isinstance(stmt_print.values[i], _ast.Str):
                data = "'" + self.escape(stmt_print.values[i].s) + "'"
            elif isinstance(stmt_print.values[i], _ast.Num):
                data = stmt_print.values[i].n
            elif isinstance(stmt_print.values[i], _ast.Name):
                data = stmt_print.values[i].id
            elif isinstance(stmt_print.values[i], _ast.List):
                data = self.parseList(stmt_print.values[i].elts)
            elif isinstance(stmt_print.values[i], _ast.BinOp):
                data = self.parseExp(stmt_print.values[i])

            code += str(data) + ");"
            if (i + 1) < values:
                code += " stdout.write(' ');"
            else:
                code += " stdout.write('\\n');";
            i += 1

    def visit_Assign(self, stmt_assign):
        global code

        for target in stmt_assign.targets:
            if symTab.__contains__(target.id) == False:
                symTab.append(target.id)
                code += " var"

            if isinstance(stmt_assign.value, _ast.Num):
                value = stmt_assign.value.n
            elif isinstance(stmt_assign.value, _ast.Str):
                value = "'" + stmt_assign.value.s + "'"
            elif isinstance(stmt_assign.value, _ast.List):
                value = self.parseList(stmt_assign.value.elts)
            elif isinstance(stmt_assign.value, _ast.Name):
                value = stmt_assign.value.id
            elif isinstance(stmt_assign.value, _ast.BinOp):
                value = self.parseExp(stmt_assign.value)

            code += " " + target.id + " = " + str(value) + ";"

    def visit_If(self, stmt_If):
        global code

        code += "if("
        varType = str(type(stmt_If.test.left))[13:-2]

        if varType == "Name":
            if stmt_If.test.left.id == 'True':
                code += "true"
            elif stmt_If.test.left.id == 'False':
                code += "false"
            else:
                code += stmt_If.test.left.id
        elif varType == "Str":
            code += stmt_If.test.left.s
        elif varType == "Num":
            code += str(stmt_If.test.left.n)
        else:
            print debug_warning
            print "Type not recognized => ", varType

        code += operators[str(type(stmt_If.test.ops[0]))[8:-2]]
        varType = str(type(stmt_If.test.comparators[0]))[13:-2]

        if varType == "Name":
            if stmt_If.test.comparators[0].id == 'True':
                code += "true"
            elif stmt_If.test.comparators[0].id == 'False':
                code += "false"
            else:
                code += stmt_If.test.comparators[0].id
        elif varType == "Str":
            code += stmt_If.test.comparators[0].s
        elif varType == "Num":
            code += str(stmt_If.test.comparators[0].n)
        else:
            print debug_warning
            print "Type not recognized => ", varType

        code += ") {"
        for node in stmt_If.body:
            self.visit(node)

        code += "}"
        if len(stmt_If.orelse) > 0:
            code += " else {"
            for node in stmt_If.orelse:
                self.visit(node)
            code += "}"

MyParser().parse(open(sys.argv[1]).read())

code += " }"

for imp in imports:
    code = "import '" + imp + "'; " + code

for func in functions:
    code = func + code

outFile.write(code)
outFile.close()