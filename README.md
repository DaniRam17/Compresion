# Compresion

 Descripción del Proyecto
Este proyecto implementa dos algoritmos de compresión: LZW (Lempel-Ziv-Welch) y LZ77 (Sliding Window). Ambos se integran en aplicaciones de interfaz gráfica desarrolladas con Tkinter, permitiendo:

Comprimir texto desde un archivo .txt.

Guardar el resultado comprimido.

Visualizar los pasos del algoritmo (registro detallado).

Descomprimir el archivo comprimido.

Mostrar el texto original recuperado.

🛠️ Requisitos
Python 3.7+

Librerías estándar:

tkinter

time

os

No necesitas instalar dependencias externas.

🧩 Instrucciones de instalación y ejecución
🔹 1. Ejecutar el código (modo desarrollo)



python lzw_app.py     # para el compresor LZW
python lz77_app.py    # para el compresor LZ77


🔹 2. Compilar a .exe para distribución (requiere pyinstaller)

Instala PyInstaller:


pip install pyinstaller
Compila el archivo a ejecutable:


pyinstaller --onefile --noconsole lzw.py
pyinstaller --onefile --noconsole lz77.py
El ejecutable aparecerá en la carpeta dist/.


 Uso de los programas
1. Comprimir texto
Clic en 📂 Cargar archivo y selecciona un archivo .txt.

Clic en 📦 Comprimir.

El archivo comprimido se guarda como:

lzw_comprimido.txt (LZW)

nombre_comprimido.lz77 (LZ77)

Se muestra un log detallado con los pasos del algoritmo.

2. Descomprimir archivo
Clic en 📤 Descomprimir y selecciona el archivo comprimido.

Se mostrará:

El log del proceso de reconstrucción.

El texto descomprimido final.

Un nuevo archivo descomprimido.txt.

