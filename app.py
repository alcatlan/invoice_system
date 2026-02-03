import os
import customtkinter as ctk
from tkinter import messagebox
from main import generar_factura_completa
from dotenv import load_dotenv

load_dotenv()
#configuramos el estilo visual
ctk.set_appearance_mode("dark") #modo nocturno
ctk.set_default_color_theme("blue") #Tema Azul

class InvoiceApp(ctk.CTk):
    def __init__(self):
        super() .__init__()

        #Configuracion de la ventana
        self.title("Invoice System - Alejandro Manrique")
        self.geometry("1200x1000")

        #Aqui iremos agregando los botones y textos
        self.label_titulo = ctk.CTkLabel(self, text="FACTURACION", font=("Roboto", 24))
        self.label_titulo.pack(pady=20)
        # --- Campo: Número de Invoice Actual ---
        self.label_invoice = ctk.CTkLabel(self, text="Próximo número de Invoice:")
        self.label_invoice.pack(pady=(10, 0))
        
        # Creamos el cuadro de texto
        self.entry_invoice = ctk.CTkEntry(self, width=100)
        self.entry_invoice.pack(pady=(0, 10))

        # Cargamos el número actual del archivo al abrir la app
        self.cargar_numero_inicial()
        # --- Campo: Tarifa por Hora ---
        self.label_tarifa = ctk.CTkLabel(self, text="Tarifa por hora (CAD):")
        self.label_tarifa.pack(pady=(10, 0))
        
        self.entry_tarifa = ctk.CTkEntry(self, placeholder_text="Ej: 20.50")
        self.entry_tarifa.pack(pady=(0, 10))
        # 📥 Cargamos la tarifa desde el .env
        tarifa_env = os.getenv("TARIFA_HORA")
        if tarifa_env:
            self.entry_tarifa.insert(0, tarifa_env)

        # --- Campo: Email del Cliente ---
        self.label_email = ctk.CTkLabel(self, text="Correo del cliente:")
        self.label_email.pack(pady=(10, 0))
        
        self.entry_email = ctk.CTkEntry(self, placeholder_text="cliente@correo.com", width=250)
        self.entry_email.pack(pady=(0, 20))
        # 📥 Cargamos el email desde el .env
        email_env = os.getenv("MI_CORREO")
        if email_env:
            self.entry_email.insert(0, email_env)

        # --- Campo: Descripción del Servicio ---
        self.label_desc = ctk.CTkLabel(self, text="Descripción del servicio:")
        self.label_desc.pack(pady=(10, 0))
        
        self.entry_desc = ctk.CTkEntry(self, placeholder_text="Ej: Consultoría técnica", width=300)
        self.entry_desc.pack(pady=(0, 10))

        # --- Campo: Horas del Servicio ---
        self.label_horas = ctk.CTkLabel(self, text="Horas trabajadas:")
        self.label_horas.pack(pady=(10, 0))
        
        self.entry_horas = ctk.CTkEntry(self, placeholder_text="Ej: 5")
        self.entry_horas.pack(pady=(0, 10))

        # --- Botón: Añadir Servicio ---
        self.btn_add = ctk.CTkButton(self, text="➕ Añadir a la lista", command=self.agregar_servicio, fg_color="green", hover_color="#006400")
        self.btn_add.pack(pady=10)
        # --- Lista Visual de Servicios ---
        
        # --- Panel Desplazable de Servicios ---
        self.frame_servicios = ctk.CTkScrollableFrame(self, width=400, height=200, label_text="Servicios añadidos")
        self.frame_servicios.pack(pady=10)
        
        # Lista interna para guardar los servicios
        self.servicios = []

        # --- Botón para continuar ---
        self.btn_generar = ctk.CTkButton(self, text="Generar Factura", command=self.obtener_datos)
        self.btn_generar.pack(pady=20)
    #Actualizar archivo consecutivo
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
        print("\n--- INICIANDO VALIDACIÓN ---") # 🔍 Diagnóstico
        # 1. Validamos si la lista está vacía
        
        if not self.servicios:
            messagebox.showwarning("Lista Vacía", "Debes añadir al menos un servicio antes de generar la factura.")
            return # Aquí se detiene y no sigue con el resto
        
        try:
            email = self.entry_email.get().strip()
            tarifa_texto = self.entry_tarifa.get().strip()
            
            # Convertimos y mostramos en la terminal el valor exacto
            tarifa = float(tarifa_texto)
            print(f"DEBUG: El programa leyó la tarifa como: [{tarifa}]")

            #---------- FILTRO DE SEGURIDAD ---------
            if tarifa <= 0:
                print("DEBUG: Entró al IF (Tarifa <= 0). Mostrando error...")
                messagebox.showerror("Error", f"La tarifa ({tarifa}) debe ser mayor a 0")
                return # Esto DEBE detener la factura
            #-----------------------------------------

            numero_a_usar = int(self.entry_invoice.get())
            
        except ValueError:
            messagebox.showwarning("Error de Formato", "Ingresa números válidos en Tarifa y Factura")
            return

        # Validación de email
        if "@" not in email or '.' not in email:
            messagebox.showwarning("Email Inválido", "Ingresa un correo válido.")
            return         

        # Si llegamos aquí, es que la tarifa pasó la prueba ✅
        print(f"✅ Validación exitosa. Generando factura con tarifa {tarifa}")
        generar_factura_completa(tarifa, email, self.servicios, numero_a_usar)  

        print("\n--- RESUMEN DE FACTURA ---")
        print(f"💰 Tarifa: {tarifa} CAD/hr")
        print(f"📧 Enviar a: {email}")
        print(f"📄 Invoice No: {numero_a_usar}")
        print("🛠️ Servicios registrados:")
        
        for s in self.servicios:
            print(f"  - {s['descripcion']}: {s['horas']} horas")

        # 🚀 ¡LLAMADA AL MOTOR! 
        # IMPORTANTE: Ahora pasamos 'numero_actual' como el cuarto argumento
        generar_factura_completa(tarifa, email, self.servicios, numero_a_usar)
        
        # 3. INCREMENTO AUTOMÁTICO 🔄
        # Calculamos el siguiente número para la próxima factura
        nuevo_numero_sugerido = numero_a_usar + 1
        
        # Guardamos este nuevo número en el archivo 'ultimo_numero.txt'
        self.actualizar_archivo_consecutivo(nuevo_numero_sugerido)
        
        # Actualizamos visualmente el cuadro de la ventana para que ya diga el siguiente
        self.entry_invoice.delete(0, 'end')
        self.entry_invoice.insert(0, str(nuevo_numero_sugerido))

        # ✨ LIMPIEZA POST-FACTURACIÓN
        self.servicios = [] # Vaciamos la lista interna
        
        # Reseteamos la caja de texto visual de la lista de servicios
        for widget in self.frame_servicios.winfo_children():
            widget.destroy()

        label_exito = ctk.CTkLabel(
            self.frame_servicios, 
            text=f"✅ Factura #{numero_a_usar} generada y enviada con éxito",
            text_color="#2ecc71",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_exito.pack(pady=20)
        

        print(f"✅ Proceso completado. Sistema listo para factura #{nuevo_numero_sugerido}")
            
    def agregar_servicio(self):
        # 1. Capturamos los valores actuales
        descripcion = self.entry_desc.get()
        horas_texto = self.entry_horas.get()

        # 2. Validamos de campos vacios
        if not descripcion or not horas_texto:
            messagebox.showwarning("Campos Vacios", "Por favor, completa tanto la descripcion como las horas")
            return
        try:
            # 3 . Intento de conversion y validacion logica

            horas = float(horas_texto)

            if horas <= 0:
                messagebox.showerror("Error de horas","La cantidad de horas debe ser un numero mayor a 0.")
                return
            
            # 4. Si todo es correto(True) guardamos en la lista interna
            servicio = {"descripcion": descripcion, "horas": float(horas_texto)}
            self.servicios.append(servicio)
            
            print(f"✅ Añadido: {descripcion} ({horas_texto} hrs)")
            
            # 5. Limpiamos los cuadros de texto
            self.entry_desc.delete(0, 'end')
            self.entry_horas.delete(0, 'end')
            # Actualizamos la interfaz visual (la "tarjeta")

            fila = ctk.CTkFrame(self.frame_servicios)
            fila.pack(fill="x", padx=5, pady=2)

            # Etiqueta con el nombre y horas
            lbl = ctk.CTkLabel(fila, text=f"• {descripcion} ({horas} hrs)")
            lbl.pack(side="left", padx=10)

            # ¡El botón de eliminar! 🗑️
            btn_del = ctk.CTkButton(
                fila, text="X", width=30, fg_color="red", 
                command=lambda f=fila, s=servicio: self.eliminar_servicio_individual(f, s)
                )
            btn_del.pack(side="right", padx=5)
        except ValueError:
            #Capturamos si el usuario escribio letrar en le campo horas
            messagebox.showerror("Error de formato", "En el campo 'Horas' solo se permiten numeros")

    def eliminar_servicio_individual(self, frame_fila, servicio_dict):
    # Lo quitamos de la lista interna para que no salga en la factura
        self.servicios.remove(servicio_dict)
    # Lo borramos de la interfaz visual
        frame_fila.destroy()
        print(f"🗑️ Eliminado de la lista: {servicio_dict['descripcion']}")
        
        # Aquí es donde más adelante llamaremos a tus funciones de main.py
if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()


