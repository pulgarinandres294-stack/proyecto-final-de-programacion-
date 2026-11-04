import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class SistemaBiomedicoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Sistema de Inventario - Inicio de Sesión")
    self.root.geometry("700x350")
    self.root.resizable(False, False)

    # Base de datos simulada en memoria (Usuario: {"password": ..., "correo": ...})
    self.usuarios_db = {"admin": {"password": "1234", "correo": "admin@mail.com"}}

    # 1. PANEL IZQUIERDO: Carrusel de imágenes
    self.lbl_imagen = tk.Label(root, bg="#0f172a")
    self.lbl_imagen.place(x=0, y=0, width=350, height=350)

    self.nombres_imagenes = ["fondo_1.jpg", "fondo_2.jpg", "fondo_3.jpg"]
    self.imagenes_pil = []
    self.indice_actual = 0

    for nombre in self.nombres_imagenes:
      try:
        img = Image.open(nombre).resize(
            (350, 350), Image.Resampling.LANCZOS
        )
        self.imagenes_pil.append(img)
      except Exception:
        img = Image.new("RGB", (350, 350), color="#0f172a")
        self.imagenes_pil.append(img)

    self.fotos_carrusel = [
        ImageTk.PhotoImage(img) for img in self.imagenes_pil
    ]
    if self.fotos_carrusel:
      self.lbl_imagen.config(image=self.fotos_carrusel[0])

    self.root.after(5000, self.proximo_slide)

    # 2. PANEL DERECHO: Formulario de inicio de sesión
    self.frame_form = tk.Frame(root, bg="#0f172a")
    self.frame_form.place(x=350, y=0, width=350, height=350)

    titulo = tk.Label(
        self.frame_form,
        text="SISTEMA DE INVENTARIO",
        font=("Arial", 12, "bold"),
        bg="#0f172a",
        fg="#38bdf8",
    )
    titulo.pack(pady=(35, 15))

    # Campos de entrada
    lbl_usuario = tk.Label(
        self.frame_form,
        text="Usuario",
        font=("Arial", 9, "bold"),
        bg="#0f172a",
        fg="#cbd5e1",
    )
    lbl_usuario.pack(anchor="w", padx=40)
    self.entry_usuario = tk.Entry(
        self.frame_form,
        font=("Arial", 11),
        bg="#1e293b",
        fg="white",
        insertbackground="white",
        relief="flat",
    )
    self.entry_usuario.pack(fill="x", padx=40, pady=2)

    lbl_password = tk.Label(
        self.frame_form,
        text="Contraseña",
        font=("Arial", 9, "bold"),
        bg="#0f172a",
        fg="#cbd5e1",
    )
    lbl_password.pack(anchor="w", padx=40, pady=(8, 0))
    self.entry_password = tk.Entry(
        self.frame_form,
        font=("Arial", 11),
        bg="#1e293b",
        fg="white",
        insertbackground="white",
        show="*",
        relief="flat",
    )
    self.entry_password.pack(fill="x", padx=40, pady=2)

    # Enlace de ¿Olvidaste tu contraseña?
    btn_olvido = tk.Button(
        self.frame_form,
        text="¿Olvidaste tu contraseña?",
        font=("Arial", 8),
        bg="#0f172a",
        fg="#38bdf8",
        activebackground="#0f172a",
        activeforeground="#7dd3fc",
        bd=0,
        cursor="hand2",
        command=self.ventana_recuperar,
    )
    btn_olvido.pack(anchor="e", padx=40, pady=2)

    # Botón de Ingresar
    btn_ingresar = tk.Button(
        self.frame_form,
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
    btn_ingresar.pack(fill="x", padx=40, pady=10)

    # Enlace para registrar nuevo usuario
    btn_registro = tk.Button(
        self.frame_form,
        text="¿No tienes cuenta? Regístrate aquí",
        font=("Arial", 9),
        bg="#0f172a",
        fg="#38bdf8",
        activebackground="#0f172a",
        activeforeground="#7dd3fc",
        bd=0,
        cursor="hand2",
        command=self.ventana_registro,
    )
    btn_registro.pack(pady=5)

  def proximo_slide(self):
    if self.fotos_carrusel:
      self.indice_actual = (self.indice_actual + 1) % len(
          self.fotos_carrusel
      )
      self.lbl_imagen.config(image=self.fotos_carrusel[self.indice_actual])
    self.root.after(5000, self.proximo_slide)

  def validar_credenciales(self):
    usuario = self.entry_usuario.get().strip()
    password = self.entry_password.get().strip()

    if usuario in self.usuarios_db and self.usuarios_db[usuario]["password"] == password:
      messagebox.showinfo(
          "Bienvenido", f"Acceso concedido. ¡Hola, {usuario}!"
      )
    else:
      messagebox.showerror(
          "Error", "Usuario o contraseña incorrectos."
      )

  # --- VENTANA DE REGISTRO ---
  def ventana_registro(self):
    ven_reg = tk.Toplevel(self.root)
    ven_reg.title("Registro de Nuevo Usuario")
    ven_reg.geometry("320x300")
    ven_reg.config(bg="#0f172a")
    ven_reg.resizable(False, False)

    tk.Label(
        ven_reg,
        text="REGISTRO DE USUARIO",
        font=("Arial", 11, "bold"),
        bg="#0f172a",
        fg="#38bdf8",
    ).pack(pady=20)

    tk.Label(
        ven_reg, text="Nuevo Usuario:", font=("Arial", 9), bg="#0f172a", fg="white"
    ).pack(anchor="w", padx=30)
    ent_usu = tk.Entry(ven_reg, font=("Arial", 10), width=26)
    ent_usu.pack(pady=2)

    tk.Label(
        ven_reg,
        text="Correo Electrónico:",
        font=("Arial", 9),
        bg="#0f172a",
        fg="white",
    ).pack(anchor="w", padx=30)
    ent_corr = tk.Entry(ven_reg, font=("Arial", 10), width=26)
    ent_corr.pack(pady=2)

    tk.Label(
        ven_reg, text="Contraseña:", font=("Arial", 9), bg="#0f172a", fg="white"
    ).pack(anchor="w", padx=30)
    ent_pass = tk.Entry(ven_reg, font=("Arial", 10), width=26, show="*")
    ent_pass.pack(pady=2)

    def guardar_usuario():
      u = ent_usu.get().strip()
      c = ent_corr.get().strip()
      p = ent_pass.get().strip()

      if not u or not c or not p:
        messagebox.showerror("Error", "Todos los campos son obligatorios.", parent=ven_reg)
        return

      if u in self.usuarios_db:
        messagebox.showerror("Error", "El usuario ya existe.", parent=ven_reg)
        return

      self.usuarios_db[u] = {"password": p, "correo": c}
      messagebox.showinfo("Éxito", "Usuario registrado correctamente.", parent=ven_reg)
      ven_reg.destroy()

    tk.Button(
        ven_reg,
        text="Registrarse",
        font=("Arial", 10, "bold"),
        bg="#0284c7",
        fg="white",
        width=20,
        command=guardar_usuario,
    ).pack(pady=20)

  # --- VENTANA DE RECUPERACIÓN ---
  def ventana_recuperar(self):
    ven_rec = tk.Toplevel(self.root)
    ven_rec.title("Recuperar Contraseña")
    ven_rec.geometry("350x280")
    ven_rec.config(bg="#0f172a")
    ven_rec.resizable(False, False)

    tk.Label(
        ven_rec,
        text="RECUPERAR CONTRASEÑA",
        font=("Arial", 11, "bold"),
        bg="#0f172a",
        fg="#38bdf8",
    ).pack(pady=15)

    # Opciones de método de recuperación
    self.metodo_recu = tk.StringVar(value="usuario")

    tk.Radiobutton(
        ven_rec,
        text="Ingresar mi Usuario",
        variable=self.metodo_recu,
        value="usuario",
        bg="#0f172a",
        fg="white",
        selectcolor="#1e293b",
        font=("Arial", 9),
        command=lambda: actualizar_campo(),
    ).pack(anchor="w", padx=40)

    tk.Radiobutton(
        ven_rec,
        text="Probar otro método (Ingresar Correo)",
        variable=self.metodo_recu,
        value="correo",
        bg="#0f172a",
        fg="white",
        selectcolor="#1e293b",
        font=("Arial", 9),
        command=lambda: actualizar_campo(),
    ).pack(anchor="w", padx=40, pady=5)

    lbl_dinamico = tk.Label(
        ven_rec, text="Escribe tu Usuario:", font=("Arial", 9), bg="#0f172a", fg="white"
    )
    lbl_dinamico.pack(anchor="w", padx=40, pady=(10, 0))

    ent_valor = tk.Entry(ven_rec, font=("Arial", 10), width=28)
    ent_valor.pack(pady=5)

    def actualizar_campo():
      if self.metodo_recu.get() == "usuario":
        lbl_dinamico.config(text="Escribe tu Usuario:")
      else:
        lbl_dinamico.config(text="Escribe tu Correo de Registro:")

    def ejecutar_recuperacion():
      val = ent_valor.get().strip()
      if not val:
        messagebox.showerror("Error", "Este campo no puede estar vacío.", parent=ven_rec)
        return

      encontrado = False
      password_encontrada = ""

      if self.metodo_recu.get() == "usuario":
        if val in self.usuarios_db:
          password_encontrada = self.usuarios_db[val]["password"]
          encontrado = True
      else:
        for usu, datos in self.usuarios_db.items():
          if datos["correo"] == val:
            password_encontrada = datos["password"]
            encontrado = True
            break

      if encontrado:
        messagebox.showinfo(
            "Recuperación exitosa",
            f"Tu contraseña es: {password_encontrada}",
            parent=ven_rec,
        )
        ven_rec.destroy()
      else:
        messagebox.showerror(
            "No encontrado",
            "No se encontró ninguna cuenta con esos datos.",
            parent=ven_rec,
        )

    tk.Button(
        ven_rec,
        text="Buscar Contraseña",
        font=("Arial", 10, "bold"),
        bg="#0284c7",
        fg="white",
        width=22,
        command=ejecutar_recuperacion,
    ).pack(pady=15)


if __name__ == "__main__":
  root = tk.Tk()
  app = SistemaBiomedicoApp(root)
  root.mainloop()