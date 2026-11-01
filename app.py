import tkinter as tk
from tkinter import messagebox


class SistemaBiomedicoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Sistema Biomédico - Inicio de Sesión")
    self.root.geometry("450x350")
    self.root.config(bg="#f0f4f8")

    # Título principal
    titulo = tk.Label(
        root,
        text="Acceso al Sistema Biomédico",
        font=("Arial", 14, "bold"),
        bg="#f0f4f8",
        fg="#1e3a8a",
    )
    titulo.pack(pady=25)

    # Marco (Frame) para organizar los campos de texto
    frame_form = tk.Frame(root, bg="#f0f4f8")
    frame_form.pack(pady=10)

    # Casilla de Usuario
    lbl_usuario = tk.Label(
        frame_form,
        text="Usuario:",
        font=("Arial", 11),
        bg="#f0f4f8",
        anchor="w",
    )
    lbl_usuario.grid(row=0, column=0, sticky="w", pady=8, padx=5)
    self.entry_usuario = tk.Entry(frame_form, font=("Arial", 11), width=22)
    self.entry_usuario.grid(row=0, column=1, pady=8, padx=5)

    # Casilla de Contraseña (oculta los caracteres con asteriscos)
    lbl_password = tk.Label(
        frame_form,
        text="Contraseña:",
        font=("Arial", 11),
        bg="#f0f4f8",
        anchor="w",
    )
    lbl_password.grid(row=1, column=0, sticky="w", pady=8, padx=5)
    self.entry_password = tk.Entry(
        frame_form, font=("Arial", 11), width=22, show="*"
    )
    self.entry_password.grid(row=1, column=1, pady=8, padx=5)

    # Botón de Ingresar
    btn_ingresar = tk.Button(
        root,
        text="Iniciar Sesión",
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        width=15,
        command=self.validar_credenciales,
    )
    btn_ingresar.pack(pady=20)

  def validar_credenciales(self):
    usuario = self.entry_usuario.get()
    password = self.entry_password.get()

    # Validación simple de ejemplo
    if usuario == "admin" and password == "1234":
      messagebox.showinfo(
          "Bienvenido", f"Acceso concedido. ¡Hola, {usuario}!"
      )
    else:
      messagebox.showerror(
          "Error", "Usuario o contraseña incorrectos."
      )


if __name__ == "__main__":
  root = tk.Tk()
  app = SistemaBiomedicoApp(root)
  root.mainloop()