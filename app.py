import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class SistemaBiomedicoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Sistema Biomédico - Inicio de Sesión")
    self.root.geometry("450x350")
    self.root.resizable(False, False)

    # 1. Lista con los nombres EXACTOS de tus imágenes
    self.nombres_imagenes = ["fondo_1.jpg", "fondo_2.jpg", "fondo_3.jpg"]
    self.fotos_carrusel = []
    self.indice_actual = 0

    # Cargar y adaptar las imágenes al tamaño de la ventana (450x350)
    for nombre in self.nombres_imagenes:
      try:
        img = Image.open(nombre)
        img = img.resize((450, 350), Image.Resampling.LANCZOS)
        self.fotos_carrusel.append(ImageTk.PhotoImage(img))
      except Exception as e:
        print(f"No se pudo cargar la imagen {nombre}: {e}")
        # Imagen de respaldo por si ocurre algún fallo
        img = Image.new("RGB", (450, 350), color="#1e3a8a")
        self.fotos_carrusel.append(ImageTk.PhotoImage(img))

    # 2. Label que funcionará como fondo de la ventana
    self.lbl_fondo = tk.Label(root)
    self.lbl_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    # Iniciar el carrusel de fondo (cambia cada 4000 milisegundos / 4 segundos)
    self.animar_carrusel()

    # 3. Contenedor flotante (Frame) con fondo semitransparente visual para el formulario
    frame_form = tk.Frame(root, bg="#ffffff", bd=2, relief="solid")
    frame_form.place(relx=0.5, rely=0.5, anchor="center", width=340, height=270)

    # Título
    titulo = tk.Label(
        frame_form,
        text="Sistema Biomédico",
        font=("Arial", 13, "bold"),
        bg="#ffffff",
        fg="#1e3a8a",
    )
    titulo.pack(pady=15)

    # Campos de entrada
    lbl_usuario = tk.Label(
        frame_form, text="Usuario:", font=("Arial", 10), bg="#ffffff"
    )
    lbl_usuario.pack(anchor="w", padx=25)
    self.entry_usuario = tk.Entry(frame_form, font=("Arial", 10), width=28)
    self.entry_usuario.pack(pady=2)

    lbl_password = tk.Label(
        frame_form, text="Contraseña:", font=("Arial", 10), bg="#ffffff"
    )
    lbl_password.pack(anchor="w", padx=25)
    self.entry_password = tk.Entry(
        frame_form, font=("Arial", 10), width=28, show="*"
    )
    self.entry_password.pack(pady=2)

    # Botón de Ingresar
    btn_ingresar = tk.Button(
        frame_form,
        text="Iniciar Sesión",
        font=("Arial", 10, "bold"),
        bg="#2563eb",
        fg="white",
        width=20,
        command=self.validar_credenciales,
    )
    btn_ingresar.pack(pady=15)

  def cambiar_carrusel(self):
    if self.fotos_carrusel:
      # Mostrar la imagen actual en el Label de fondo
      self.lbl_fondo.config(image=self.fotos_carrusel[self.indice_actual])
      # Avanzar al siguiente índice de forma circular
      self.indice_actual = (self.indice_actual + 1) % len(
          self.fotos_carrusel
      )

  def animar_carrusel(self):
    self.cambiar_carrusel()
    # Programar el siguiente cambio en 4000 milisegundos (4 segundos)
    self.root.after(4000, self.animar_carrusel)

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