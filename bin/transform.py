import ast, _ast, sys, os

inc_path = "file:///" + os.path.expanduser("~").replace("\\", "/") + "/.medusa/lib/"

dartImports = []
dartLocalVars = []
dartClassVars = []
dartGlobalVars = []

pyClassCache = {}
pyGlobalVars = []
pyClasses = []
pyInbuilts = ['abs',
            'all',
            'any',
            'bin',
            'dict',
            'file',
            'float',
            'input',
            'int',
            'len',
            'list',
            'max',
            'min',
            'open',
            'range',
            'raw_input',
            'set',
            'str',
            'sum',
            'tuple',
            'xrange',
            'zip']

parsedImports = []
parsedClasses = []
parsedFunctions = []
parsedCode = []
variableArgs = ["max", "min", "zip"]
userImports = []

fNames = []
fCalled = []

classyMode = False
funMode = False
broken = False
formats = False
fromTest = False
wrap = True
importing = False

imports = dict()
imports['random'] = [inc_path + "pyrandom.dart", "$PyRandom"]
imports['time'] = [inc_path + "pytime.dart", "$PyTime"]

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

        if "'" in s:
            s = '"' + s + '"'
        else:
            s = "'" + s + "'"

        return s

    def addImport(self, module):
        global dartImports

        if module not in dartImports:
            dartImports.append(module)

    def addGuard(self, name):
        global dartGlobalVars

        if name not in dartGlobalVars:
            dartGlobalVars.append(name)

    def visit_Module(self, stmt_module):
        global parsedType, parsedClasses, parsedFunctions, parsedCode, parsedImports

        for node in stmt_module.body:
            parsedType = "code"
            parsed = self.visit(node)

            if parsedType is "class":
                parsedClasses.append(parsed)
            elif parsedType is "function":
                parsedFunctions.append(parsed)
            elif parsedType is "code":
                parsedCode.append(parsed)
            elif parsedType is "imports":
                parsedImports += parsed.split(":")
            else:
                sys.stderr.write("[Medusa Error] Can't Parse " + type(node))
                exit(-1)

    def visit_UAdd(self, stmt_uadd):
        return "+"

    def visit_USub(self, stmt_usub):
        return "-"

    def visit_Invert(self, stmt_invert):
        return "~"

    def visit_Name(self, stmt_name):
        global parsedType, wrap

        name = stmt_name.id
        if name is "False" or name is "True":
            name = 'false' if name == 'False' else 'true'
            if wrap:
                self.addImport(inc_path + "inbuilts.dart")
                name = "new $PyBool(" + name + ")"
        elif name is "self":
            name = "this"
        elif name is "None":
            self.addImport(inc_path + "inbuilts.dart")
            name = "new $PyNone()"

        return name

    def visit_Num(self, stmt_num):
        global wrap

        code = ""
        if wrap:
            self.addImport(inc_path + "inbuilts.dart")
            code = "$n(" + str(stmt_num.n) + ")"
        else:
            code = str(stmt_num.n)
        return code

    def visit_Str(self, stmt_str):
        global wrap

        code = ""
        if wrap:
            self.addImport(inc_path + "inbuilts.dart")
            code =  "str('" + str(stmt_str.s) + "')"
        else:
            code = "'" + str(stmt_str.s) + "'"
        return code

    def visit_Add(self, stmt_add):
        return "+"

    def visit_Sub(self, stmt_sub):
        return "-"

    def visit_Mult(self, stmt_mult):
        return "*"

    def visit_Div(self, stmt_div):
        return "/"

    def visit_FloorDiv(self, stmt_fdiv):
        return "/"

    def visit_Pow(self, stmt_pow):
        self.addImport(inc_path + "inbuilts.dart")
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
        return "and"

    def visit_Or(self, stmt_or):
        return "or"

    def visit_In(self, stmt_in):
        return ".contains"

    def visit_Not(self, stmt_not):
        return "!"

    def visit_Is(self, stmt_is):
        return "=="

    def visit_IsNot(self, stmt_isnot):
        return "!="

    def visit_NotIn(self, stmt_notin):
        return "NotIn"

    def visit_IfExp(self, stmt_ternary):
        stmt = self.visit(stmt_ternary.test) + "?" + self.visit(stmt_ternary.body) + ":" + self.visit(stmt_ternary.orelse)
        return stmt

    def visit_UnaryOp(self, stmt_unop):
        data = self.visit(stmt_unop.op) + self.visit(stmt_unop.operand)

        return data

    def visit_BinOp(self, stmt_binop):
        global wrap

        left = self.visit(stmt_binop.left)
        op = self.visit(stmt_binop.op)
        wrap = False
        right = self.visit(stmt_binop.right)
        wrap = True
        exp = "(" + left + op + right + ")"

        if op == ",":
            exp = "($pow" + exp + ")"

        return exp

    def visit_BoolOp(self, stmt_boolop):
        self.addImport(inc_path + "inbuilts.dart");
        op = self.visit(stmt_boolop.op)
        code = "$generator((){var $temp;"

        i = 0
        while i < len(stmt_boolop.values):
            item = self.visit(stmt_boolop.values[i])
            code += "$temp=" + item + ";"
            if i == len(stmt_boolop.values) - 1:
                code += "return $temp;"
            else:
                if op == "and":
                    code += "if(!$checkValue($temp))return $temp;"
                elif op == "or":
                    code += "if($checkValue($temp))return $temp;"
                else:
                    sys.stderr.write("[Medusa Error] Operator not implemented => " + op)
                    exit(-1)
            i += 1

        code += "})"
        if fromTest:
            code = "$checkValue(" + code + ")"

        return code

    def visit_Import(self, stmt_import):
        global parsedType, imports, parsedClasses, parsedFunctions, parsedCode, importing, userImports

        code, alias, wd = [], "", os.path.split(os.path.realpath(sys.argv[1]))[0]

        for name in stmt_import.names:
            if name.name in userImports:
                continue

            try:
                self.addImport(imports[name.name][0])
                if name.asname is None:
                    alias = name.name
                else:
                    alias = name.asname

                userImports.append(name.name)
                code.append(alias + "=new " + imports[name.name][1] + "()")
            except KeyError:
                if os.path.exists(wd + os.sep + name.name + ".py"):
                    iFile =  wd + os.sep + name.name + ".py";
                elif os.path.exists(inc_path + name.name + ".py"):
                    iFile = inc_path + name.name + ".py"
                else:
                    sys.stderr.write("[Medusa Error] Unimplemented or module found for import: " + name.name)
                    exit(-1)

                if importing:
                    sys.stderr.write("[Medusa Error] Cannot recursively import user code. Yet. Sorry :(")
                    exit(-1)

                importing = True
                class_bak, func_bak, code_bak = parsedClasses, parsedFunctions, parsedCode
                parsedClasses, parsedFunctions, parsedCode = [], [], []

                self.parse(open(iFile).read())

                class_bak.append("class $" + name.name + "{")
                class_bak[-1] += "".join(parsedClasses)
                class_bak[-1] += "".join(parsedFunctions)
                class_bak[-1] += "}";
                parsedClasses = class_bak
                parsedFunctions = func_bak

                if code_bak is not []:
                    code_bak += parsedCode
                    parsedCode = code_bak

                importing = False

                if name.asname is None:
                    alias = name.name
                else:
                    alias = name.asname

                userImports.append(name.name)
                code.append(alias + "=new $" + name.name + "()")

        parsedType = "imports"
        if code is not []:
            return ":".join(code)
        else:
            return ""

    def visit_List(self, stmt_list):
        global wrap

        code = ""
        if wrap:
            self.addImport(inc_path + "inbuilts.dart");
            code += "new $PyList(["
        else:
            code += "["

        alen = len(stmt_list.elts)
        i = 0
        while i < alen:
            code += self.visit(stmt_list.elts[i])
            if i < alen - 1:
                code += ","
            i += 1
        code += "]"

        if wrap:
            code += ")"

        return code

    def visit_ListComp(self, stmt_listcomp):
        self.addImport(inc_path + "inbuilts.dart")
        code = "$generator((){var $list=new $PyList([]);"
        for node in stmt_listcomp.generators:
            code += "for(var " + self.visit(node.target) + " in " + self.visit(node.iter) + "){"
            for ifnode in node.ifs:
                code += "if(" + self.visit(ifnode) + "){"

        code += "$list.append(" + self.visit(stmt_listcomp.elt) + ");"

        for node in reversed(stmt_listcomp.generators):
            for ifnode in node.ifs:
                code += "}"
            code += "}"

        code += "return $list;})"

        return code

    def visit_GeneratorExp(self, stmt_generatorexp):
        return self.visit_ListComp(stmt_generatorexp)

    def visit_Dict(self, stmt_dict):
        self.addImport(inc_path + "inbuilts.dart");
        code = "dict(list(["
        l = len(stmt_dict.keys)
        i = 0
        while i < l:
            code += "tuple([" + self.visit(stmt_dict.keys[i]) + "," + self.visit(stmt_dict.values[i]) + "])"
            if (i + 1) < l:
                code += ","
            i += 1
        code += "]))"

        return code

    def visit_Tuple(self, stmt_tuple):
        self.addImport(inc_path + "inbuilts.dart")

        code = "tuple(["
        i = 0
        alen = len(stmt_tuple.elts)
        while i < alen:
            code += self.visit(stmt_tuple.elts[i])

            if (i + 1) < alen:
                code += ","
            i += 1
        code += "])"

        return code

    def visit_Subscript(self, stmt_Subscript):
        if isinstance(stmt_Subscript.slice, _ast.Slice):
            self.addImport(inc_path + "slice.dart")
            listVar = self.visit(stmt_Subscript.value)
            lower = self.subsituteVisit(stmt_Subscript.slice.lower)
            upper = self.subsituteVisit(stmt_Subscript.slice.upper)
            step = self.subsituteVisit(stmt_Subscript.slice.step)
            step = "new $PyNum(1)" if step is None or step == "None" else int(step)
            lower = (str(listVar) + ".length," if step < 0 else "0,") if lower is None  else str(lower) + ","
            upper = (str(listVar) + ".length," if step > 0 else "0,") if upper is None  else str(upper) + ","
            data = "$slice(" + str(listVar) + "," + str(lower) + str(upper) + str(step) + ")"
            return data
        elif isinstance(stmt_Subscript.slice, _ast.Index):
            listVar = self.visit(stmt_Subscript.value)
            index = self.visit(stmt_Subscript.slice.value)
            if isinstance(index, _ast.Num):
                index = (str(listVar) + ".length" + str(index)) if int(index) < 0 else index
            index = "[" + str(index) + "]"
            data = str(listVar) + index
            return data
        else:
            sys.stderr.write("[Medusa Error] Unimplemented Type => " + type(stmt_Subscript.slice))
            exit(-1)

    def subsituteVisit(self, node):
        if node is not None:
            return self.visit(node)
        else:
            return None

    def visit_Compare(self, stmt_test):
        global wrap

        left = self.visit(stmt_test.left)
        op = self.visit(stmt_test.ops[0])
        wrap = False
        right = self.visit(stmt_test.comparators[0])
        wrap = True

        if op == ".contains":
            code = right + op + "(" + left + ")"
        elif op == "NotIn":
            code = "!" + right + ".contains(" + left + ")"
        else:
            code = left + op + right

        return code

    def visit_ClassDef(self, stmt_class):
        global parsedType, dartLocalVars, dartClassVars, classyMode, pyClassCache

        if stmt_class.name not in pyClasses:
            pyClasses.append(stmt_class.name)

        code = "class " + stmt_class.name
        if len(stmt_class.bases) == 1:
            if stmt_class.bases[0].id == "object":
                base = "Object"
            else:
                base = str(stmt_class.bases[0].id)
            code += " extends " + base + "{"
        elif len(stmt_class.bases) > 1:
            code += "{"
            for base in stmt_class.bases:
                try:
                    code += pyClassCache[str(base.id)]
                except KeyError:
                    sys.stderr.write("[Medusa Error] Class " + str(base.id) + " is not yet defined!")
                    exit(-1)
        else:
            code += "{"

        body = ""
        classyMode = True
        for node in stmt_class.body:
            body += self.visit(node)

        pyClassCache[stmt_class.name] = body
        code += body + "}"
        classyMode = False
        dartClassVars = []

        parsedType = "class"
        return code

    def visit_Global(self, stmt_global):
        global dartGlobalVars

        for name in stmt_global.names:
            if name not in dartGlobalVars:
                dartGlobalVars.append(name)

        return ""

    def visit_Pass(self, stmt_pass):
        return ""

    def visit_FunctionDef(self, stmt_function):
        global dartLocalVars, funMode, parsedType, fNames

        body, code, defines, arguments = "", "", "", []

        for arg in stmt_function.args.args:
            arguments.append(arg.id)
            if arg.id == "self":
                stmt_function.args.args.remove(arg)
                break

        funMode = True
        for node in stmt_function.body:
            body += self.visit(node)
        funMode = False

        for arg in arguments:
            if arg in dartLocalVars:
                dartLocalVars.remove(arg)

        if len(dartLocalVars) > 0:
            defines = "var " + ",".join(dartLocalVars) + ";"

        if stmt_function.name not in fNames:
            fNames.append(stmt_function.name)

        if stmt_function.name == "__init__":
            code = pyClasses[-1] + "(" + code
        elif stmt_function.name == "main":
            code = "$main(" + code
        else:
            code = stmt_function.name + "(" + code

        alen = len(stmt_function.args.args)
        dIndex = -1

        if len(stmt_function.args.defaults):
            dIndex = alen - len(stmt_function.args.defaults)

        i, j = 0, 0
        b = False
        fixers = ""
        while i < alen:
            var = stmt_function.args.args[i].id

            if dIndex > -1 and i >= dIndex:
                if not b:
                    code += "["
                    b = True
                fixers += "if(" + var + "==null" + "){" + var + "=" + self.visit(stmt_function.args.defaults[j]) + ";}"
                j += 1

            code += var
            dartLocalVars.append(stmt_function.args.args[i].id)
            if (i + 1) < alen:
                code += ","
            i += 1

        if b:
            code += "]"
        code += "){" + fixers + defines + body + "}"
        dartLocalVars = []
        parsedType = "function"
        return code

    def visit_Call(self, stmt_call):
        global pyClasses, pyInbuilts, forceCall, formats, fCalled

        code = self.visit(stmt_call.func)
        fname = code
        keyDict = {}

        if fname in pyInbuilts:
            self.addImport(inc_path + "inbuilts.dart")
        elif code in pyClasses:
            code = "new " + fname
        elif not isinstance(stmt_call.func, _ast.Attribute) and fname not in fCalled:
            fCalled.append(fname)

        alen = len(stmt_call.args)
        i = 0

        if code == "exit":
            self.addImport("dart:io")
            if alen == 1:
                arg = stmt_call.args[0].n
            else:
                arg = 0
            return "exit(" + str(arg) + ")"
        elif code == "main":
            fname, code = "$main", "$main"

        code += "([" if (formats or fname in variableArgs) else "("
        while i < alen:
            code += self.visit(stmt_call.args[i])

            if (i + 1) < alen:
                code += ","
            i += 1
        code += "]" if (fname in variableArgs or formats) else ""

        if stmt_call.starargs != None:
            code += "," + self.visit(stmt_call.starargs)

        for node in stmt_call.keywords:
            arg = node.arg
            value = self.visit(node.value)
            keyDict[arg] = value

        code += ("," + str(keyDict) + ")") if formats else ")"

        formats = False
        return code

    def visit_Expr(self, stmt_expr):
        return self.visit(stmt_expr.value) + ";"

    def visit_Return(self, stmt_return):
        code = "return " + self.visit(stmt_return.value) + ";"
        return code

    def visit_Print(self, stmt_print):
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

        return code

    def visit_Assign(self, stmt_assign):
        global dartLocalVars, funMode, pyGlobalVars, classyMode

        code = ""
        index = 0
        multi = False

        if isinstance(stmt_assign.targets[0], _ast.Tuple):
            targets = stmt_assign.targets[0].elts

            code += "$multi=" + self.visit(stmt_assign.value) + ";";
            multi = True
            self.addGuard("$multi")
        else:
            targets = stmt_assign.targets

        for target in targets:
            if isinstance(target, _ast.Attribute) or isinstance(target, _ast.Subscript):
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
                code += target.id + "="
            if multi:
                code += "$multi[" + str(index) + "];"
                index += 1
            else:
                code += self.visit(stmt_assign.value) + ";"

        return code

    def visit_AugAssign(self, stmt_aug_assign):
        global powFlag, wrap

        left = self.visit(stmt_aug_assign.target)
        op = self.visit(stmt_aug_assign.op)
        wrap = False
        right = self.visit(stmt_aug_assign.value)
        wrap = True

        code = left
        if op == ",":
            code += "=$pow(" + left + op + right + ")"
        else:
            code += op + "=" + right

        return code + ";"

    def visit_Break(self, stmt_break):
        global broken
        return "$broken=true;break;" if broken else "break;"

    def visit_If(self, stmt_if):
        global fromTest

        fromTest = True
        code = self.visit(stmt_if.test)
        if isinstance(stmt_if.test, _ast.Name):
            code = "$checkValue(" + code + ")"
        code = "if(" + code + "){"
        for node in stmt_if.body:
            code += self.visit(node)
        code += "}"

        if len(stmt_if.orelse) > 0:
            code += "else "
            if len(stmt_if.orelse) == 1 and isinstance(stmt_if.orelse[0], _ast.If):
                code += self.visit(stmt_if.orelse[0])
            else:
                code += "{"
                for node in stmt_if.orelse:
                    code += self.visit(node)
                code += "}"

        fromTest = False
        return code

    def visit_While(self, stmt_while):
        code = "while(" + self.visit(stmt_while.test) + "){"
        for node in stmt_while.body:
            code += self.visit(node)
        code += "}"

        code += "if(!(" + self.visit(stmt_while.test) + ")){"
        for node in stmt_while.orelse:
            code += self.visit(node)
        code += "}"

        return code

    def visit_For(self, stmt_for):
        global broken, funMode

        multi = False
        if isinstance(stmt_for.target, _ast.Tuple):
            target = "$obj"
            targets = stmt_for.target.elts
            multi = True
        else:
            target = stmt_for.target.id

        broken = True
        code = "for(var " + target + " in " + self.visit(stmt_for.iter) + "){"

        if multi:
            index = 0
            for target in targets:
                t = self.visit(target)
                if funMode and t not in dartLocalVars:
                    dartLocalVars.append(t)
                elif t not in dartGlobalVars:
                    dartGlobalVars.append(t)
                code += t + "=$obj[" + str(index) + "];"
                index += 1

        for node in stmt_for.body:
            code += self.visit(node)
        code += "}"

        if len(stmt_for.orelse) > 0:
            self.addGuard("$broken")
            code = "$broken=false;" + code + "if($broken==false){"
            for node in stmt_for.orelse:
                code += self.visit(node)
            code += "$broken=false;}"
        broken = False
        return code

    def visit_Raise(self, stmt_raise):
        return "throw " + self.visit(stmt_raise.type) + ";"

    def visit_TryExcept(self, stmt_tryexcept, final = False):
        global dartLocalVars

        if not final:
            nodes = stmt_tryexcept
        else:
            nodes = stmt_tryexcept[0]

        code = "try{"
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
                sys.stderr.write("[Medusa Error] Exception handler not implemented for " + handler.type.id)
                exit(-1)

        if not final and len(nodes.orelse) > 0:
            self.addGuard("$tried")
            code = "$tried=true;" + code + "if($tried){"
            for node in nodes.orelse:
                code += self.visit(node)
            code += "$tried=false;}"

        return code;

    def visit_TryFinally(self, stmt_tryfinally):
        code = self.visit_TryExcept(stmt_tryfinally.body, True) + "finally{"
        for node in stmt_tryfinally.finalbody:
            code += self.visit(node)
        code += "}"

        if len(stmt_tryfinally.body[0].orelse) > 0:
            self.addGuard("$tried")
            code = "$tried=true;" + code + "if($tried){"
            for node in stmt_tryfinally.body[0].orelse:
                code += self.visit(node)
            code += "$tried=false;}"

        return code

    def visit_Attribute(self, stmt_attribute):
        global formats

        value = self.visit(stmt_attribute.value)
        if isinstance(stmt_attribute.value, _ast.Str) and stmt_attribute.attr is "format":
            formats = True

        code = value + "." + stmt_attribute.attr
        return code

PyParser().parse(open(sys.argv[1]).read())

stitched = ""
pyClassCache.clear()

for module in dartImports:
    stitched += "import'" + module + "';"
if len(parsedImports):
    stitched += "var " + ",".join(parsedImports) + ";"
if len(dartGlobalVars):
    stitched += "var " + ",".join(dartGlobalVars) + ";"
for parsedClass in parsedClasses:
    stitched += parsedClass
for func in fCalled:
    stitched += parsedFunctions[fNames.index(func)]
del fCalled[:]
del fNames[:]
stitched += "main(){"
for code in parsedCode:
    stitched += code
stitched += "}"

sys.stdout.write(stitched)
