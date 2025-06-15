# codegen.py

def generate_c_code(ast):
    lines = [
        '#include <stdio.h>',
        '',
        'int main() {'
    ]

    def walk(node):
        if node[0] == 'program':
            for stmt in node[1]:
                walk(stmt)

        elif node[0] == 'assign':
            var = node[1]
            val = expr(node[2])
            lines.append(f"    int {var} = {val};")  # Consider updating this later for inferred types

        elif node[0] == 'declare':
            typ, var, val = node[1], node[2], node[3]
            c_type = {
                'int': 'int',
                'float': 'float',
                'bool': 'int'  # No native bool in C89; we treat bool as int
            }.get(typ, 'int')  # default to int if type unknown
            val_code = expr(val)
            lines.append(f"    {c_type} {var} = {val_code};")

        elif node[0] == 'print':
            val = expr(node[1])
            lines.append(f"    printf(\"%d\\n\", {val});")

        elif node[0] == 'block':
            for stmt in node[1]:
                walk(stmt)

        elif node[0] == 'if':
            condition = expr(node[1])
            lines.append(f"    if ({condition}) {{")
            walk(node[2])
            lines.append("    }")

        elif node[0] == 'if-else':
            condition = expr(node[1])
            lines.append(f"    if ({condition}) {{")
            walk(node[2])
            lines.append("    } else {")
            walk(node[3])
            lines.append("    }")

        elif node[0] == 'while':
            condition = expr(node[1])
            lines.append(f"    while ({condition}) {{")
            walk(node[2])
            lines.append("    }")
        
        elif node[0] == 'switch':
            expr_val = expr(node[1])
            lines.append(f"    switch ({expr_val}) {{")
            for case in node[2]:
                case_val, body = case[1], case[2]
                lines.append(f"    case {case_val}:")
                for stmt in body:
                    walk(stmt)
                lines.append("        break;")
            if node[3]:  # default clause
                lines.append("    default:")
                for stmt in node[3][1]:
                    walk(stmt)
            lines.append("    }")

        elif node[0] == 'do-while':
            lines.append("    do {")
            walk(node[1])
            condition = expr(node[2])
            lines.append(f"    }} while ({condition});")

        else:
            lines.append(f"    // Unknown node: {node}")


    def expr(node):
        if node[0] == 'num':
            return str(node[1])
        elif node[0] == 'id':
            return node[1]
        elif node[0] == 'binop':
            left = expr(node[2])
            right = expr(node[3])
            return f"({left} {node[1]} {right})"
        else:
            return "/* unknown_expr */"

    walk(ast)
    lines.append("    return 0;")
    lines.append("}")

    return "\n".join(lines)

