import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import time
import os

def lz77_compress(data, window_size=20, lookahead_buffer_size=15):
    i = 0
    compressed = []
    log = []
    while i < len(data):
        max_match_distance = -1
        max_match_length = -1
        for j in range(max(0, i - window_size), i):
            length = 0
            while length < lookahead_buffer_size and i + length < len(data) and data[j + length] == data[i + length]:
                length += 1
            if length > max_match_length:
                max_match_distance = i - j
                max_match_length = length
        if max_match_length > 0:
            next_char = data[i + max_match_length] if i + max_match_length < len(data) else ''
            compressed.append((max_match_distance, max_match_length, next_char))
            log.append(f"[{i}] Match: ({max_match_distance}, {max_match_length}, {repr(next_char)})")
            i += max_match_length + 1
        else:
            compressed.append((0, 0, data[i]))
            log.append(f"[{i}] No match: (0, 0, {repr(data[i])})")
            i += 1
    return compressed, log

def lz77_decompress(compressed):
    decompressed = []
    log = []
    for step, (offset, length, next_char) in enumerate(compressed):
        if offset == 0 and length == 0:
            decompressed.append(next_char)
            log.append(f"[{step}] Direct: {repr(next_char)}")
        else:
            start = len(decompressed) - offset
            for i in range(length):
                decompressed.append(decompressed[start + i])
            decompressed.append(next_char)
            log.append(f"[{step}] Copy {length} chars from -{offset}, then add {repr(next_char)}")
    return ''.join(decompressed), log

def cargar_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ruta:
        with open(ruta, "r", encoding="utf-8") as file:
            contenido = file.read()
        texto_original.delete("1.0", tk.END)
        texto_original.insert(tk.END, contenido)
        entrada_ruta.set(ruta)

def comprimir_archivo():
    data = texto_original.get("1.0", tk.END)
    if not data.strip():
        messagebox.showwarning("Advertencia", "No hay texto para comprimir.")
        return
    start = time.time()
    compressed, log = lz77_compress(data)
    end = time.time()
    ruta = entrada_ruta.get()
    nombre = os.path.splitext(os.path.basename(ruta))[0] if ruta else "archivo"
    salida = f"{nombre}_comprimido.lz77"
    with open(salida, "w", encoding="utf-8") as f:
        for item in compressed:
            f.write(f"{item[0]},{item[1]},{repr(item[2])}\n")
    ratio = round((1 - (len(compressed) * 3 / len(data))) * 100, 2)
    salida_texto.set(f"✅ Archivo comprimido: {salida}\n📉 Tasa de compresión: {ratio}%\n⏱️ Tiempo: {round(end - start, 4)} s")
    log_compresion.delete("1.0", tk.END)
    log_compresion.insert(tk.END, "\n".join(log))
    log_descompresion.delete("1.0", tk.END)
    salida_descomp.delete("1.0", tk.END)

def descomprimir_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("LZ77 Compressed", "*.lz77")])
    if ruta:
        compressed = []
        with open(ruta, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",", 2)
                if len(parts) == 3:
                    offset, length, char_repr = parts
                    char = eval(char_repr)
                    compressed.append((int(offset), int(length), char))
        start = time.time()
        data, log = lz77_decompress(compressed)
        end = time.time()
        salida = "descomprimido.txt"
        with open(salida, "w", encoding="utf-8") as f:
            f.write(data)
        salida_texto.set(f"✅ Archivo descomprimido: {salida}\n⏱️ Tiempo: {round(end - start, 4)} s")
        log_descompresion.delete("1.0", tk.END)
        log_descompresion.insert(tk.END, "\n".join(log))
        salida_descomp.delete("1.0", tk.END)
        salida_descomp.insert(tk.END, data)

def limpiar_campos():
    texto_original.delete("1.0", tk.END)
    log_compresion.delete("1.0", tk.END)
    log_descompresion.delete("1.0", tk.END)
    salida_descomp.delete("1.0", tk.END)
    entrada_ruta.set("")
    salida_texto.set("")

# Interfaz
ventana = tk.Tk()
ventana.title("Compresión y Descompresión LZ77")
ventana.geometry("950x800")
ventana.configure(bg="#e6f0ff")

entrada_ruta = tk.StringVar()
salida_texto = tk.StringVar()

tk.Label(ventana, text="Texto original:", font=("Arial", 12, "bold"), bg="#e6f0ff").pack(pady=(10, 0))
texto_original = scrolledtext.ScrolledText(ventana, height=10, font=("Courier", 10), bg="white")
texto_original.pack(fill="x", padx=15, pady=5)

frame_botones = tk.Frame(ventana, bg="#e6f0ff")
frame_botones.pack(pady=10)

estilo_btn = {"bg": "#007acc", "fg": "white", "font": ("Arial", 10, "bold"), "width": 20}
tk.Button(frame_botones, text="📂 Cargar archivo", command=cargar_archivo, **estilo_btn).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="📦 Comprimir", command=comprimir_archivo, **estilo_btn).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="📤 Descomprimir", command=descomprimir_archivo, **estilo_btn).grid(row=0, column=2, padx=5)
tk.Button(frame_botones, text="🧹 Limpiar", command=limpiar_campos, **estilo_btn).grid(row=0, column=3, padx=5)

tk.Label(ventana, text="Resultado:", font=("Arial", 11, "bold"), bg="#e6f0ff").pack()
tk.Label(ventana, textvariable=salida_texto, fg="#007acc", bg="#e6f0ff", font=("Arial", 10)).pack(pady=5)

tk.Label(ventana, text="📘 Registro de Compresión:", font=("Arial", 11, "bold"), bg="#e6f0ff").pack(pady=(10, 0))
log_compresion = scrolledtext.ScrolledText(ventana, height=10, font=("Consolas", 10), bg="white")
log_compresion.pack(fill="both", expand=False, padx=15, pady=5)

tk.Label(ventana, text="📗 Registro de Descompresión:", font=("Arial", 11, "bold"), bg="#e6f0ff").pack(pady=(10, 0))
log_descompresion = scrolledtext.ScrolledText(ventana, height=10, font=("Consolas", 10), bg="white")
log_descompresion.pack(fill="both", expand=False, padx=15, pady=5)

tk.Label(ventana, text="📄 Texto Descomprimido Final:", font=("Arial", 11, "bold"), bg="#e6f0ff").pack(pady=(10, 0))
salida_descomp = scrolledtext.ScrolledText(ventana, height=8, font=("Courier", 10), bg="#f9f9ff")
salida_descomp.pack(fill="x", padx=15, pady=(5, 15))

ventana.mainloop()
