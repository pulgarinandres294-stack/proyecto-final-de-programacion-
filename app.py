import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class SistemaBiomedicoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Sistema Biomédico - Inicio de Sesión")
    self.root.geometry("450x350")
    self.root.resizable(False, False)

    # 1. Rutas de las imágenes del carrusel
    self.nombres_imagenes = ["fondo_1.jpg", "fondo_2.jpg", "fondo_3.jpg"]
    self.imagenes_pil = []
    self.indice_actual = 0

    # Cargar y redimensionar las imágenes originales
    for nombre in self.nombres_imagenes:
      try:
        img = Image.open(nombre).resize((450, 350), Image.Resampling.LANCZOS)
        self.imagenes_pil.append(img)
      except Exception as e:
        print(f"Aviso: No se pudo cargar {nombre} ({e})")
        # Imagen de respaldo azul oscuro si falta alguna
        img = Image.new("RGB", (450, 350), color="#0f172a")
        self.imagenes_pil.append(img)

    # Mantener referencias activas para Tkinter
    self.fotos_carrusel = [
        ImageTk.PhotoImage(img) for img in self.imagenes_pil
    ]

    # 2. Label de fondo principal
    self.lbl_fondo = tk.Label(root)
    self.lbl_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    if self.fotos_carrusel:
      self.lbl_fondo.config(image=self.fotos_carrusel[0])

    # Iniciar carrusel automático (cambia cada 5 segundos)
    self.root.after(5000, self.proximo_slide)

    # 3. Panel de inicio de sesión estilizado (minimalista y semitransparente visualmente)
    # Usamos un color oscuro elegante para que contraste perfecto con las fotos biomédicas
    frame_form = tk.Frame(root, bg="#0f172a", bd=0)
    frame_form.place(relx=0.5, rely=0.5, anchor="center", width=320, height=260)

    # Título
    titulo = tk.Label(
        frame_form,
        text="SISTEMA BIOMÉDICO",
        font=("Arial", 12, "bold"),
        bg="#0f172a",
        fg="#38bdf8",
    )
    titulo.pack(pady=15)

    # Campos de entrada
    lbl_usuario = tk.Label(
        frame_form,
        text="Usuario",
        font=("Arial", 9, "bold"),
        bg="#0f172a",
        fg="#cbd5e1",
    )
    lbl_usuario.pack(anchor="w", padx=30)
    self.entry_usuario = tk.Entry(
        frame_form,
        font=("Arial", 11),
        bg="#1e293b",
        fg="white",
        insertbackground="white",
        relief="flat",
    )
    self.entry_usuario.pack(fill="x", padx=30, pady=4)

    lbl_password = tk.Label(
        frame_form,
        text="Contraseña",
        font=("Arial", 9, "bold"),
        bg="#0f172a",
        fg="#cbd5e1",
    )
    lbl_password.pack(anchor="w", padx=30, pady=(5, 0))
    self.entry_password = tk.Entry(
        frame_form,
        font=("Arial", 11),
        bg="#1e293b",
        fg="white",
        insertbackground="white",
        show="*",
        relief="flat",
    )
    self.entry_password.pack(fill="x", padx=30, pady=4)

    # Botón de Ingresar moderno
    btn_ingresar = tk.Button(
        frame_form,
        text="Ingresar",
        font=("Arial", 10, "bold"),
        bg="#0284c7",
        fg="white",
        activebackground="#0369a1",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=self.validar_credenciales,
    )
    btn_ingresar.pack(fill="x", padx=30, pady=15)

  def proximo_slide(self):
    # Calcular siguiente índice
    siguiente_indice = (self.indice_actual + 1) % len(self.imagenes_pil)

    # Efecto de transición suave (Cross-fade usando Pillow)
    self.transicionar_imagenes(
        self.imagenes_pil[self.indice_actual],
        self.imagenes_pil[siguiente_indice],
        paso=0,
    )

    self.indice_actual = siguiente_indice
    # Repetir el ciclo cada 5 segundos
    self.root.after(5000, self.proximo_slide)

  def transicionar_imagenes(self, img1, img2, paso):
    # Realiza pequeños pasos de mezcla para lograr el efecto desvanecido fluido
    if paso <= 10:
      alpha = paso / 10.0
      img_mezclada = Image.blend(img1, img2, alpha)
      foto_temp = ImageTk.PhotoImage(img_mezclada)
      self.lbl_fondo.config(image=foto_temp)
      self.lbl_fondo.image = foto_temp  # Evita que Python borre la referencia
      # Velocidad de la transición (40 milisegundos por frame)
      self.root.after(
          40, lambda: self.transicionar_imagenes(img1, img2, paso + 1)
      )

  def validar_credenciales(self):
    usuario = self.entry_usuario.get()
    password = self.entry_password.get()

    if usuario == "admin" and password == "1234":
      messagebox.showinfo(
          "Bienvenido", f"Acceso concedido. ¡Hola, {usuario}!"
      )
    else:
      messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


if __name__ == "__main__":
  root = tk.Tk()
  app = SistemaBiomedicoApp(root)
  root.mainloop()