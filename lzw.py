import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import time

def lzw_compress(uncompressed):
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []
    log = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            log.append(f"Emitir: {dictionary[w]} para '{w}'")
            dictionary[wc] = dict_size
            log.append(f"Añadir: '{wc}' como {dict_size}")
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
        log.append(f"Emitir final: {dictionary[w]} para '{w}'")
    return result, log

def lzw_decompress(compressed):
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    result = []
    log = []
    w = chr(compressed.pop(0))
    result.append(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError("Error en descompresión.")
        result.append(entry)
        log.append(f"Añadir: {dict_size} => '{w + entry[0]}'")
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return ''.join(result), log

def cargar_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ruta:
        with open(ruta, "r", encoding="utf-8") as file:
            contenido = file.read()
        texto_original.delete("1.0", tk.END)
        texto_original.insert(tk.END, contenido)
        entrada_ruta.set(ruta)

def comprimir_lzw():
    data = texto_original.get("1.0", tk.END)
    if not data.strip():
        messagebox.showwarning("Advertencia", "No hay texto para comprimir.")
        return
    start = time.time()
    compressed, log = lzw_compress(data)
    end = time.time()
    salida = "lzw_comprimido.txt"
    with open(salida, "w", encoding="utf-8") as f:
        f.write(','.join(map(str, compressed)))
    salida_texto.set(f"✅ LZW comprimido: {salida}\n⏱️ Tiempo: {round(end - start, 4)} s")
    log_lzw.delete("1.0", tk.END)
    log_lzw.insert(tk.END, "\n".join(log))
    log_lzw_descomp.delete("1.0", tk.END)
    salida_descomp.delete("1.0", tk.END)

def descomprimir_lzw():
    ruta = filedialog.askopenfilename(filetypes=[("LZW Compressed", "*.txt")])
    if ruta:
        with open(ruta, "r", encoding="utf-8") as f:
            compressed = list(map(int, f.read().split(",")))
        start = time.time()
        original, log = lzw_decompress(compressed)
        end = time.time()
        salida = "lzw_descomprimido.txt"
        with open(salida, "w", encoding="utf-8") as f:
            f.write(original)
        salida_texto.set(f"✅ LZW descomprimido: {salida}\n⏱️ Tiempo: {round(end - start, 4)} s")
        log_lzw_descomp.delete("1.0", tk.END)
        log_lzw_descomp.insert(tk.END, "\n".join(log))
        salida_descomp.delete("1.0", tk.END)
        salida_descomp.insert(tk.END, original)

def limpiar_campos():
    texto_original.delete("1.0", tk.END)
    log_lzw.delete("1.0", tk.END)
    log_lzw_descomp.delete("1.0", tk.END)
    salida_descomp.delete("1.0", tk.END)
    entrada_ruta.set("")
    salida_texto.set("")

# Interfaz
ventana = tk.Tk()
ventana.title("Compresión LZW")
ventana.geometry("950x780")
ventana.configure(bg="#e6f0ff")

entrada_ruta = tk.StringVar()
salida_texto = tk.StringVar()

tk.Label(ventana, text="Texto original:", font=("Arial", 12, "bold"), bg="#e6f0ff").pack(pady=(10, 0))
texto_original = scrolledtext.ScrolledText(ventana, height=10, font=("Courier", 10), bg="#ffffff")
texto_original.pack(fill="x", padx=15, pady=5)

frame_botones = tk.Frame(ventana, bg="#e6f0ff")
frame_botones.pack(pady=10)

estilo_btn = {"bg": "#007acc", "fg": "white", "font": ("Arial", 10, "bold"), "width": 20}

tk.Button(frame_botones, text="📂 Cargar archivo", command=cargar_archivo, **estilo_btn).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="🔄 LZW Comprimir", command=comprimir_lzw, **estilo_btn).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="♻️ LZW Descomprimir", command=descomprimir_lzw, **estilo_btn).grid(row=0, column=2, padx=5)
tk.Button(frame_botones, text="🧹 Limpiar", command=limpiar_campos, **estilo_btn).grid(row=0, column=3, padx=5)

tk.Label(ventana, text="Resultado:", font=("Arial", 11, "bold"), bg="#e6f0ff").pack()
tk.Label(ventana, textvariable=salida_texto, fg="blue", bg="#e6f0ff", font=("Arial", 10)).pack(pady=5)

tk.Label(ventana, text="🗜️ Compresión LZW - Registro:", font=("Arial", 11, "bold"), bg="#e6f0ff").pack(pady=(10, 0))
log_lzw = scrolledtext.ScrolledText(ventana, height=10, font=("Consolas", 10), bg="#ffffff")
log_lzw.pack(fill="both", expand=False, padx=15, pady=5)

tk.Label(ventana, text="🧩 Descompresión LZW - Registro:", font=("Arial", 11, "bold"), bg="#e6f0ff").pack(pady=(10, 0))
log_lzw_descomp = scrolledtext.ScrolledText(ventana, height=10, font=("Consolas", 10), bg="#ffffff")
log_lzw_descomp.pack(fill="both", expand=False, padx=15, pady=5)

tk.Label(ventana, text="📄 Texto descomprimido final:", font=("Arial", 11, "bold"), bg="#e6f0ff").pack(pady=(10, 0))
salida_descomp = scrolledtext.ScrolledText(ventana, height=8, font=("Courier", 10), bg="#f9f9ff")
salida_descomp.pack(fill="x", padx=15, pady=(5, 15))

ventana.mainloop()
