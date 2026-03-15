import tkinter as tk
from tkinter import messagebox
import random


def cargar_preguntas(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            texto = f.read()
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo {nombre_archivo}")
        return []

    lineas = [line.strip() for line in texto.split("\n") if line.strip()]
    preguntas = []

    i = 0
    while i < len(lineas) - 1:
        pregunta = lineas[i]
        respuesta = lineas[i + 1]

        if respuesta.startswith("(Respuesta):"):
            respuesta = respuesta.replace("(Respuesta):", "", 1).strip()
            preguntas.append((pregunta, respuesta))

        i += 2

    return preguntas


class AppPreguntas:
    def __init__(self, root):
        self.root = root
        self.root.title("Preguntas aleatorias")
        self.root.geometry("800x500")
        self.root.configure(padx=20, pady=20)

        # Diccionario de categorías y archivos
        self.archivos_categorias = {
            "Medicina": "preguntas_medicina.txt",
            "Historia": "preguntas_historia.txt",
            "Literatura": "preguntas_literatura.txt",
        }

        self.preguntas = []
        self.pregunta_actual = None

        titulo = tk.Label(
            root,
            text="Preguntas aleatorias",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=(0, 20))

        # Frame para categoría
        frame_categoria = tk.Frame(root)
        frame_categoria.pack(pady=10)

        label_categoria = tk.Label(
            frame_categoria,
            text="Elegí una categoría:",
            font=("Arial", 12)
        )
        label_categoria.grid(row=0, column=0, padx=10)

        self.categoria_var = tk.StringVar()
        self.categoria_var.set("Todas")

        opciones = ["Todas"] + list(self.archivos_categorias.keys())

        menu_categoria = tk.OptionMenu(
            frame_categoria,
            self.categoria_var,
            *opciones,
            command=self.cambiar_categoria
        )
        menu_categoria.config(font=("Arial", 12), width=15)
        menu_categoria.grid(row=0, column=1, padx=10)

        self.label_pregunta = tk.Label(
            root,
            text="Elegí una categoría y apretá 'Nueva pregunta'",
            font=("Arial", 16),
            wraplength=700,
            justify="center"
        )
        self.label_pregunta.pack(pady=20)

        self.label_respuesta = tk.Label(
            root,
            text="Respuesta oculta",
            font=("Arial", 14),
            fg="blue",
            wraplength=700,
            justify="center"
        )
        self.label_respuesta.pack(pady=20)

        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=20)

        btn_pregunta = tk.Button(
            frame_botones,
            text="Nueva pregunta",
            font=("Arial", 12),
            width=18,
            command=self.nueva_pregunta
        )
        btn_pregunta.grid(row=0, column=0, padx=10)

        btn_respuesta = tk.Button(
            frame_botones,
            text="Mostrar respuesta",
            font=("Arial", 12),
            width=18,
            command=self.mostrar_respuesta
        )
        btn_respuesta.grid(row=0, column=1, padx=10)

        # Cargar categoría inicial
        self.cambiar_categoria("Todas")

    def cargar_todas_las_preguntas(self):
        todas = []
        for archivo in self.archivos_categorias.values():
            todas.extend(cargar_preguntas(archivo))
        return todas

    def cambiar_categoria(self, categoria):
        if categoria == "Todas":
            self.preguntas = self.cargar_todas_las_preguntas()
        else:
            archivo = self.archivos_categorias[categoria]
            self.preguntas = cargar_preguntas(archivo)

        self.pregunta_actual = None
        self.label_pregunta.config(text=f"Categoría actual: {categoria}\nApretá 'Nueva pregunta'")
        self.label_respuesta.config(text="Respuesta oculta")

        if not self.preguntas:
            messagebox.showwarning(
                "Aviso",
                f"No se cargaron preguntas válidas para la categoría '{categoria}'."
            )

    def nueva_pregunta(self):
        if not self.preguntas:
            messagebox.showwarning("Aviso", "No hay preguntas cargadas en esta categoría.")
            return

        self.pregunta_actual = random.choice(self.preguntas)
        self.label_pregunta.config(text=self.pregunta_actual[0])
        self.label_respuesta.config(text="Respuesta oculta")

    def mostrar_respuesta(self):
        if self.pregunta_actual is None:
            messagebox.showinfo("Aviso", "Primero elegí una pregunta.")
            return

        self.label_respuesta.config(text=self.pregunta_actual[1])


if __name__ == "__main__":
    root = tk.Tk()
    app = AppPreguntas(root)
    root.mainloop()