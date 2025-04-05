import re

# misc


def comment(line):
    _ = False
    if re.findall("strategy|study|plot|//", line):
        line = line.split(' ')
        line.insert(0, '#')
        line = ' '.join(line)
        _ = True
    return line, _

# logic >>>> add more logic support


def logic(line):
    if re.findall("if ", line):
        # Mejora para manejar la indentación
        line = line.strip()
        if line.endswith(':'):
            # Ya tiene el formato correcto de Python
            return line + '\n'
            
        parts = line.split(' ')
        parts[-1] = parts[-1].strip('\n')
        if not line.endswith(':'):
            parts.append(':')
        formatted_line = ' '.join(parts) + '\n'
        return formatted_line
    return line

# booleans


def boolean(line):
    boolx = re.findall("true|false", line)
    for booly in boolx:
        string = line.split(booly)
        booly = booly.replace(" ", "").capitalize()
        string.insert(-1, booly)
        line = ''.join(string)
    return line

# operators


def operator(line):
    # Mejorado: ahora maneja correctamente := y ?
    if ":=" in line:
        parts = line.split(":=")
        if len(parts) >= 2:
            # Eliminar espacios al principio y final
            var_name = parts[0].strip()
            value = parts[1].strip()
            line = f"{var_name} = {value}"
    elif "?" in line and ":" in line:
        try:
            # Extraer variable = condición ? valor_true : valor_false
            if "=" in line:
                var_parts = line.split("=", 1)
                var_name = var_parts[0].strip()
                ternary_expr = var_parts[1].strip()
            else:
                var_name = ""
                ternary_expr = line
                
            # Extraer partes del operador ternario
            condition_parts = ternary_expr.split("?", 1)
            condition = condition_parts[0].strip()
            
            values_parts = condition_parts[1].split(":", 1) if len(condition_parts) > 1 else ["", ""]
            true_value = values_parts[0].strip() if len(values_parts) > 0 else ""
            false_value = values_parts[1].strip() if len(values_parts) > 1 else ""
            
            if var_name and condition and true_value and false_value:
                line = f"{var_name} = {true_value} if {condition} else {false_value}"
            else:
                line = '# Error: formato incorrecto para operador ternario'
        except Exception as e:
            line = f'# Error en operador ternario: {str(e)}'
            
    return line

# Función para manejar valores NA/na
def handle_na(line):
    if " na" in line or "=na" in line or ",na" in line or "(na" in line:
        line = line.replace(" na", " None")
        line = line.replace("=na", "=None")
        line = line.replace(",na", ",None")
        line = line.replace("(na", "(None")
    return line

# Función para corregir asignaciones múltiples
def fix_multi_assignments(line):
    # Buscar patrones de asignación consecutiva 
    if "=" in line and not "==" in line and not "<=" in line and not ">=" in line:
        # Eliminar espacios al inicio y final
        line = line.strip()
        
        # Si hay múltiples '=' en la línea, podría ser una asignación múltiple
        if line.count('=') > 1:
            parts = line.split('=')
            # Limpiar espacios en blanco
            parts = [p.strip() for p in parts]
            
            # Crear líneas de asignación separadas
            result = ""
            for i in range(len(parts) - 1):
                result += f"{parts[i]} = {parts[-1]}\n"
            return result
    
    return line

# builtins >>>>> add more builtin function support


def builtins(line):
    # Manejar funciones nativas de Pine Script
    pine_funcs = {
        "ta.rsi": "calculate_rsi",
        "ta.ema": "calculate_ema",
        "ta.sma": "calculate_sma",
        "input.int": "input_int",
        "input.float": "input_float",
        "input.bool": "input_bool",
        "input.string": "input_string",
        "input.time": "input_time",
        "timestamp": "convert_timestamp",
        "strategy.entry": "strategy_entry",
        "strategy.exit": "strategy_exit",
        "strategy.close_all": "strategy_close_all",
        "plot": "plot_indicator"
    }
    
    for pine_func, py_func in pine_funcs.items():
        if pine_func in line:
            line = line.replace(pine_func, py_func)
    
    # Manejo de funciones específicas - corregido escape de caracteres
    funcx = re.findall(r"input\(|alert\(", line)
    if funcx:
        funcy = funcx[0]
        if funcy == 'alert(':
            string = line.split(funcy)
            funcy = funcy.replace("alert(", "print(")
            string.insert(-1, funcy)
            line = ''.join(string)
        if funcy == 'input(':
            line = '# pyine does not currently support inputs [{0}]\n'.format(
                line.strip('\n'))
    return line

# functions


def functions(line):
    if "=>" in line:
        # Manejar funciones definidas con =>
        try:
            parts = line.split("=>")
            func_def = parts[0].strip()
            func_body = parts[1].strip()
            
            # Extraer nombre de función y parámetros
            if "(" in func_def and ")" in func_def:
                func_name = func_def.split("(")[0].strip()
                params = "(" + func_def.split("(", 1)[1]
            else:
                func_name = func_def
                params = "()"
                
            # Crear definición de función en Python
            func_definition = f"def {func_name}{params}:\n"
            
            # Manejar el cuerpo de la función
            # Si hay un switch, lo manejamos de forma especial
            if "switch" in func_body:
                switch_code = handle_switch(func_body, func_name, params)
                func_definition += switch_code
            else:
                func_definition += "    return " + func_body
                
            line = func_definition
        except Exception as e:
            line = f"# Error convirtiendo función: {str(e)}\n# Original: {line}"
    return line

# Manejar estructuras switch - mejorado
def handle_switch(line, func_name="", params=""):
    if "switch" not in line:
        return line
        
    try:
        # Extraer la variable del switch
        switch_var = line.split("switch")[1].split()[0].strip()
        
        # Crear una función de switch más completa
        result = "    # Convertido desde switch de Pine Script\n"
        result += f"    switch_var = {switch_var}\n"
        
        # Buscar casos en el formato "valor" => expresión
        if "=>" in line:
            # Preparar código para casos
            result += "    if switch_var == "
            
            # Este es un enfoque simplificado, mejorable por un parser real
            if '"close"' in line:
                result += '"close":\n        return close\n'
            if '"high"' in line:
                result += '    elif switch_var == "high":\n        return high\n'
            if '"low"' in line:
                result += '    elif switch_var == "low":\n        return low\n'
            if '"open"' in line:
                result += '    elif switch_var == "open":\n        return open\n'
            
            result += "    else:\n        return None  # Valor por defecto\n"
        else:
            result += "    # Se requiere completar manualmente los casos del switch\n"
            result += "    pass\n"
            
        return result
    except Exception as e:
        return f"    # Error al convertir switch: {str(e)}\n    pass\n"

# Función para ajustar la indentación
def fix_indentation(lines):
    result = []
    indentation_level = 0
    
    for line in lines:
        line = line.rstrip()
        
        # Si la línea termina con ":", aumentamos la indentación para la siguiente línea
        if line.endswith(':'):
            result.append(line)
            indentation_level += 1
            continue
            
        # Si la línea es solo espacios o está vacía, la mantenemos igual
        if not line.strip() or line.strip().startswith('#'):
            result.append(line)
            continue
            
        # Aplicar la indentación actual
        if indentation_level > 0:
            line = '    ' * indentation_level + line.lstrip()
            
        result.append(line)
    
    return result

# MAIN
def convert(file):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        filename = file.split(".")[0]

    # Almacenar líneas procesadas
    processed_lines = []
    
    # Añadir encabezado y funciones de ayuda
    processed_lines.append('from pyine.indicators import *\n')
    processed_lines.append('# Funciones auxiliares para la traduccion de Pine Script\n')
    processed_lines.append('def calculate_rsi(source, length):\n')
    processed_lines.append('    # Implementar calculo de RSI usando pandas\n')
    processed_lines.append('    return None  # TODO: Implementar\n\n')
    processed_lines.append('def calculate_ema(source, length):\n')
    processed_lines.append('    # Implementar EMA usando pandas\n')
    processed_lines.append('    return None  # TODO: Implementar\n\n')
    processed_lines.append('def input_int(default, title, **kwargs):\n')
    processed_lines.append('    # En Python simplemente devolvemos el valor por defecto\n')
    processed_lines.append('    return default\n\n')
    processed_lines.append('def input_float(default, title, **kwargs):\n')
    processed_lines.append('    return default\n\n')
    processed_lines.append('def input_bool(default, title, **kwargs):\n')
    processed_lines.append('    return default\n\n')
    processed_lines.append('def input_string(default, title, **kwargs):\n')
    processed_lines.append('    return default\n\n')
    processed_lines.append('def input_time(timestamp_val, title, **kwargs):\n')
    processed_lines.append('    return timestamp_val\n\n')
    processed_lines.append('def convert_timestamp(year, month, day, hour=0, minute=0):\n')
    processed_lines.append('    from datetime import datetime\n')
    processed_lines.append('    return datetime(year, month, day, hour, minute)\n\n')
    processed_lines.append('def strategy_entry(id, direction, **kwargs):\n')
    processed_lines.append('    print(f"Entrada: {id}, direccion: {direction}")\n\n')
    processed_lines.append('def strategy_exit(id, **kwargs):\n')
    processed_lines.append('    print(f"Salida: {id}")\n\n')
    processed_lines.append('def strategy_close_all(comment=""):\n')
    processed_lines.append('    print(f"Cerrar todas las posiciones: {comment}")\n\n')
    processed_lines.append('def plot_indicator(value, title="", color=None, **kwargs):\n')
    processed_lines.append('    # Seria implementado con matplotlib o similar\n')
    processed_lines.append('    pass\n\n')
    
    # Añadir función getSource manualmente
    processed_lines.append('def getSource(src):\n')
    processed_lines.append('    # Convertido manualmente desde switch de Pine Script\n')
    processed_lines.append('    if src == "close":\n')
    processed_lines.append('        return close\n')
    processed_lines.append('    elif src == "high":\n')
    processed_lines.append('        return high\n')
    processed_lines.append('    elif src == "low":\n')
    processed_lines.append('        return low\n')
    processed_lines.append('    elif src == "open":\n')
    processed_lines.append('        return open\n')
    processed_lines.append('    else:\n')
    processed_lines.append('        return None  # Valor por defecto\n\n')
    
    processed_lines.append('\n# Codigo traducido de Pine Script\n\n')
    
    # Procesar el archivo línea por línea
    skip_getSource = False
    
    for i, line in enumerate(lines):
        # Detectar y omitir la definición de getSource
        if "getSource(src) =>" in line:
            skip_getSource = True
            continue
            
        # Omitir líneas de la definición de getSource
        if skip_getSource:
            if line.strip() and not line.strip().startswith("//") and not "switch" in line and not "=>" in line and not line.strip().startswith('"'):
                skip_getSource = False
            else:
                continue
        
        # Procesar normalmente las demás líneas
        line, c = comment(line)
        if not c:
            # Aplicar todas las transformaciones
            line = functions(line)
            line = logic(line)
            line = boolean(line)
            line = operator(line)
            line = handle_na(line)
            line = builtins(line)
            line = fix_multi_assignments(line)
        
        processed_lines.append(line)
    
    # Arreglar la indentación
    indented_lines = fix_indentation(processed_lines)
    
    # Escribir el resultado
    with open('{0}.py'.format(filename), 'w', encoding='utf-8') as f:
        for line in indented_lines:
            f.write(line + '\n' if not line.endswith('\n') else line)
