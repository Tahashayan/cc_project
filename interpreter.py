
# ---------- interpreter.py ----------
# Placeholder for runtime/interpreter logic — will be completed in next step
# We will build the AST executor, environment stack, and built-in functions here

# interpreter.py

def execute(ast):
    env = {}  # Variable storage: {'x': (value, type)}

    def eval_expr(expr):
        if expr[0] == 'num':
            return expr[1]
        elif expr[0] == 'id':
            val = env.get(expr[1], (0, 'int'))  # default to 0 if undeclared
            return val[0]
        elif expr[0] == 'binop':
            op, left, right = expr[1], expr[2], expr[3]
            lval, rval = eval_expr(left), eval_expr(right)
            if op == '+': return lval + rval
            elif op == '-': return lval - rval
            elif op == '*': return lval * rval
            elif op == '/': return lval // rval if rval != 0 else 0
            elif op == '%': return lval % rval
            elif op == '>': return int(lval > rval)
            elif op == '<': return int(lval < rval)
            elif op == '==': return int(lval == rval)
            elif op == '!=': return int(lval != rval)
            elif op == '>=': return int(lval >= rval)
            elif op == '<=': return int(lval <= rval)
            elif op == '&&': return int(bool(lval) and bool(rval))
            elif op == '||': return int(bool(lval) or bool(rval))
            else: raise Exception(f"Unknown operator {op}")
        else:
            raise Exception(f"Unknown expression type {expr[0]}")

    def exec_stmt(stmt):
        kind = stmt[0]
        if kind == 'assign':
            varname, expr_val = stmt[1], eval_expr(stmt[2])
            if varname not in env:
                raise Exception(f"Variable '{varname}' not declared")
            _, var_type = env[varname]
            env[varname] = (expr_val, var_type)
        elif kind == 'declare':
            typ, var, val = stmt[1], stmt[2], eval_expr(stmt[3])
            env[var] = (val, typ)
        elif kind == 'print':
            val = eval_expr(stmt[1])
            print(val)
        elif kind == 'if-else':
            cond, then_block, else_block = stmt[1], stmt[2], stmt[3]
            if eval_expr(cond):
                exec_block(then_block)
            else:
                exec_block(else_block)
        elif kind == 'if':
            cond, then_block = stmt[1], stmt[2]
            if eval_expr(cond):
                exec_block(then_block)
        elif kind == 'while':
            cond, block = stmt[1], stmt[2]
            while eval_expr(cond):
                exec_block(block)
        elif kind == 'do-while':
            block, condition = stmt[1], stmt[2]
            while True:
                exec_block(block)
                if not eval_expr(condition):
                    break
        elif kind == 'switch':
            value = eval_expr(stmt[1])
            cases = stmt[2]
            default = stmt[3]
            executed = False
            for case in cases:
                if case[0] == 'case':
                    case_val, case_block = case[1], case[2]
                    if value == case_val:
                        exec_block(('block', case_block))
                        executed = True
                        break
            if not executed and default:
                exec_block(('block', default[1]))
        elif kind == 'break':
            pass  # handled in exec_block
        else:
            raise Exception(f"Unknown statement type {kind}")

    def exec_block(block):
        for stmt in block[1]:  # skip 'block'
            if stmt[0] == 'break':
                break
            exec_stmt(stmt)

    if ast[0] == 'program':
        for stmt in ast[1]:
            exec_stmt(stmt)
