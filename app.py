from datetime import datetime, timedelta
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Archivos de persistencia
ARCHIVO_USUARIOS = "usuarios.txt"
ARCHIVO_EQUIPOS = "equipos_biomedicos.txt"


def cargar_base_datos():
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
      print(f"Error al leer la base de datos de usuarios: {e}")
  else:
    guardar_base_datos_usuarios(db)

  return db


def guardar_base_datos_usuarios(db):
  try:
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
      for usu, info in db.items():
        f.write(f"{usu}::{info['password']}::{info['correo']}::{info['rol']}\n")
  except Exception as e:
    print(f"Error al guardar usuarios: {e}")


def cargar_equipos():
  equipos = []
  if os.path.exists(ARCHIVO_EQUIPOS):
    try:
      with open(ARCHIVO_EQUIPOS, "r", encoding="utf-8") as f:
        for linea in f:
          partes = linea.strip().split("::")
          if len(partes) >= 8:
            equipos.append({
                "area": partes[0],
                "nombre": partes[1],
                "serial": partes[2],
                "modelo": partes[3],
                "funciones": partes[4],
                "ultimo_registro": partes[5],
                "prox_mant": partes[6],
                "prox_calib": partes[7],
                "observaciones": (
                    partes[8] if len(partes) > 8 else "Sin observaciones"
                ),
            })
    except Exception as e:
      print(f"Error al leer equipos: {e}")
  return equipos


def guardar_equipos(equipos):
  try:
    with open(ARCHIVO_EQUIPOS, "w", encoding="utf-8") as f:
      for eq in equipos:
        obs = eq.get("observaciones", "Sin observaciones")
        f.write(
            f"{eq['area']}::{eq['nombre']}::{eq['serial']}::{eq['modelo']}::{eq['funciones']}::{eq['ultimo_registro']}::{eq['prox_mant']}::{eq['prox_calib']}::{obs}\n"
        )
  except Exception as e:
    print(f"Error al guardar equipos: {e}")


USUARIOS_DB = cargar_base_datos()


class SistemaBiomedicoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Sistema Biomédico - Inicio de Sesión")
    self.root.geometry("700x350")
    self.root.resizable(False, False)

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
      self.root.withdraw()
      abrir_pantalla_principal(usuario, rol_usuario, self.root)
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
      guardar_base_datos_usuarios(USUARIOS_DB)
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


def abrir_ventana_herramienta(
    accion_titulo, area_nombre, usuario_activo, rol_activo
):
  ven_herramienta = tk.Toplevel()
  ven_herramienta.title(f"Herramienta: {accion_titulo} - {area_nombre}")
  ven_herramienta.geometry("850x550")
  ven_herramienta.config(bg="#f1f5f9")
  ven_herramienta.resizable(False, False)

  header = tk.Frame(ven_herramienta, bg="#0f172a", height=55)
  header.pack(fill="x")
  tk.Label(
      header,
      text=f"⚙️ {accion_titulo} | Área: {area_nombre} | Usuario: {usuario_activo}",
      font=("Arial", 10, "bold"),
      bg="#0f172a",
      fg="#38bdf8",
  ).pack(side="left", padx=20)

  cuerpo = tk.Frame(ven_herramienta, bg="#f1f5f9")
  cuerpo.pack(fill="both", expand=True, padx=20, pady=15)

  frame_notif = tk.Frame(
      cuerpo, bg="#eff6ff", bd=1, relief="solid", padx=15, pady=10
  )
  frame_notif.pack(fill="x", pady=(0, 10))

  tk.Label(
      frame_notif,
      text="🔔 Notificaciones y Estado de Mantenimiento / Calibración:",
      font=("Arial", 10, "bold"),
      bg="#eff6ff",
      fg="#1e40af",
  ).pack(anchor="w", pady=(0, 5))

  lbl_estado_alertas = tk.Label(
      frame_notif,
      text="Analizando equipos y fechas programadas...",
      font=("Arial", 9),
      bg="#eff6ff",
      fg="#334155",
      justify="left",
  )
  lbl_estado_alertas.pack(anchor="w")

  frame_inv = tk.Frame(cuerpo, bg="#ffffff", bd=1, relief="solid")
  frame_inv.pack(fill="both", expand=True)

  tk.Label(
      frame_inv,
      text=f"📋 Equipos Registrados en {area_nombre} para {accion_titulo}",
      font=("Arial", 11, "bold"),
      bg="#ffffff",
      fg="#0f172a",
  ).pack(anchor="w", padx=15, pady=10)

  canvas_h = tk.Canvas(frame_inv, bg="#ffffff", highlightthickness=0)
  canvas_h.pack(fill="both", expand=True, padx=15, pady=5)

  scroll_h = tk.Scrollbar(
      frame_inv, orient="vertical", command=canvas_h.yview
  )
  scroll_h.pack(side="right", fill="y")
  canvas_h.configure(yscrollcommand=scroll_h.set)

  frame_items_h = tk.Frame(canvas_h, bg="#ffffff")
  canvas_h.create_window((0, 0), window=frame_items_h, anchor="nw")

  lista_equipos = cargar_equipos()

  def actualizar_datos_herramienta():
    for widget in frame_items_h.winfo_children():
      widget.destroy()

    filtrados = [eq for eq in lista_equipos if eq["area"] == area_nombre]
    hoy = datetime.now().date()
    mensajes_alerta = []

    if not filtrados:
      tk.Label(
          frame_items_h,
          text="No hay equipos registrados en esta área para gestionar.",
          font=("Arial", 10),
          bg="#ffffff",
          fg="#64748b",
      ).pack(pady=30)
      lbl_estado_alertas.config(
          text="✅ No hay equipos registrados. Todo en orden."
      )
      return

    for eq in filtrados:
      try:
        f_mant = datetime.strptime(eq["prox_mant"], "%Y-%m-%d").date()
        dias_mant = (f_mant - hoy).days
        if dias_mant <= 5:
          mensajes_alerta.append(
              f"⚠️ ALERTA: '{eq['nombre']}' (Serial: {eq['serial']}) requiere"
              f" Mantenimiento pronto ({eq['prox_mant']})."
          )
      except Exception:
        pass

      tarjeta = tk.Frame(
          frame_items_h, bg="#f8fafc", bd=1, relief="solid", padx=10, pady=8
      )
      tarjeta.pack(fill="x", pady=4, padx=5)

      info = (
          f"Máquina: {eq['nombre']}  |  Modelo: {eq['modelo']}  |  Serial:"
          f" {eq['serial']}\nFunciones: {eq['funciones']}\n🕒 Último Registro:"
          f" {eq['ultimo_registro']}   |   📅 Próx. Mant: {eq['prox_mant']}  "
          f" |   🔧 Próx. Calib: {eq['prox_calib']}\n📝 Observaciones:"
          f" {eq.get('observaciones', 'Sin observaciones')}"
      )

      lbl_info = tk.Label(
          tarjeta,
          text=info,
          font=("Arial", 9),
          bg="#f8fafc",
          fg="#0f172a",
          justify="left",
      )
      lbl_info.pack(side="left")

      btn_accion = tk.Button(
          tarjeta,
          text="Actualizar / Observación",
          font=("Arial", 8, "bold"),
          bg="#0284c7",
          fg="white",
          relief="flat",
          cursor="hand2",
          command=lambda s=eq["serial"]: abrir_modal_actualizar(s),
      )
      btn_accion.pack(side="right", padx=5)

    if mensajes_alerta:
      lbl_estado_alertas.config(text="\n".join(mensajes_alerta), fg="#b91c1c")
    else:
      lbl_estado_alertas.config(
          text="✅ Todos los equipos de esta área tienen sus fechas al día.",
          fg="#15803d",
      )

    frame_items_h.update_idletasks()
    canvas_h.config(scrollregion=canvas_h.bbox("all"))

  def abrir_modal_actualizar(serial):
    ven_mod = tk.Toplevel(ven_herramienta)
    ven_mod.title(f"Gestionar Equipo - Serial {serial}")
    ven_mod.geometry("380x300")
    ven_mod.config(bg="#ffffff")
    ven_mod.resizable(False, False)

    tk.Label(
        ven_mod,
        text=f"Actualizar Registro ({accion_titulo})",
        font=("Arial", 10, "bold"),
        bg="#ffffff",
        fg="#0284c7",
    ).pack(pady=10)

    tk.Label(
        ven_mod,
        text="Nuevas Observaciones o Notas Técnicas:",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#334155",
    ).pack(anchor="w", padx=25)
    ent_obs = tk.Entry(ven_mod, font=("Arial", 10), width=30)
    ent_obs.pack(pady=5)

    tk.Label(
        ven_mod,
        text="Nueva Fecha Próx. Mantenimiento (AAAA-MM-DD):",
        font=("Arial", 9),
        bg="#ffffff",
        fg="#334155",
    ).pack(anchor="w", padx=25)
    ent_m = tk.Entry(ven_mod, font=("Arial", 10), width=30)
    ent_m.pack(pady=5)

    def guardar_actualizacion():
      nueva_obs = ent_obs.get().strip()
      nuevo_m = ent_m.get().strip()

      for eq in lista_equipos:
        if eq["serial"] == serial:
          if nueva_obs:
            eq["observaciones"] = f"[{usuario_activo}]: {nueva_obs}"
          if nuevo_m:
            eq["prox_mant"] = nuevo_m
          eq["ultimo_registro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          break

      guardar_equipos(lista_equipos)
      messagebox.showinfo(
          "Actualizado",
          "El equipo ha sido actualizado con éxito.",
          parent=ven_mod,
      )
      ven_mod.destroy()
      actualizar_datos_herramienta()

    tk.Button(
        ven_mod,
        text="Guardar Cambios",
        font=("Arial", 9, "bold"),
        bg="#0284c7",
        fg="white",
        width=20,
        command=guardar_actualizacion,
    ).pack(pady=15)

  actualizar_datos_herramienta()


def abrir_ventana_area(area_nombre, usuario_activo, rol_activo, root_login):
  ven_area = tk.Toplevel()
  ven_area.title(f"Zona Clínica - {area_nombre}")
  ven_area.geometry("900x580")
  ven_area.config(bg="#f1f5f9")
  ven_area.resizable(False, False)

  header = tk.Frame(ven_area, bg="#0f172a", height=55)
  header.pack(fill="x")
  tk.Label(
      header,
      text=f"🏥 Área: {area_nombre}   |   Usuario: {usuario_activo} ({rol_activo})",
      font=("Arial", 11, "bold"),
      bg="#0f172a",
      fg="#38bdf8",
  ).pack(side="left", padx=20)

  def cerrar_zona():
    ven_area.destroy()
    abrir_pantalla_principal(usuario_activo, rol_activo, root_login)

  tk.Button(
      header,
      text="⬅ Volver al Panel",
      font=("Arial", 9, "bold"),
      bg="#334155",
      fg="white",
      relief="flat",
      cursor="hand2",
      command=cerrar_zona,
  ).pack(side="right", padx=20)

  cuerpo = tk.Frame(ven_area, bg="#f1f5f9")
  cuerpo.pack(fill="both", expand=True, padx=20, pady=15)

  lista_equipos = cargar_equipos()

  def verificar_alertas():
    hoy = datetime.now().date()
    alertas = []
    for eq in lista_equipos:
      if eq["area"] == area_nombre:
        try:
          f_mant = datetime.strptime(eq["prox_mant"], "%Y-%m-%d").date()
          dias_mant = (f_mant - hoy).days
          if dias_mant <= 5:
            alertas.append(
                f"⚠️ El equipo '{eq['nombre']}' (Serial: {eq['serial']}) tiene"
                f" su Mantenimiento próximo o vencido ({eq['prox_mant']})."
            )
        except Exception:
          pass
    if alertas:
      messagebox.showwarning(
          "🚨 Alerta de Mantenimiento", "\n".join(alertas), parent=ven_area
      )
    else:
      messagebox.showinfo(
          "Estado de Alertas",
          "No hay equipos con alertas críticas próximas en esta zona.",
          parent=ven_area,
      )

  def ventana_registrar_equipo():
    ven_reg_eq = tk.Toplevel(ven_area)
    ven_reg_eq.title(f"Registrar Equipo en {area_nombre}")
    ven_reg_eq.geometry("400x420")
    ven_reg_eq.config(bg="#ffffff")
    ven_reg_eq.resizable(False, False)

    tk.Label(
        ven_reg_eq,
        text="NUEVO EQUIPO BIOMÉDICO",
        font=("Arial", 11, "bold"),
        bg="#ffffff",
        fg="#0284c7",
    ).pack(pady=12)

    campos = [
        ("Nombre de la Máquina:", "entry_nombre"),
        ("Número de Serie:", "entry_serial"),
        ("Modelo:", "entry_modelo"),
        ("Funciones Clínicas:", "entry_funciones"),
        ("Próximo Mantenimiento (AAAA-MM-DD):", "entry_mant"),
        ("Próxima Calibración (AAAA-MM-DD):", "entry_calib"),
    ]

    entries = {}
    for label_text, key in campos:
      tk.Label(
          ven_reg_eq,
          text=label_text,
          font=("Arial", 9),
          bg="#ffffff",
          fg="#334155",
      ).pack(anchor="w", padx=30)
      ent = tk.Entry(
          ven_reg_eq,
          font=("Arial", 10),
          width=32,
          bg="#f1f5f9",
          fg="#0f172a",
          relief="flat",
      )
      ent.pack(pady=2)
      entries[key] = ent

    def guardar_nuevo_equipo():
      nombre = entries["entry_nombre"].get().strip()
      serial = entries["entry_serial"].get().strip()
      modelo = entries["entry_modelo"].get().strip()
      funciones = entries["entry_funciones"].get().strip()
      mant = entries["entry_mant"].get().strip()
      calib = entries["entry_calib"].get().strip()

      if not nombre or not serial or not modelo or not mant or not calib:
        messagebox.showerror(
            "Error",
            "Todos los campos principales y fechas son obligatorios.",
            parent=ven_reg_eq,
        )
        return

      ultimo_reg = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      nuevo = {
          "area": area_nombre,
          "nombre": nombre,
          "serial": serial,
          "modelo": modelo,
          "funciones": funciones if funciones else "N/A",
          "ultimo_registro": ultimo_reg,
          "prox_mant": mant,
          "prox_calib": calib,
          "observaciones": "Registrado inicialmente",
      }

      lista_equipos.append(nuevo)
      guardar_equipos(lista_equipos)
      messagebox.showinfo(
          "Éxito", "Equipo registrado correctamente.", parent=ven_reg_eq
      )
      ven_reg_eq.destroy()
      actualizar_tabla()

    tk.Button(
        ven_reg_eq,
        text="Guardar Equipo",
        font=("Arial", 10, "bold"),
        bg="#0284c7",
        fg="white",
        width=25,
        command=guardar_nuevo_equipo,
    ).pack(pady=15)

  frame_herramientas = tk.Frame(
      cuerpo, bg="#ffffff", bd=1, relief="solid", padx=15, pady=10
  )
  frame_herramientas.pack(fill="x", pady=(0, 10))

  tk.Label(
      frame_herramientas,
      text=f"🛠️ Herramientas de Gestión ({rol_activo}) en esta Zona:",
      font=("Arial", 10, "bold"),
      bg="#ffffff",
      fg="#0f172a",
  ).pack(anchor="w", pady=(0, 5))

  sub_tools_frame = tk.Frame(frame_herramientas, bg="#ffffff")
  sub_tools_frame.pack(fill="x")

  if rol_activo == "Tecnólogo Biomédico":
    tk.Button(
        sub_tools_frame,
        text="📅 Registrar Fechas y Procesos Operativos",
        font=("Arial", 9, "bold"),
        bg="#334155",
        fg="white",
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=5,
        command=lambda: abrir_ventana_herramienta(
            "Registro de Fechas y Procesos",
            area_nombre,
            usuario_activo,
            rol_activo,
        ),
    ).pack(side="left", padx=5)

    tk.Button(
        sub_tools_frame,
        text="📝 Agregar Observaciones Técnicas",
        font=("Arial", 9, "bold"),
        bg="#334155",
        fg="white",
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=5,
        command=lambda: abrir_ventana_herramienta(
            "Observaciones Técnicas", area_nombre, usuario_activo, rol_activo
        ),
    ).pack(side="left", padx=5)

  elif rol_activo in ["Ingeniero Biomédico", "Supervisor"]:
    tk.Button(
        sub_tools_frame,
        text="👁️ Auditar Registros",
        font=("Arial", 9, "bold"),
        bg="#334155",
        fg="white",
        relief="flat",
        cursor="hand2",
        padx=8,
        pady=5,
        command=lambda: abrir_ventana_herramienta(
            "Auditoría de Registros", area_nombre, usuario_activo, rol_activo
        ),
    ).pack(side="left", padx=3)

    tk.Button(
        sub_tools_frame,
        text="✏️ Editar y Analizar Mantenimientos",
        font=("Arial", 9, "bold"),
        bg="#334155",
        fg="white",
        relief="flat",
        cursor="hand2",
        padx=8,
        pady=5,
        command=lambda: abrir_ventana_herramienta(
            "Análisis y Edición de Mantenimiento",
            area_nombre,
            usuario_activo,
            rol_activo,
        ),
    ).pack(side="left", padx=3)

    tk.Button(
        sub_tools_frame,
        text="💰 Presupuestos Médicos",
        font=("Arial", 9, "bold"),
        bg="#334155",
        fg="white",
        relief="flat",
        cursor="hand2",
        padx=8,
        pady=5,
        command=lambda: abrir_ventana_herramienta(
            "Control de Presupuestos", area_nombre, usuario_activo, rol_activo
        ),
    ).pack(side="left", padx=3)

  tk.Button(
      sub_tools_frame,
      text="➕ Registrar Equipo",
      font=("Arial", 9, "bold"),
      bg="#0284c7",
      fg="white",
      relief="flat",
      cursor="hand2",
      padx=8,
      pady=5,
      command=ventana_registrar_equipo,
  ).pack(side="right", padx=3)

  tk.Button(
      sub_tools_frame,
      text="🔔 Alertas",
      font=("Arial", 9, "bold"),
      bg="#d97706",
      fg="white",
      relief="flat",
      cursor="hand2",
      padx=8,
      pady=5,
      command=verificar_alertas,
  ).pack(side="right", padx=3)

  frame_tabla_contenedor = tk.Frame(cuerpo, bg="#ffffff", bd=1, relief="solid")
  frame_tabla_contenedor.pack(fill="both", expand=True)

  tk.Label(
      frame_tabla_contenedor,
      text=f"📋 Inventario y Registro de Equipos en {area_nombre}",
      font=("Arial", 11, "bold"),
      bg="#ffffff",
      fg="#0f172a",
  ).pack(anchor="w", padx=15, pady=10)

  canvas_tabla = tk.Canvas(
      frame_tabla_contenedor, bg="#ffffff", highlightthickness=0
  )
  canvas_tabla.pack(fill="both", expand=True, padx=15, pady=5)

  scroll_tabla = tk.Scrollbar(
      frame_tabla_contenedor, orient="vertical", command=canvas_tabla.yview
  )
  scroll_tabla.pack(side="right", fill="y")
  canvas_tabla.configure(yscrollcommand=scroll_tabla.set)

  frame_items = tk.Frame(canvas_tabla, bg="#ffffff")
  canvas_tabla.create_window((0, 0), window=frame_items, anchor="nw")

  def actualizar_tabla():
    for widget in frame_items.winfo_children():
      widget.destroy()

    filtrados = [eq for eq in lista_equipos if eq["area"] == area_nombre]

    if not filtrados:
      tk.Label(
          frame_items,
          text="No hay equipos registrados en esta área todavía.",
          font=("Arial", 10),
          bg="#ffffff",
          fg="#64748b",
      ).pack(pady=30)
      return

    for eq in filtrados:
      tarjeta_eq = tk.Frame(
          frame_items, bg="#f8fafc", bd=1, relief="solid", padx=10, pady=8
      )
      tarjeta_eq.pack(fill="x", pady=4, padx=5)

      info_texto = (
          f"Máquina: {eq['nombre']}  |  Modelo: {eq['modelo']}  |  Serial:"
          f" {eq['serial']}\nFunciones: {eq['funciones']}\n🕒 Último Registro:"
          f" {eq['ultimo_registro']}   |   📅 Próx. Mant: {eq['prox_mant']}  "
          f" |   🔧 Próx. Calib: {eq['prox_calib']}"
      )

      lbl_detalles = tk.Label(
          tarjeta_eq,
          text=info_texto,
          font=("Arial", 9),
          bg="#f8fafc",
          fg="#0f172a",
          justify="left",
      )
      lbl_detalles.pack(side="left")

      if rol_activo in ["Ingeniero Biomédico", "Supervisor"]:
        btn_borrar_eq = tk.Button(
            tarjeta_eq,
            text="Eliminar",
            font=("Arial", 8, "bold"),
            bg="#ef4444",
            fg="white",
            relief="flat",
            command=lambda s=eq["serial"]: eliminar_equipo(s),
        )
        btn_borrar_eq.pack(side="right", padx=5)

    frame_items.update_idletasks()
    canvas_tabla.config(scrollregion=canvas_tabla.bbox("all"))

  def eliminar_equipo(serial):
    if messagebox.askyesno(
        "Confirmar",
        f"¿Desea eliminar el equipo con serial {serial}?",
        parent=ven_area,
    ):
      nonlocal lista_equipos
      lista_equipos = [eq for eq in lista_equipos if eq["serial"] != serial]
      guardar_equipos(lista_equipos)
      actualizar_tabla()

  actualizar_tabla()


def abrir_pantalla_principal(usuario_activo, rol_activo, root_login):
  ventana_principal = tk.Toplevel()
  ventana_principal.title(f"Sistema Biomédico - {rol_activo}")
  ventana_principal.geometry("750x450")
  ventana_principal.config(bg="#f1f5f9")
  ventana_principal.resizable(False, False)

  header = tk.Frame(ventana_principal, bg="#0f172a", height=60)
  header.pack(fill="x")

  lbl_titulo_app = tk.Label(
      header,
      text="🏥 SELECCIÓN DE ZONA CLÍNICA",
      font=("Arial", 11, "bold"),
      bg="#0f172a",
      fg="#38bdf8",
  )
  lbl_titulo_app.pack(side="left", padx=20)

  def cerrar_sesion():
    ventana_principal.destroy()
    root_login.deiconify()

  btn_salir = tk.Button(
      header,
      text="Cerrar Sesión",
      font=("Arial", 9, "bold"),
      bg="#ef4444",
      fg="white",
      relief="flat",
      cursor="hand2",
      command=cerrar_sesion,
  )
  btn_salir.pack(side="right", padx=20)

  sub_header = tk.Frame(ventana_principal, bg="#ffffff", height=45)
  sub_header.pack(fill="x", pady=(0, 15))

  lbl_bienvenida = tk.Label(
      sub_header,
      text=f"Usuario: {usuario_activo}   |   Rol: {rol_activo}",
      font=("Arial", 10),
      bg="#ffffff",
      fg="#475569",
  )
  lbl_bienvenida.pack(side="left", padx=25)

  cuerpo = tk.Frame(ventana_principal, bg="#f1f5f9")
  cuerpo.pack(fill="both", expand=True, padx=40, pady=10)

  tk.Label(
      cuerpo,
      text="Seleccione el área hospitalaria a gestionar:",
      font=("Arial", 12, "bold"),
      bg="#f1f5f9",
      fg="#0f172a",
  ).pack(anchor="w", pady=(0, 15))

  def ingresar_zona(nombre_area):
    ventana_principal.destroy()
    abrir_ventana_area(nombre_area, usuario_activo, rol_activo, root_login)

  btn_uci = tk.Button(
      cuerpo,
      text=(
          "🏥 Cuidados Intensivos (UCI)\n(Gestión de equipos, ventiladores,"
          " monitores y herramientas de rol)"
      ),
      font=("Arial", 10, "bold"),
      bg="#0284c7",
      fg="white",
      activebackground="#0369a1",
      activeforeground="white",
      relief="flat",
      cursor="hand2",
      justify="left",
      padx=15,
      pady=12,
      command=lambda: ingresar_zona("Cuidados Intensivos (UCI)"),
  )
  btn_uci.pack(fill="x", pady=8)

  btn_neo = tk.Button(
      cuerpo,
      text=(
          "👶 Neonatología\n(Gestión de incubadoras, cunas radiantes y"
          " herramientas de rol)"
      ),
      font=("Arial", 10, "bold"),
      bg="#0284c7",
      fg="white",
      activebackground="#0369a1",
      activeforeground="white",
      relief="flat",
      cursor="hand2",
      justify="left",
      padx=15,
      pady=12,
      command=lambda: ingresar_zona("Neonatología"),
  )
  btn_neo.pack(fill="x", pady=8)

  def gestionar_usuarios():
    ven_gestion = tk.Toplevel(ventana_principal)
    ven_gestion.title("Gestión y Eliminación de Perfiles")
    ven_gestion.geometry("420x380")
    ven_gestion.config(bg="#ffffff")
    ven_gestion.resizable(False, False)

    tk.Label(
        ven_gestion,
        text="GESTIÓN DE PERFILES DE USUARIO",
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
        fila = tk.Frame(frame_lista, bg="#f8fafc", pady=6, padx=5)
        fila.pack(fill="x", pady=3)

        lbl_info = tk.Label(
            fila,
            text=f"{usu} ({info['rol']})",
            font=("Arial", 9, "bold"),
            bg="#f8fafc",
            fg="#0f172a",
        )
        lbl_info.pack(side="left", padx=5)

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
              bg="#ef4444",
              fg="white",
              relief="flat",
              cursor="hand2",
              command=lambda u=usu: confirmar_eliminacion(u),
          )
          btn_borrar.pack(side="right", padx=5)
        else:
          lbl_tag = tk.Label(
              fila,
              text=etiqueta_estado,
              font=("Arial", 8),
              bg="#f8fafc",
              fg="#64748b",
          )
          lbl_tag.pack(side="right", padx=5)

    def confirmar_eliminacion(u):
      if messagebox.askyesno(
          "Confirmar",
          f"¿Estás seguro de eliminar permanentemente el perfil de '{u}'?",
          parent=ven_gestion,
      ):
        if u in USUARIOS_DB:
          del USUARIOS_DB[u]
          guardar_base_datos_usuarios(USUARIOS_DB)
          messagebox.showinfo(
              "Eliminado",
              f"El perfil '{u}' fue borrado con éxito.",
              parent=ven_gestion,
          )
          actualizar_lista()

    actualizar_lista()

  if rol_activo == "Supervisor":
    tk.Button(
        cuerpo,
        text="👥 Gestionar y Eliminar Perfiles de Usuario",
        font=("Arial", 9, "bold"),
        bg="#dc2626",
        fg="white",
        activebackground="#b91c1c",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=8,
        command=gestionar_usuarios,
    ).pack(fill="x", pady=(15, 0))


if __name__ == "__main__":
  root = tk.Tk()
  app = SistemaBiomedicoApp(root)
  root.mainloop()