import os
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from main import generar_factura_completa
from dotenv import load_dotenv
from datetime import datetime
import sys

def resource_path(relative_path):
    """ Obtiene la ruta absoluta de los archivos para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


load_dotenv()
#configuramos el estilo visual
ctk.set_appearance_mode("dark") #modo nocturno
ctk.set_default_color_theme("blue") #Tema Azul

class InvoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Invoice System")
        self.geometry("1200x1000")

        # 1. Configuración de la cuadrícula principal
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)

        # 2. SIDEBAR (Panel Izquierdo)
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky='nswe')
        self.sidebar_frame.grid_rowconfigure(7, weight=0) 
        try:
            img_original = Image.open("logo.png")
            
            # Guardamos la imagen en self.logo_image para que no desaparezca
            self.logo_image = ctk.CTkImage(light_image=img_original,
                                         dark_image=img_original,
                                         size=(120, 30))

            # 3. Creamos el Label Y LO UBICAMOS con .grid() 📍
            self.label_logo = ctk.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
            self.label_logo.grid(row=0, column=0, padx=20, pady=(20, 0)) # Fila 0            
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            # --- BOTÓN PARA ABRIR CARPETA 
        self.btn_folder = ctk.CTkButton(
            self.sidebar_frame, 
            text="📂 Abrir Inv", 
            command=self.abrir_carpeta_historial, # Llamamos a una función
            fg_color="#5D6D7E",
            hover_color="#34495E"
        )
        self.btn_folder.grid(row=8, column=0, padx=20, pady=10)

        
        # Elementos del Side Bar (Panel Derecho)
        self.label_titulo = ctk.CTkLabel(self.sidebar_frame, text="FACTURACIÓN", font=("Roboto", 24, "bold"))
        self.label_titulo.grid(row=1, column=0, padx=20, pady=20)

        self.label_invoice = ctk.CTkLabel(self.sidebar_frame, text="Próximo número de Invoice:")
        self.label_invoice.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.entry_invoice = ctk.CTkEntry(self.sidebar_frame, width=150)
        self.entry_invoice.grid(row=3, column=0, padx=20, pady=(0, 10))
        self.cargar_numero_inicial()

        self.label_tarifa = ctk.CTkLabel(self.sidebar_frame, text="Tarifa por hora (CAD):")
        self.label_tarifa.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.entry_tarifa = ctk.CTkEntry(self.sidebar_frame)
        self.entry_tarifa.grid(row=5, column=0, padx=20, pady=(0, 10))
        
        tarifa_env = os.getenv("TARIFA_HORA")
        if tarifa_env: self.entry_tarifa.insert(0, tarifa_env)

        self.label_email = ctk.CTkLabel(self.sidebar_frame, text="Correo del cliente:")
        self.label_email.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.entry_email = ctk.CTkEntry(self.sidebar_frame, width=250)
        self.entry_email.grid(row=7, column=0, padx=20, pady=(0, 20))

        self.sidebar_frame.grid_rowconfigure(8,weight=1)
        
        email_env = os.getenv("MI_CORREO")
        if email_env: self.entry_email.insert(0, email_env)

        # 3. ÁREA PRINCIPAL (Panel Derecho) - ¡IMPORTANTE CREARLO ANTES DE USARLO!
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(5, weight=1)

        # --- Elementos del Main Frame ---
        self.label_desc = ctk.CTkLabel(self.main_frame, text="Descripción del servicio:", font=("Roboto", 14))
        self.label_desc.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        self.entry_desc = ctk.CTkEntry(self.main_frame, placeholder_text="Ej: Consultoría técnica", width=400)
        self.entry_desc.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.label_horas = ctk.CTkLabel(self.main_frame, text="Horas trabajadas:", font=("Roboto", 14))
        self.label_horas.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.entry_horas = ctk.CTkEntry(self.main_frame, placeholder_text="Ej: 5", width=400)
        self.entry_horas.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.btn_add = ctk.CTkButton(self.main_frame, text="➕ Añadir a la lista", command=self.agregar_servicio, fg_color="green", hover_color="#006400")
        self.btn_add.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

        self.frame_servicios = ctk.CTkScrollableFrame(self.main_frame, width=400, height=300, label_text="Servicios añadidos")
        self.frame_servicios.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
        
        self.servicios = []

        self.btn_generar = ctk.CTkButton(self.main_frame, text="Generar Factura", command=self.obtener_datos)
        self.btn_generar.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
    def cargar_numero_inicial(self):
        try:
            with open("ultimo_numero.txt", "r") as f:
                numero = f.read().strip()
                self.entry_invoice.insert(0, numero)
        except FileNotFoundError:
            self.entry_invoice.insert(0, "1")

    def actualizar_archivo_consecutivo(self, nuevo_numero):
        with open("ultimo_numero.txt", "w") as f:
            f.write(str(nuevo_numero))
    def obtener_datos(self):
        print("\n--- INICIANDO VALIDACIÓN ---")
        
        # 1. Validaciones de seguridad
        if not self.servicios:
            messagebox.showwarning("Lista Vacía", "Debes añadir al menos un servicio.")
            return
        
        try:
            email = self.entry_email.get().strip()
            tarifa = float(self.entry_tarifa.get().strip())
            numero_a_usar = int(self.entry_invoice.get())

            if tarifa <= 0:
                messagebox.showerror("Error", "La tarifa debe ser mayor a 0")
                return
            if "@" not in email or '.' not in email:
                messagebox.showwarning("Email Inválido", "Ingresa un correo válido.")
                return 
        except ValueError:
            messagebox.showwarning("Error de Formato", "Revisa los números en Tarifa e Invoice")
            return

        # 2. PROCESO DE GENERACIÓN (Solo una vez)
        self.mostrar_progreso()
        self.update() 

        try:
            # 🚀 ESTA ES LA ÚNICA LLAMADA QUE NECESITAMOS
            generar_factura_completa(tarifa, email, self.servicios, numero_a_usar)
            
            # Cerramos la ventana de carga
            self.ventana_carga.destroy()
            
            # 3. ACTUALIZACIÓN Y LIMPIEZA
            nuevo_numero = numero_a_usar + 1
            self.actualizar_archivo_consecutivo(nuevo_numero)
            
            # Actualizar interfaz
            self.entry_invoice.delete(0, 'end')
            self.entry_invoice.insert(0, str(nuevo_numero))
            
            # Limpiar lista de servicios (memoria y visual)
            self.servicios = []
            for widget in self.frame_servicios.winfo_children():
                widget.destroy()

            # Mensaje final de éxito
            label_exito = ctk.CTkLabel(
                self.frame_servicios, 
                text=f"✅ Factura #{numero_a_usar} enviada con éxito",
                text_color="#2ecc71",
                font=("Roboto", 14, "bold")
            )
            label_exito.pack(pady=20)
            
            messagebox.showinfo("Éxito", f"Factura #{numero_a_usar} enviada correctamente.")
            print(f"✅ Proceso completado. Sistema listo para factura #{nuevo_numero}")

        except Exception as e:
            if hasattr(self, 'ventana_carga'): self.ventana_carga.destroy()
            messagebox.showerror("Error Crítico", f"No se pudo completar: {e}")
            
    def agregar_servicio(self):
        descripcion = self.entry_desc.get()
        horas_texto = self.entry_horas.get()

        if not descripcion or not horas_texto:
            messagebox.showwarning("Campos Vacios", "Por favor, completa tanto la descripcion como las horas")
            return
        try:
            horas = float(horas_texto)
            if horas <= 0:
                messagebox.showerror("Error de horas","La cantidad de horas debe ser mayor a 0.")
                return
            
            # Guardamos en la memoria
            servicio = {"descripcion": descripcion, "horas": horas}
            self.servicios.append(servicio)
            
            # CREACIÓN VISUAL (Una sola vez)
            fila = ctk.CTkFrame(self.frame_servicios)
            fila.pack(fill="x", padx=5, pady=2)

            lbl = ctk.CTkLabel(fila, text=f"• {descripcion} ({horas} hrs)")
            lbl.pack(side="left", padx=10)

            btn_del = ctk.CTkButton(fila, text="X", width=30, fg_color="red", 
                                   command=lambda f=fila, s=servicio: self.eliminar_servicio_individual(f, s))
            btn_del.pack(side="right", padx=5)

            # Limpiar entradas
            self.entry_desc.delete(0, 'end')
            self.entry_horas.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Error de formato", "En el campo 'Horas' solo se permiten numeros")

    def eliminar_servicio_individual(self, frame_fila, servicio_dict):
    # Lo quitamos de la lista interna para que no salga en la factura
        self.servicios.remove(servicio_dict)
    # Lo borramos de la interfaz visual
        frame_fila.destroy()
        print(f"🗑️ Eliminado de la lista: {servicio_dict['descripcion']}")
        
        # Aquí es donde más adelante llamaremos a tus funciones de main.py

    def abrir_carpeta_historial(self):
        ruta = "Inv"
        if os.path.exists(ruta):
            os.startfile(ruta) # Esto abre la carpeta en Windows automáticamente
        else:
            messagebox.showinfo("Carpeta no encontrada", "Aún no se ha creado la carpeta Inv. Genera tu primera factura primero.")

    def mostrar_progreso(self):
            # Creamos una ventana pequeña encima de la principal
            self.ventana_carga = ctk.CTkToplevel(self)
            self.ventana_carga.title("Procesando")
            self.ventana_carga.geometry("300x150")
            self.ventana_carga.grab_set() # Bloquea la ventana principal
            
            lbl = ctk.CTkLabel(self.ventana_carga, text="Generando Factura...", font=("Roboto", 14))
            lbl.pack(pady=20)
            
            # Barra de progreso indeterminada (va y viene)
            self.progreso = ctk.CTkProgressBar(self.ventana_carga, orientation="horizontal", mode="indeterminate")
            self.progreso.pack(pady=10, padx=20, fill="x")
            self.progreso.start() # Inicia el movimiento animado



if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()



