import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image as PILImage, ImageOps, ImageTk, ImageFilter
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

class FiltroDesenfoque(Filtro):
    def aplicar(self, imagen: Imagen):
        if imagen.imagen:
            imagen.imagen = imagen.imagen.filter(ImageFilter.BLUR)

class FiltroBinarizacion(Filtro):
    def aplicar(self, imagen: Imagen):
        if imagen.imagen:
            imagen.imagen = imagen.imagen.convert("L").point(lambda x: 0 if x < 128 else 255, '1').convert("RGB")

class FiltroRedimension(Filtro):
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

    def aplicar(self, imagen: Imagen):
        if imagen.imagen:
            imagen.imagen = imagen.imagen.resize((self.ancho, self.alto))

class FiltroRotacion(Filtro):
    def __init__(self, angulo):
        self.angulo = angulo

    def aplicar(self, imagen: Imagen):
        if imagen.imagen:
            imagen.imagen = imagen.imagen.rotate(self.angulo, expand=True)

# ----- Interfaz Gráfica con Tkinter -----
class EditorImagenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes - Filtros Avanzados")

        self.imagen = Imagen()

        # Botones
        botones = [
            ("Cargar Imagen", self.cargar_imagen),
            ("Aplicar Filtro Grises", self.aplicar_grises),
            ("Aplicar Filtro Inversión", self.aplicar_inversion),
            ("Aplicar Desenfoque", self.aplicar_desenfoque),
            ("Aplicar Binarización", self.aplicar_binarizacion),
            ("Redimensionar Imagen", self.aplicar_redimension),
            ("Rotar Imagen", self.aplicar_rotacion),
            ("Guardar Imagen", self.guardar_imagen)
        ]

        for texto, comando in botones:
            tk.Button(root, text=texto, command=comando).pack()

        self.canvas = tk.Label(root)
        self.canvas.pack()

    def mostrar_imagen(self):
        if self.imagen.imagen:
            img_tk = ImageTk.PhotoImage(self.imagen.imagen.resize((400, 400)))
            self.canvas.config(image=img_tk)
            self.canvas.image = img_tk

    def cargar_imagen(self):
        archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg *.bmp")])
        if archivo:
            self.imagen.cargar(archivo)
            self.mostrar_imagen()

    def aplicar_filtro(self, filtro):
        if self.imagen.imagen:
            filtro.aplicar(self.imagen)
            self.mostrar_imagen()
        else:
            messagebox.showwarning("Advertencia", "Primero debes cargar una imagen.")

    def aplicar_grises(self):
        self.aplicar_filtro(FiltroGrises())

    def aplicar_inversion(self):
        self.aplicar_filtro(FiltroInversion())

    def aplicar_desenfoque(self):
        self.aplicar_filtro(FiltroDesenfoque())

    def aplicar_binarizacion(self):
        self.aplicar_filtro(FiltroBinarizacion())

    def aplicar_redimension(self):
        ancho = simpledialog.askinteger("Redimensionar", "Nuevo ancho:")
        alto = simpledialog.askinteger("Redimensionar", "Nueva altura:")
        if ancho and alto:
            self.aplicar_filtro(FiltroRedimension(ancho, alto))

    def aplicar_rotacion(self):
        angulo = simpledialog.askfloat("Rotar", "Ángulo de rotación (grados):")
        if angulo is not None:
            self.aplicar_filtro(FiltroRotacion(angulo))

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
