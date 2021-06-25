import js2py
import PyvD
from os import getcwd


context = js2py.EvalJs()

context.execute(open(getcwd() + "\\js\\api.js", encoding="utf-8").read())

result = context.rsaKey("13232469869", "050616", "asdq")
print(result)