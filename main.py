import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
import math  # Importar para detectar NaN

# Obtener la ruta del archivo dinámicamente (busca en el mismo directorio del script)
current_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene la ruta actual del script
file_path = os.path.join(current_dir, 'Tabla_Baraja_Syncro.xlsx')  # Construye la ruta completa

# Verificar si el archivo existe en la ruta dinámica
if not os.path.exists(file_path):
    print(f"El archivo {file_path} no se encuentra. Verifica la ubicación del archivo.")
else:
    # Cargar el archivo Excel
    df_nuevo = pd.read_excel(file_path)

    # Crear el diccionario de cartas con valores cuantitativos, cualitativos y descripciones
    cards_data_actualizado = {
        f"{row['Carta']}": (int(row['Cuantitativa (q)']) if not math.isnan(row['Cuantitativa (q)']) else 0, 
                            row['Cualitativa (cl)'])  # Si es NaN, asigna 0
        for index, row in df_nuevo.iterrows()
    }

    # Crear un diccionario para las descripciones basadas en las cualitativas
    descripciones = {
        row['Cualitativa (cl)']: row['Descripción']
        for index, row in df_nuevo.iterrows()
    }

    # Obtener los valores cualitativos disponibles
    valores_cualitativos = set(df_nuevo['Cualitativa (cl)'])

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Baraja Syncro")

    # Función para actualizar el texto de cuantitativa y cualitativa al seleccionar una carta
    def update_card_info(event, card_var, label):
        carta_seleccionada = card_var.get()
        if carta_seleccionada:
            q_value, cl_value = cards_data_actualizado[carta_seleccionada]
            label.config(text=f"Cuantitativa: {q_value}, Cualitativa: {cl_value}")
        else:
            label.config(text="")

    # Función para simplificar un número (sumar los dígitos)
    def simplificar(num):
        num = int(num)  # Convertir a entero si es decimal
        return sum(int(digit) for digit in str(num))

    # Función para verificar si el valor está en la lista de cualitativas y retornar descripción
    def verificar_o_simplificar(valor):
        valor = round(valor)  # Redondear el valor si tiene decimales
        if valor in valores_cualitativos:
            descripcion = descripciones.get(valor, "")
            return valor, None, descripcion  # No se necesita simplificación, incluir descripción
        else:
            simplificado = simplificar(valor)
            # Verificar si el número simplificado tiene una cualitativa
            if simplificado in valores_cualitativos:
                descripcion_simplificada = descripciones.get(simplificado, "")
                return simplificado, valor, descripcion_simplificada
            else:
                return simplificado, valor, ""  # Retorna el valor simplificado, el original y sin descripción

    # Variables para almacenar las selecciones de las cartas
    pasado_var = tk.StringVar()
    presente_var = tk.StringVar()
    futuro_var = tk.StringVar()

    # Etiquetas para mostrar los valores cuantitativos y cualitativos seleccionados
    pasado_info = tk.Label(root, text="")
    pasado_info.grid(column=0, row=1)

    presente_info = tk.Label(root, text="")
    presente_info.grid(column=1, row=1)

    futuro_info = tk.Label(root, text="")
    futuro_info.grid(column=2, row=1)

    # Crear las etiquetas y listas desplegables
    ttk.Label(root, text="Pasado:").grid(column=0, row=0, padx=10, pady=10)
    ttk.Label(root, text="Presente:").grid(column=1, row=0, padx=10, pady=10)
    ttk.Label(root, text="Futuro:").grid(column=2, row=0, padx=10, pady=10)

    pasado_combo = ttk.Combobox(root, textvariable=pasado_var, values=list(cards_data_actualizado.keys()))
    pasado_combo.grid(column=0, row=2, padx=10, pady=10)
    pasado_combo.bind("<<ComboboxSelected>>", lambda event: update_card_info(event, pasado_var, pasado_info))

    presente_combo = ttk.Combobox(root, textvariable=presente_var, values=list(cards_data_actualizado.keys()))
    presente_combo.grid(column=1, row=2, padx=10, pady=10)
    presente_combo.bind("<<ComboboxSelected>>", lambda event: update_card_info(event, presente_var, presente_info))

    futuro_combo = ttk.Combobox(root, textvariable=futuro_var, values=list(cards_data_actualizado.keys()))
    futuro_combo.grid(column=2, row=2, padx=10, pady=10)
    futuro_combo.bind("<<ComboboxSelected>>", lambda event: update_card_info(event, futuro_var, futuro_info))

    # Función para calcular las capas con los nuevos valores, mostrando descripciones cuando aplique
    def syncro_model():
        pasado = pasado_var.get()
        presente = presente_var.get()
        futuro = futuro_var.get()
        
        # Obtener valores cuantitativos y cualitativos desde los datos actualizados
        qE, clE = cards_data_actualizado[pasado]
        qG, clG = cards_data_actualizado[presente]
        qQ, clQ = cards_data_actualizado[futuro]
        
        # Cálculos para las capas con operaciones
        operaciones = []
        
        capa1, original1, desc1 = verificar_o_simplificar(qE + qG + qQ)
        if original1:
            operaciones.append(f"§1: {qE} + {qG} + {qQ} = {original1} -> Simplificado = {capa1}")
        else:
            operaciones.append(f"§1: {qE} + {qG} + {qQ} = {capa1}")
        if desc1:
            operaciones.append(f"Descripción: {desc1}")
        
        capa2, original2, desc2 = verificar_o_simplificar(clE + clG + clQ)
        if original2:
            operaciones.append(f"§2: {clE} + {clG} + {clQ} = {original2} -> Simplificado = {capa2}")
        else:
            operaciones.append(f"§2: {clE} + {clG} + {clQ} = {capa2}")
        if desc2:
            operaciones.append(f"Descripción: {desc2}")
        
        capa3a, original3a, desc3a = verificar_o_simplificar(qE + qG)
        capa3b, original3b, desc3b = verificar_o_simplificar(qG + qQ)
        if original3a:
            operaciones.append(f"§3a: {qE} + {qG} = {original3a} -> Simplificado = {capa3a}")
        else:
            operaciones.append(f"§3a: {qE} + {qG} = {capa3a}")
        if desc3a:
            operaciones.append(f"Descripción: {desc3a}")
        if original3b:
            operaciones.append(f"§3b: {qG} + {qQ} = {original3b} -> Simplificado = {capa3b}")
        else:
            operaciones.append(f"§3b: {qG} + {qQ} = {capa3b}")
        if desc3b:
            operaciones.append(f"Descripción: {desc3b}")
        
        capa4a, original4a, desc4a = verificar_o_simplificar(clE + clG)
        capa4b, original4b, desc4b = verificar_o_simplificar(clG + clQ)
        if original4a:
            operaciones.append(f"§4a: {clE} + {clG} = {original4a} -> Simplificado = {capa4a}")
        else:
            operaciones.append(f"§4a: {clE} + {clG} = {capa4a}")
        if desc4a:
            operaciones.append(f"Descripción: {desc4a}")
        if original4b:
            operaciones.append(f"§4b: {clG} + {clQ} = {original4b} -> Simplificado = {capa4b}")
        else:
            operaciones.append(f"§4b: {clG} + {clQ} = {capa4b}")
        if desc4b:
            operaciones.append(f"Descripción: {desc4b}")
        
        # Asegurarnos de que concatenamos enteros en lugar de decimales
        capa5a, original5a, desc5a = verificar_o_simplificar(int(f"{int(qE)}{int(qG)}"))
        capa5b, original5b, desc5b = verificar_o_simplificar(int(f"{int(qG)}{int(qQ)}"))
        if original5a:
            operaciones.append(f"§5a: Unión de {qE} y {qG} = {original5a} -> Simplificado = {capa5a}")
        else:
            operaciones.append(f"§5a: Unión de {qE} y {qG} = {capa5a}")
        if desc5a:
            operaciones.append(f"Descripción: {desc5a}")
        if original5b:
            operaciones.append(f"§5b: Unión de {qG} y {qQ} = {original5b} -> Simplificado = {capa5b}")
        else:
            operaciones.append(f"§5b: Unión de {qG} y {qQ} = {capa5b}")
        if desc5b:
            operaciones.append(f"Descripción: {desc5b}")
        
        capa6a, original6a, desc6a = verificar_o_simplificar(qE + clG)
        capa6b, original6b, desc6b = verificar_o_simplificar(qG + clQ)
        if original6a:
            operaciones.append(f"§6a: {qE} + {clG} = {original6a} -> Simplificado = {capa6a}")
        else:
            operaciones.append(f"§6a: {qE} + {clG} = {capa6a}")
        if desc6a:
            operaciones.append(f"Descripción: {desc6a}")
        if original6b:
            operaciones.append(f"§6b: {qG} + {clQ} = {original6b} -> Simplificado = {capa6b}")
        else:
            operaciones.append(f"§6b: {qG} + {clQ} = {capa6b}")
        if desc6b:
            operaciones.append(f"Descripción: {desc6b}")
        
        capa7a, original7a, desc7a = verificar_o_simplificar(clE + qG)
        capa7b, original7b, desc7b = verificar_o_simplificar(clG + qQ)
        if original7a:
            operaciones.append(f"§7a: {clE} + {qG} = {original7a} -> Simplificado = {capa7a}")
        else:
            operaciones.append(f"§7a: {clE} + {qG} = {capa7a}")
        if desc7a:
            operaciones.append(f"Descripción: {desc7a}")
        if original7b:
            operaciones.append(f"§7b: {clG} + {qQ} = {original7b} -> Simplificado = {capa7b}")
        else:
            operaciones.append(f"§7b: {clG} + {qQ} = {capa7b}")
        if desc7b:
            operaciones.append(f"Descripción: {desc7b}")
        
        capa8, original8, desc8 = verificar_o_simplificar(int(f"{int(qE)}{int(qG)}") + qQ)
        if original8:
            operaciones.append(f"§8: Unión de {qE} y {qG} + {qQ} = {original8} -> Simplificado = {capa8}")
        else:
            operaciones.append(f"§8: Unión de {qE} y {qG} + {qQ} = {capa8}")
        if desc8:
            operaciones.append(f"Descripción: {desc8}")
        
        capa9, original9, desc9 = verificar_o_simplificar(qE + int(f"{int(qG)}{int(qQ)}"))
        if original9:
            operaciones.append(f"§9: {qE} + Unión de {qG} y {qQ} = {original9} -> Simplificado = {capa9}")
        else:
            operaciones.append(f"§9: {qE} + Unión de {qG} y {qQ} = {capa9}")
        if desc9:
            operaciones.append(f"Descripción: {desc9}")
        
        capa10, original10, desc10 = verificar_o_simplificar(clE + qG + qQ)
        if original10:
            operaciones.append(f"§10: {clE} + {qG} + {qQ} = {original10} -> Simplificado = {capa10}")
        else:
            operaciones.append(f"§10: {clE} + {qG} + {qQ} = {capa10}")
        if desc10:
            operaciones.append(f"Descripción: {desc10}")
        
        # Crear una nueva ventana para mostrar los resultados en un cuadro de texto
        result_window = tk.Toplevel(root)
        result_window.title("Resultados Syncro")

        # Crear un cuadro de texto para mostrar los resultados
        text_box = tk.Text(result_window, wrap='word', width=60, height=20)
        text_box.pack(padx=20, pady=20)
        
        # Insertar las operaciones en el cuadro de texto
        for operacion in operaciones:
            text_box.insert(tk.END, operacion + "\n")

        text_box.config(state="normal")  # Permite seleccionar y copiar el texto

    # Botón para calcular Syncro
    syncro_button = ttk.Button(root, text="Syncro", command=syncro_model)
    syncro_button.grid(column=1, row=3, padx=10, pady=20)

    # Ejecutar la ventana principal
    root.mainloop()
