from pyine import convert
import sys

if len(sys.argv) > 1:
    convert(sys.argv[1])
else:
    print("Uso: python main.py <archivo.pine>")
