import sys
import os
print("Current directory:", os.getcwd())
print("Files:", os.listdir())
from parser import parser
from interpreter import execute
from codegen import generate_c_code


filename = 'test.tiny'  # Or any path to your test file
with open(filename, 'r') as file:
    code = file.read()

# Parse
result = parser.parse(code)

print("✅ AST Generated:")
print(result)

print("\n💻 Executing program:\n")
execute(result)


c_code = generate_c_code(result)
with open("out.c", "w") as f:
    f.write(c_code)
print("✅ C code generated in out.c")

