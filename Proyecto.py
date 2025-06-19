import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image as PILImage, ImageOps, ImageTk
from abc import ABC, abstractmethod

# ----- Lógica POO de imagen y filtros -----
class Imagen:
    def __init__(self):
        self.imagen = None
        self.ruta = None

    def cargar(self, ruta):
        self.ruta = ruta
        self.imagen = PILImage.open(ruta)

    def guardar(self, ruta_destino):
        if self.imagen:
            self.imagen.save(ruta_destino)

class Filtro(ABC):
    @abstractmethod
    def aplicar(self, imagen: Imagen):
        pass

class FiltroGrises(Filtro):
    def aplicar(self, imagen: Imagen):
        if imagen.imagen:
            imagen.imagen = imagen.imagen.convert("L").convert("RGB")

class FiltroInversion(Filtro):
    def aplicar(self, imagen: Imagen):
        if imagen.imagen:
            imagen.imagen = ImageOps.invert(imagen.imagen)

# ----- Interfaz Gráfica con Tkinter -----
class EditorImagenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes - Filtros Básicos")

        self.imagen = Imagen()

        # Botones
        self.btn_cargar = tk.Button(root, text="Cargar Imagen", command=self.cargar_imagen)
        self.btn_cargar.pack()

        self.btn_grises = tk.Button(root, text="Aplicar Filtro Grises", command=self.aplicar_grises)
        self.btn_grises.pack()

        self.btn_invertir = tk.Button(root, text="Aplicar Filtro Inversión", command=self.aplicar_inversion)
        self.btn_invertir.pack()

        self.btn_guardar = tk.Button(root, text="Guardar Imagen", command=self.guardar_imagen)
        self.btn_guardar.pack()

        self.canvas = tk.Label(root)
        self.canvas.pack()

    def mostrar_imagen(self):
        if self.imagen.imagen:
            img_tk = ImageTk.PhotoImage(self.imagen.imagen.resize((400, 400)))
            self.canvas.config(image=img_tk)
            self.canvas.image = img_tk  # Mantener referencia

    def cargar_imagen(self):
        archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg *.bmp")])
        if archivo:
            self.imagen.cargar(archivo)
            self.mostrar_imagen()

    def aplicar_grises(self):
        if self.imagen.imagen:
            filtro = FiltroGrises()
            filtro.aplicar(self.imagen)
            self.mostrar_imagen()
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar una imagen.")

    def aplicar_inversion(self):
        if self.imagen.imagen:
            filtro = FiltroInversion()
            filtro.aplicar(self.imagen)
            self.mostrar_imagen()
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar una imagen.")

    def guardar_imagen(self):
        if self.imagen.imagen:
            archivo = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                    filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if archivo:
                self.imagen.guardar(archivo)
                messagebox.showinfo("Éxito", "Imagen guardada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "No hay imagen para guardar.")

# ----- Ejecutar la aplicación -----
if __name__ == "__main__":
    root = tk.Tk()
    app = EditorImagenApp(root)
    root.mainloop()
