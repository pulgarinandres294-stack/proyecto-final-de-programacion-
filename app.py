import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Nombre del archivo de persistencia
ARCHIVO_USUARIOS = "usuarios.txt"


def cargar_base_datos():
  """Carga los usuarios desde el archivo de texto o crea los valores por defecto."""
  db = {
      "tecnologo_1": {
          "password": "123",
          "correo": "tec1@biomedica.com",
          "rol": "Tecnólogo Biomédico",
      },
      "ingeniero_1": {
          "password": "123",
          "correo": "ing1@biomedica.com",
          "rol": "Ingeniero Biomédico",
      },
      "supervisor_1": {
          "password": "123",
          "correo": "sup1@biomedica.com",
          "rol": "Supervisor",
      },
      "supervisor_2": {
          "password": "123",
          "correo": "sup2@biomedica.com",
          "rol": "Supervisor",
      },
  }

  if os.path.exists(ARCHIVO_USUARIOS):
    try:
      with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
        for linea in f:
          partes = linea.strip().split("::")
          if len(partes) == 4:
            usu, pas, corr, rol = partes
            db[usu] = {"password": pas, "correo": corr, "rol": rol}
    except Exception as e:
      print(f"Error al leer la base de datos: {e}")
  else:
    guardar_base_datos(db)

  return db


def guardar_base_datos(db):
  """Guarda el diccionario actual de usuarios en el archivo de texto."""
  try:
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
      for usu, info in db.items():
        f.write(f"{usu}::{info['password']}::{info['correo']}::{info['rol']}\n")
  except Exception as e:
    print(f"Error al guardar la base de datos: {e}")


# Cargar usuarios al iniciar la aplicación
USUARIOS_DB = cargar_base_datos()


class SistemaBiomedicoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Sistema Biomédico - Inicio de Sesión")
    self.root.geometry("700x350")
    self.root.resizable(False, False)

    # 1. PANEL IZQUIERDO: Carrusel de imágenes
    self.lbl_imagen = tk.Label(root, bg="#ffffff")
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
        img = Image.new("RGB", (350, 350), color="#e2e8f0")
        self.imagenes_pil.append(img)

    self.fotos_carrusel = [
        ImageTk.PhotoImage(img) for img in self.imagenes_pil
    ]
    if self.fotos_carrusel:
      self.lbl_imagen.config(image=self.fotos_carrusel[0])

    self.root.after(5000, self.proximo_slide)

    # 2. PANEL DERECHO: Formulario de inicio de sesión con fondo blanco
    self.frame_form = tk.Frame(root, bg="#ffffff")
    self.frame_form.place(x=350, y=0, width=350, height=350)

    titulo = tk.Label(
        self.frame_form,
        text="SISTEMA BIOMÉDICO",
        font=("Arial", 12, "bold"),
        bg="#ffffff",
        fg="#0284c7",
    )
    titulo.pack(pady=(30, 10))

    lbl_usuario = tk.Label(
        self.frame_form,
        text="Usuario",
        font=("Arial", 9, "bold"),
        bg="#ffffff",
        fg="#334155",
    )
    lbl_usuario.pack(anchor="w", padx=40)
    self.entry_usuario = tk.Entry(
        self.frame_form,
        font=("Arial", 11),
        bg="#f1f5f9",
        fg="#0f172a",
        insertbackground="#0f172a",
        relief="flat",
    )
    self.entry_usuario.pack(fill="x", padx=40, pady=2)

    lbl_password = tk.Label(
        self.frame_form,
        text="Contraseña",
        font=("Arial", 9, "bold"),
        bg="#ffffff",
        fg="#334155",
    )
    lbl_password.pack(anchor="w", padx=40, pady=(6, 0))
    self.entry_password = tk.Entry(
        self.frame_form,
        font=("Arial", 11),
        bg="#f1f5f9",
        fg="#0f172a",
        insertbackground="#0f172a",
        show="*",
        relief="flat",
    )
    self.entry_password.pack(fill="x", padx=40, pady=2)

    btn_olvido = tk.Button(
        self.frame_form,
        text="¿Olvidaste tu contraseña?",
        font=("Arial", 8),
        bg="#ffffff",
        fg="#0284c7",
        activebackground="#ffffff",
        activeforeground="#0369a1",
        bd=0,
        cursor="hand2",
        command=self.ventana_recuperar,
    )
    btn_olvido.pack(anchor="e", padx=40, pady=2)

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
    btn_ingresar.pack(fill="x", padx=40, pady=8)

    btn_registro = tk.Button(
        self.frame_form,
        text="¿No tienes cuenta? Regístrate aquí",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#0284c7",
        activebackground="#ffffff",
        activeforeground="#0369a1",
        bd=0,
        cursor="hand2",
        command=self.ventana_registro,
    )
    btn_registro.pack(pady=2)

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

    if usuario in USUARIOS_DB and USUARIOS_DB[usuario]["password"] == password:
      rol_usuario = USUARIOS_DB[usuario]["rol"]
      self.root.destroy()
      abrir_pantalla_principal(usuario, rol_usuario)
    else:
      messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

  def ventana_registro(self):
    ven_reg = tk.Toplevel(self.root)
    ven_reg.title("Registro de Nuevo Usuario")
    ven_reg.geometry("320x360")
    ven_reg.config(bg="#ffffff")
    ven_reg.resizable(False, False)

    tk.Label(
        ven_reg,
        text="REGISTRO DE USUARIO",
        font=("Arial", 11, "bold"),
        bg="#ffffff",
        fg="#0284c7",
    ).pack(pady=15)

    tk.Label(
        ven_reg,
        text="Usuario (ej. tecnologo_2):",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#334155",
    ).pack(anchor="w", padx=30)
    ent_usu = tk.Entry(
        ven_reg,
        font=("Arial", 10),
        width=26,
        bg="#f1f5f9",
        fg="#0f172a",
        relief="flat",
    )
    ent_usu.pack(pady=2)

    tk.Label(
        ven_reg,
        text="Correo Electrónico:",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#334155",
    ).pack(anchor="w", padx=30)
    ent_corr = tk.Entry(
        ven_reg,
        font=("Arial", 10),
        width=26,
        bg="#f1f5f9",
        fg="#0f172a",
        relief="flat",
    )
    ent_corr.pack(pady=2)

    tk.Label(
        ven_reg,
        text="Contraseña:",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#334155",
    ).pack(anchor="w", padx=30)
    ent_pass = tk.Entry(
        ven_reg,
        font=("Arial", 10),
        width=26,
        show="*",
        bg="#f1f5f9",
        fg="#0f172a",
        relief="flat",
    )
    ent_pass.pack(pady=2)

    tk.Label(
        ven_reg,
        text="Seleccione Rol:",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#334155",
    ).pack(anchor="w", padx=30)
    rol_var = tk.StringVar(value="Tecnólogo Biomédico")
    tk.Radiobutton(
        ven_reg,
        text="Tecnólogo Biomédico",
        variable=rol_var,
        value="Tecnólogo Biomédico",
        bg="#ffffff",
        fg="#334155",
        selectcolor="#f1f5f9",
    ).pack(anchor="w", padx=40)
    tk.Radiobutton(
        ven_reg,
        text="Ingeniero Biomédico",
        variable=rol_var,
        value="Ingeniero Biomédico",
        bg="#ffffff",
        fg="#334155",
        selectcolor="#f1f5f9",
    ).pack(anchor="w", padx=40)
    tk.Radiobutton(
        ven_reg,
        text="Supervisor",
        variable=rol_var,
        value="Supervisor",
        bg="#ffffff",
        fg="#334155",
        selectcolor="#f1f5f9",
    ).pack(anchor="w", padx=40)

    def guardar_usuario():
      u = ent_usu.get().strip()
      c = ent_corr.get().strip()
      p = ent_pass.get().strip()
      r = rol_var.get()

      if not u or not c or not p:
        messagebox.showerror(
            "Error", "Todos los campos son obligatorios.", parent=ven_reg
        )
        return

      if u in USUARIOS_DB:
        messagebox.showerror(
            "Error", "El nombre de usuario ya existe.", parent=ven_reg
        )
        return

      USUARIOS_DB[u] = {"password": p, "correo": c, "rol": r}
      guardar_base_datos(USUARIOS_DB)
      messagebox.showinfo(
          "Éxito", f"Usuario '{u}' registrado como {r}.", parent=ven_reg
      )
      ven_reg.destroy()

    tk.Button(
        ven_reg,
        text="Registrarse",
        font=("Arial", 10, "bold"),
        bg="#0284c7",
        fg="white",
        width=20,
        command=guardar_usuario,
    ).pack(pady=15)

  def ventana_recuperar(self):
    ven_rec = tk.Toplevel(self.root)
    ven_rec.title("Recuperar Contraseña")
    ven_rec.geometry("350x280")
    ven_rec.config(bg="#ffffff")
    ven_rec.resizable(False, False)

    tk.Label(
        ven_rec,
        text="RECUPERAR CONTRASEÑA",
        font=("Arial", 11, "bold"),
        bg="#ffffff",
        fg="#0284c7",
    ).pack(pady=15)

    self.metodo_recu = tk.StringVar(value="usuario")

    tk.Radiobutton(
        ven_rec,
        text="Ingresar mi Usuario",
        variable=self.metodo_recu,
        value="usuario",
        bg="#ffffff",
        fg="#334155",
        selectcolor="#f1f5f9",
        font=("Arial", 9),
        command=lambda: actualizar_campo(),
    ).pack(anchor="w", padx=40)

    tk.Radiobutton(
        ven_rec,
        text="Probar otro método (Ingresar Correo)",
        variable=self.metodo_recu,
        value="correo",
        bg="#ffffff",
        fg="#334155",
        selectcolor="#f1f5f9",
        font=("Arial", 9),
        command=lambda: actualizar_campo(),
    ).pack(anchor="w", padx=40, pady=5)

    lbl_dinamico = tk.Label(
        ven_rec,
        text="Escribe tu Usuario:",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#334155",
    )
    lbl_dinamico.pack(anchor="w", padx=40, pady=(10, 0))

    ent_valor = tk.Entry(
        ven_rec,
        font=("Arial", 10),
        width=28,
        bg="#f1f5f9",
        fg="#0f172a",
        relief="flat",
    )
    ent_valor.pack(pady=5)

    def actualizar_campo():
      if self.metodo_recu.get() == "usuario":
        lbl_dinamico.config(text="Escribe tu Usuario:")
      else:
        lbl_dinamico.config(text="Escribe tu Correo de Registro:")

    def ejecutar_recuperacion():
      val = ent_valor.get().strip()
      if not val:
        messagebox.showerror(
            "Error", "Este campo no puede estar vacío.", parent=ven_rec
        )
        return

      encontrado = False
      password_encontrada = ""

      if self.metodo_recu.get() == "usuario":
        if val in USUARIOS_DB:
          password_encontrada = USUARIOS_DB[val]["password"]
          encontrado = True
      else:
        for usu, datos in USUARIOS_DB.items():
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


# --- PANTALLA PRINCIPAL DINÁMICA CON TEMA CLARO ---
def abrir_pantalla_principal(usuario_activo, rol_activo):
  ventana_principal = tk.Tk()
  ventana_principal.title(f"Sistema Biomédico - {rol_activo}")
  ventana_principal.geometry("780x520")
  ventana_principal.config(bg="#f8fafc")
  ventana_principal.resizable(False, False)

  header = tk.Frame(ventana_principal, bg="#e2e8f0", height=65)
  header.pack(fill="x")

  lbl_bienvenida = tk.Label(
      header,
      text=f"Usuario: {usuario_activo} | Rol: {rol_activo}",
      font=("Arial", 11, "bold"),
      bg="#e2e8f0",
      fg="#0f172a",
  )
  lbl_bienvenida.pack(side="left", padx=20)

  def cerrar_sesion():
    ventana_principal.destroy()
    root_login = tk.Tk()
    SistemaBiomedicoApp(root_login)
    root_login.mainloop()

  btn_salir = tk.Button(
      header,
      text="Cerrar Sesión",
      font=("Arial", 9, "bold"),
      bg="#dc2626",
      fg="white",
      relief="flat",
      cursor="hand2",
      command=cerrar_sesion,
  )
  btn_salir.pack(side="right", padx=20)

  cuerpo = tk.Frame(ventana_principal, bg="#f8fafc")
  cuerpo.pack(fill="both", expand=True, padx=30, pady=15)

  tk.Label(
      cuerpo,
      text="Panel de Control - Gestión de Equipos Biomédicos",
      font=("Arial", 13, "bold"),
      bg="#f8fafc",
      fg="#0f172a",
  ).pack(anchor="w", pady=5)

  def mostrar_accion(mensaje):
    messagebox.showinfo(
        f"Módulo de {rol_activo}",
        f"Accediendo a: {mensaje}\n(Perfil actual: {usuario_activo})",
    )

  # --- VENTANA DE GESTIÓN DE PERFILES CON TEMA CLARO ---
  def gestionar_usuarios():
    ven_gestion = tk.Toplevel(ventana_principal)
    ven_gestion.title("Gestión y Eliminación de Perfiles")
    ven_gestion.geometry("420x360")
    ven_gestion.config(bg="#ffffff")
    ven_gestion.resizable(False, False)

    tk.Label(
        ven_gestion,
        text="PERFILES REGISTRADOS",
        font=("Arial", 11, "bold"),
        bg="#ffffff",
        fg="#0284c7",
    ).pack(pady=15)

    frame_lista = tk.Frame(ven_gestion, bg="#ffffff")
    frame_lista.pack(fill="both", expand=True, padx=20)

    def actualizar_lista():
      for widget in frame_lista.winfo_children():
        widget.destroy()

      for usu, info in list(USUARIOS_DB.items()):
        fila = tk.Frame(frame_lista, bg="#f1f5f9", pady=5)
        fila.pack(fill="x", pady=3)

        lbl_info = tk.Label(
            fila,
            text=f"{usu} ({info['rol']})",
            font=("Arial", 9, "bold"),
            bg="#f1f5f9",
            fg="#0f172a",
        )
        lbl_info.pack(side="left", padx=10)

        puede_borrar = True
        etiqueta_estado = ""

        if usu == usuario_activo:
          puede_borrar = False
          etiqueta_estado = "(Actual)"
        elif info["rol"] == "Supervisor" and usuario_activo != "supervisor_1":
          puede_borrar = False
          etiqueta_estado = "(Protegido)"

        if puede_borrar:
          btn_borrar = tk.Button(
              fila,
              text="Eliminar",
              font=("Arial", 8, "bold"),
              bg="#dc2626",
              fg="white",
              relief="flat",
              command=lambda u=usu: confirmar_eliminacion(u),
          )
          btn_borrar.pack(side="right", padx=10)
        else:
          lbl_tag = tk.Label(
              fila,
              text=etiqueta_estado,
              font=("Arial", 8),
              bg="#f1f5f9",
              fg="#64748b",
          )
          lbl_tag.pack(side="right", padx=10)

    def confirmar_eliminacion(u):
      if messagebox.askyesno(
          "Confirmar",
          f"¿Estás seguro de eliminar permanentemente el perfil de '{u}'?",
          parent=ven_gestion,
      ):
        if u in USUARIOS_DB:
          del USUARIOS_DB[u]
          guardar_base_datos(USUARIOS_DB)
          messagebox.showinfo(
              "Eliminado",
              f"El perfil '{u}' fue borrado con éxito.",
              parent=ven_gestion,
          )
          actualizar_lista()

    actualizar_lista()

  # --- OPCIONES DE ÁREAS MÉDICAS (UCI Y NEONATOLOGÍA) ---
  tk.Label(
      cuerpo,
      text="Áreas de Especialización Médica:",
      font=("Arial", 10, "bold"),
      bg="#f8fafc",
      fg="#0284c7",
  ).pack(anchor="w", pady=(5, 2))

  tk.Button(
      cuerpo,
      text="🏥 Equipos de Cuidados Intensivos (UCI)",
      font=("Arial", 9, "bold"),
      bg="#0284c7",
      fg="white",
      activebackground="#0369a1",
      activeforeground="white",
      relief="flat",
      width=45,
      anchor="w",
      padx=10,
      command=lambda: mostrar_accion(
          "Gestión de equipos en Cuidados Intensivos (Ventiladores, Monitores, etc.)"
      ),
  ).pack(pady=3)

  tk.Button(
      cuerpo,
      text="👶 Equipos de Neonatología",
      font=("Arial", 9, "bold"),
      bg="#0284c7",
      fg="white",
      activebackground="#0369a1",
      activeforeground="white",
      relief="flat",
      width=45,
      anchor="w",
      padx=10,
      command=lambda: mostrar_accion(
          "Gestión de equipos en Neonatología (Incubadoras, Cunas radiantes, etc.)"
      ),
  ).pack(pady=3)

  tk.Label(
      cuerpo,
      text="Herramientas de Rol:",
      font=("Arial", 10, "bold"),
      bg="#f8fafc",
      fg="#0284c7",
  ).pack(anchor="w", pady=(8, 2))

  # --- OPCIONES SEGÚN EL ROL ---
  if rol_activo == "Tecnólogo Biomédico":
    tk.Button(
        cuerpo,
        text="📅 Registrar Fechas y Proceso de Mantenimiento",
        font=("Arial", 9, "bold"),
        bg="#e2e8f0",
        fg="#0f172a",
        activebackground="#cbd5e1",
        activeforeground="#0f172a",
        relief="flat",
        width=45,
        anchor="w",
        padx=10,
        command=lambda: mostrar_accion(
            "Registro de fechas, observaciones y proceso operativo"
        ),
    ).pack(pady=3)

    tk.Button(
        cuerpo,
        text="📝 Agregar Observaciones Técnicas",
        font=("Arial", 9, "bold"),
        bg="#e2e8f0",
        fg="#0f172a",
        activebackground="#cbd5e1",
        activeforeground="#0f172a",
        relief="flat",
        width=45,
        anchor="w",
        padx=10,
        command=lambda: mostrar_accion("Agregar observaciones de mantenimiento"),
    ).pack(pady=3)

  elif rol_activo in ["Ingeniero Biomédico", "Supervisor"]:
    tk.Button(
        cuerpo,
        text="👁️ Ver y Auditar Registros de Tecnólogos",
        font=("Arial", 9, "bold"),
        bg="#e2e8f0",
        fg="#0f172a",
        activebackground="#cbd5e1",
        activeforeground="#0f172a",
        relief="flat",
        width=45,
        anchor="w",
        padx=10,
        command=lambda: mostrar_accion(
            "Visualización y revisión de trabajos de los tecnólogos"
        ),
    ).pack(pady=3)

    tk.Button(
        cuerpo,
        text="✏️ Editar, Corregir y Analizar Mantenimientos",
        font=("Arial", 9, "bold"),
        bg="#e2e8f0",
        fg="#0f172a",
        activebackground="#cbd5e1",
        activeforeground="#0f172a",
        relief="flat",
        width=45,
        anchor="w",
        padx=10,
        command=lambda: mostrar_accion(
            "Edición de registros y emisión de análisis ingenieril"
        ),
    ).pack(pady=3)

    tk.Button(
        cuerpo,
        text="💰 Gestión de Presupuestos de Equipos Médicos",
        font=("Arial", 9, "bold"),
        bg="#e2e8f0",
        fg="#0f172a",
        activebackground="#cbd5e1",
        activeforeground="#0f172a",
        relief="flat",
        width=45,
        anchor="w",
        padx=10,
        command=lambda: mostrar_accion(
            "Control y revisión de presupuestos de máquinas biomédicas"
        ),
    ).pack(pady=3)

    if rol_activo == "Supervisor":
      tk.Button(
          cuerpo,
          text="👥 Gestionar y Eliminar Perfiles de Usuario",
          font=("Arial", 9, "bold"),
          bg="#b91c1c",
          fg="white",
          activebackground="#991b1b",
          activeforeground="white",
          relief="flat",
          width=45,
          anchor="w",
          padx=10,
          command=gestionar_usuarios,
      ).pack(pady=3)

  ventana_principal.mainloop()


if __name__ == "__main__":
  root = tk.Tk()
  app = SistemaBiomedicoApp(root)
  root.mainloop()