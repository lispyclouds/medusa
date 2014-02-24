""" Fast Python Transform by heisenberg, apoorv, akashgiri """

import ast, _ast, sys, re

dartImports = []
dartLocalVars = []
dartClassVars = []
dartGlobalVars = []

pyGlobalVars = []
pyClasses = []
pyInbuilts = ["abs", "all", "any", "bin", "input", "len", "open", "range", "raw_input", "str", "xrange"]

parsedClasses = []
parsedFunctions = []
parsedCode = []

classyMode = False
funMode = False
broken = False
formats = False
fromTest = False
parsedType = ""

exceptions = dict()
exceptions['Exception'] = "Exception"
exceptions['IOError'] = "FileSystemException"
exceptions['ZeroDivisionError'] = "IntegerDivisionByZeroException"

class PyParser(ast.NodeVisitor):
    def parse(self, code):
        tree = ast.parse(code)
        self.visit(tree)

    def escape(self, s):
        s = s.replace('\\', '\\\\')
        s = s.replace('\n', r'\n')
        s = s.replace('\t', r'\t')
        s = s.replace('\r', r'\r')
        s = s.replace('$', '\$')

        return  "'" + s + "'"

    def addImport(self, module):
        global dartImports

        if module not in dartImports:
            dartImports.append(module)

    def visit_Module(self, stmt_module):
        global parsedType, parsedClasses, parsedFunctions, parsedCode

        for node in stmt_module.body:
            parsed = self.visit(node)
            #print parsed
            if parsedType is "class":
                parsedClasses.append(parsed)
            elif parsedType is "function":
                parsedFunctions.append(parsed)
            elif parsedType is "code":
                parsedCode.append(parsed)
            else:
                print "Not Implemented => ", type(node)

    def visit_UAdd(self, stmt_uadd):
        return "+"

    def visit_USub(self, stmt_usub):
        return "-"

    def visit_Invert(self, stmt_invert):
        return "~"

    def visit_Name(self, stmt_name):
        global parsedType

        name = stmt_name.id

        if name is "False" or name is "True":
            name = name.lower()
        elif name is "self":
            name = "this"
        elif name is "None":
            name = "null"

        parsedType = "code"
        return str(name)

    def visit_Num(self, stmt_num):
        return str(stmt_num.n)

    def visit_Str(self, stmt_str):
        self.addImport("lib/inbuilts.dart")
        return "new $PyString(" + self.escape(stmt_str.s) + ")"

    def visit_Add(self, stmt_add):
        return "+"

    def visit_Sub(self, stmt_sub):
        return "-"

    def visit_Mult(self, stmt_mult):
        return "*"

    def visit_Div(self, stmt_div):
        return "~/"

    def visit_Pow(self, stmt_pow):
        self.addImport('dart:math')
        return ","

    def visit_RShift(self, stmt_rshift):
        return ">>"

    def visit_LShift(self, stmt_lshift):
        return "<<"

    def visit_BitAnd(self, stmt_bitand):
        return "&"

    def visit_BitXor(self, stmt_bitxor):
        return "^"

    def visit_BitOr(self, stmt_bitor):
        return "|"

    def visit_Mod(self, stmt_mod):
        return "%"

    def visit_Eq(self, stmt_eq):
        return "=="

    def visit_Gt(self, stmt_gt):
        return ">"

    def visit_Lt(self, stmt_lt):
        return "<"

    def visit_GtE(self, stmt_gte):
        return ">="

    def visit_LtE(self, stmt_lte):
        return "<="

    def visit_NotEq(self, stmt_neq):
        return "!="

    def visit_And(self, stmt_and):
        return "$and(["

    def visit_Or(self, stmt_or):
        return "$or(["

    def visit_In(self, stmt_in):
        return ".contains"



    def visit_IfExp(self, stmt_ternary):
        global parsedType

        stmt = self.visit(stmt_ternary.test) + "?" + self.visit(stmt_ternary.body) + ":" + self.visit(stmt_ternary.orelse)

        parsedType = "code"
        return stmt

    def visit_UnaryOp(self, stmt_unop):
        global parsedType

        data = self.visit(stmt_unop.op) + self.visit(stmt_unop.operand)

        parsedType = "code"
        return data

    def visit_BinOp(self, stmt_binop):
        global parsedType

        left = self.visit(stmt_binop.left)
        op = self.visit(stmt_binop.op)
        right = self.visit(stmt_binop.right)
        exp = "(" + left + op + right + ")"

        if op == ",":
            exp = "(pow" + exp + ")"

        parsedType = "code"
        return exp

    def visit_BoolOp(self, stmt_boolop):
        global parsedType

        self.addImport('lib/inbuilts.dart');
        code = self.visit(stmt_boolop.op)
        alen = len(stmt_boolop.values)
        i = 0
        while i < alen:
            code += self.visit(stmt_boolop.values[i])
            if i < alen - 1:
                code += ","
            i += 1

        code += "])"

        if fromTest:
            code = "$checkValue(" + code + ")"

        parsedType = "code"
        return code

    def visit_List(self, stmt_list):
        global parsedType

        code = "["

        alen = len(stmt_list.elts)
        i = 0
        while i < alen:
            code += self.visit(stmt_list.elts[i])
            if i < alen - 1:
                code += ","
            i += 1

        code += "]"

        parsedType = "code"
        return code

    def visit_Dict(self, stmt_dict):
        global parsedType

        keyLen = len(stmt_dict.keys)
        valueLen = len(stmt_dict.values)
        code = "{"

        if keyLen == valueLen:
            i = 0
            while i < keyLen:
                code += self.visit(stmt_dict.keys[i]) + ":" + self.visit(stmt_dict.values[i])
                if i < keyLen - 1:
                    code += ","
                i += 1
            code += "}"

            parsedType = "code"
            return code
        else:
            print "Invalid Dictionary"
            exit(1)

    def visit_Tuple(self, stmt_tuple):
        global parsedType

        self.addImport('lib/inbuilts.dart')

        code = "tuple(["
        i = 0
        alen = len(stmt_tuple.elts)
        while i < alen:
            code += self.visit(stmt_tuple.elts[i])

            if (i + 1) < alen:
                code += ","
            i += 1
        code += "])"

        parsedType = "code"
        return code

    def visit_Subscript(self, stmt_Subscript):
        if isinstance(stmt_Subscript.slice, _ast.Slice):
            self.addImport('lib/slice.dart')
            listVar = self.visit(stmt_Subscript.value)
            lower = self.subsituteVisit(stmt_Subscript.slice.lower)
            upper = self.subsituteVisit(stmt_Subscript.slice.upper)
            step = self.subsituteVisit(stmt_Subscript.slice.step)
            step = 1 if step is None or step == "None" else int(step)
            lower = (str(listVar) + ".length," if step < 0 else "0,") if lower is None  else str(lower) + ","
            upper = (str(listVar) + ".length," if step > 0 else "0,") if upper is None  else str(upper) + ","
            data = "$slice(" + str(listVar) + "," + str(lower) + str(upper) + str(step) + ")"
            return data
        elif isinstance(stmt_Subscript.slice, _ast.Index):
            listVar = self.visit(stmt_Subscript.value)
            index = self.visit(stmt_Subscript.slice.value)
            index = (str(listVar) + ".length" + str(index)) if int(index) < 0 else index
            index = "[" + str(index) + "]"
            data = str(listVar) + index
            return data
        else:
            print "Unimplemented TYpe =>", type(stmt_Subscript.slice)
            exit(1)

    def subsituteVisit(self, node):
        if node is not None:
            return self.visit(node)
        else:
            return None

    def visit_Compare(self, stmt_test):
        global parsedType

        stmt = self.visit(stmt_test.left) + self.visit(stmt_test.ops[0]) + self.visit(stmt_test.comparators[0])

        parsedType = "code"
        return stmt

    def visit_ClassDef(self, stmt_class):
        global parsedType, dartLocalVars, dartClassVars, classyMode

        if stmt_class.name not in pyClasses:
            pyClasses.append(stmt_class.name)

        code = "class " + stmt_class.name
        if len(stmt_class.bases) == 1:
            if stmt_class.bases[0].id == "object":
                base = "Object"
            else:
                base = str(stmt_class.bases[0].id)
            code += " extends " + base
        elif len(stmt_class.bases) > 1:
            print "Multiple Inheritace is unsupported at the moment :( Sorry!"
            exit(1)
        code += "{"

        classyMode = True
        for node in stmt_class.body:
            code += self.visit(node)
        code += "}"
        classyMode = False
        dartClassVars = []

        parsedType = "class"
        return code

    def visit_Global(self, stmt_global):
        global dartLocalVars

        for name in stmt_global.names:
            dartLocalVars.append(name)

        return ""

    def visit_FunctionDef(self, stmt_function):
        global dartLocalVars, funMode, parsedType

        body = ""
        code = ""
        defs = ""

        funMode = True
        for node in stmt_function.body:
            body += self.visit(node)
        funMode = False

        if len(dartLocalVars) > 0:
            defs = "var " + ",".join(dartLocalVars) + ";"

        if stmt_function.name == "__init__":
            code = pyClasses[-1] + "(" + code
        else:
            code = stmt_function.name + "(" + code

        i = 0
        alen = len(stmt_function.args.args)
        while i < alen:
            if str(stmt_function.args.args[i].id) == "self":
                i += 1
                continue

            code += stmt_function.args.args[i].id
            dartLocalVars.append(stmt_function.args.args[i].id)

            if (i + 1) < alen:
                code += ","
            i += 1
        code += "){" + defs + body + "}"

        dartLocalVars = []
        parsedType = "function"
        return code

    def visit_Call(self, stmt_call):
        global pyClasses, pyInbuilts, forceCall, parsedType, formats

        code = self.visit(stmt_call.func)
        keyDict = {}

        if code in pyInbuilts:
            self.addImport("lib/inbuilts.dart")
        elif code in pyClasses:
            code = "new " + code

        alen = len(stmt_call.args)
        i = 0

        code += "([" if formats else "("
        while i < alen:
            code += self.visit(stmt_call.args[i])

            if (i + 1) < alen:
                code += ","
            i += 1
        code += "]" if formats else ")"

        for node in stmt_call.keywords:
            arg = node.arg
            value = self.visit(node.value)
            keyDict[arg] = value

        code += ("," + str(keyDict) + ")") if formats else ""

        formats = False
        parsedType = "code"
        return code

    def visit_Expr(self, stmt_expr):
        global parsedType

        parsedType = "code"
        return self.visit(stmt_expr.value) + ";"

    def visit_Return(self, stmt_return):
        global parsedType

        code = "return " + self.visit(stmt_return.value) + ";"

        parsedType = "code"
        return code

    def visit_Print(self, stmt_print):
        global parsedType

        self.addImport("dart:io")

        code = ""
        i = 0
        values = len(stmt_print.values)

        while (i < values):
            if (i + 1) < values:
                code += "stdout.write("
            else:
                code += "stdout.writeln("

            printee = self.visit(stmt_print.values[i])
            if printee is not None:
                code += printee
            code += ");"

            if (i + 1) < values:
                code += "stdout.write(' ');"
            i += 1

        parsedType = "code"
        return code

    def visit_Assign(self, stmt_assign):
        global dartLocalVars, funMode, parsedType, pyGlobalVars, classyMode

        code = ""
        for target in stmt_assign.targets:
            if isinstance(target, _ast.Attribute):
                code += self.visit(target) + "="
            else:
                if funMode and target.id not in dartLocalVars:
                    dartLocalVars.append(target.id)
                elif classyMode and target.id not in dartClassVars:
                    dartClassVars.append(target.id)
                    code += "var "
                else:
                    if target.id not in dartGlobalVars:
                        dartGlobalVars.append(target.id)

                code += target.id + "=";
            code += self.visit(stmt_assign.value)
        code += ";"

        parsedType = "code"
        return code

    def visit_AugAssign(self, stmt_aug_assign):
        global powFlag, parsedType

        left = self.visit(stmt_aug_assign.target)
        op = self.visit(stmt_aug_assign.op)
        right = self.visit(stmt_aug_assign.value)

        code = left
        if op == ",":
            code += "=pow(" + left + op + right + ")"
        else:
            code += op + "=" + right

        parsedType = "code"
        return code + ";"

    def visit_Break(self, stmt_break):
        global broken

        return "$broken=true;break;" if broken else "break;"

    def visit_If(self, stmt_if):
        global parsedType, fromTest

        fromTest = True
        code = "if(" + self.visit(stmt_if.test) + "){"
        for node in stmt_if.body:
            code += self.visit(node)
        code += "}"

        if len(stmt_if.orelse) > 0:
            code += "else{"
            for node in stmt_if.orelse:
                code += self.visit(node)
            code += "}"

        fromTest = False
        parsedType = "code"
        return code

    def visit_While(self, stmt_while):
        global parsedType

        code = "while(" + self.visit(stmt_while.test) + "){"
        for node in stmt_while.body:
            code += self.visit(node)
        code += "}"

        code += "if(!(" + self.visit(stmt_while.test) + ")){"
        for node in stmt_while.orelse:
            code += self.visit(node)
        code += "}"

        parsedType = "code"
        return code

    def visit_For(self, stmt_for):
        global broken, parsedType

        broken = True
        code = "var $broken=false;for(var " + stmt_for.target.id + " in " + self.visit(stmt_for.iter) + "){"
        for node in stmt_for.body:
            code += self.visit(node)
        code += "}"

        if len(stmt_for.orelse) > 0:
            code += "if($broken==false){"
            for node in stmt_for.orelse:
                code += self.visit(node)
            code += "}"
        broken = False

        parsedType = "code"
        return code

    def visit_Raise(self, stmt_raise):
        return "throw " + self.visit(stmt_raise.type) + ";"

    def visit_TryExcept(self, stmt_tryexcept, final = False):
        global dartLocalVars, parsedType

        if not final:
            nodes = stmt_tryexcept
        else:
            nodes = stmt_tryexcept[0]

        code = "var $tried=true;try{"
        for node in nodes.body:
            code += self.visit(node)
        code += "}"

        for handler in nodes.handlers:
            try:
                code += "on " + exceptions[handler.type.id]
                if isinstance(handler.name, _ast.Name):
                    code += " catch(" + handler.name.id + ")"
                    dartLocalVars.append(handler.name.id)

                code += "{$tried=false;"
                for node in handler.body:
                    code += self.visit(node)
                code += "}"
            except KeyError:
                print "Fatal Error: Exception handler not implemented for " + handler.type.id
                exit(1)

        if not final and len(nodes.orelse) > 0:
            code += "if($tried){"
            for node in nodes.orelse:
                code += self.visit(node)
            code += "}"

        parsedType = "code"
        return code;

    def visit_TryFinally(self, stmt_tryfinally):
        global parsedType

        code = self.visit_TryExcept(stmt_tryfinally.body, True) + "finally{"
        for node in stmt_tryfinally.finalbody:
            code += self.visit(node)
        code += "}"

        if len(stmt_tryfinally.body[0].orelse) > 0:
            code += "if($tried){"
            for node in stmt_tryfinally.body[0].orelse:
                code += self.visit(node)
            code += "}"

        parsedType = "code"
        return code

    def visit_Attribute(self, stmt_attribute):
        global parsedType, formats

        value = self.visit(stmt_attribute.value)
        if isinstance(stmt_attribute.value, _ast.Str) and stmt_attribute.attr is "format":
            formats = True

        code = value + "." + stmt_attribute.attr
        parsedType = "code"
        return code

PyParser().parse(open(sys.argv[1]).read())

stitched = ""
for module in dartImports:
    stitched += "import'" + module + "';"
if len(dartGlobalVars):
    stitched += "var " + ",".join(dartGlobalVars) + ";"
for parsedClass in parsedClasses:
    stitched += parsedClass
for parsedFunction in parsedFunctions:
    stitched += parsedFunction
stitched += "main(){"
for code in parsedCode:
    stitched += code
stitched += "}"

outFile = open("out.dart", 'w')
outFile.write(stitched)
outFile.close()