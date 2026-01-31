import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def enviar_factura_por_email(destinatario, nombre_archivo_pdf, factura_no):
    # --- Tus credenciales ---
    mi_correo = os.getenv("MI_CORREO")
    mi_password = os.getenv("MI_PASSWORD")
    
    # 1. Creamos el contenedor del mensaje
    msg = MIMEMultipart()
    msg['From'] = mi_correo
    msg['To'] = destinatario
    msg['Subject'] = f"Invoice {factura_no} - Alejandro Manrique"

    # 2. El mensaje que leerá el cliente
    cuerpo = f"Hi,\n\nPlease find attached the invoice {factura_no}.\n\nBest regards,\n\nAlejandro."
    msg.attach(MIMEText(cuerpo, 'plain'))

    # 3. Adjuntamos el archivo PDF
    try:
        with open(nombre_archivo_pdf, "rb") as adjunto:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(adjunto.read())
        
        encoders.encode_base64(parte)
        parte.add_header('Content-Disposition', f"attachment; filename= {nombre_archivo_pdf}")
        msg.attach(parte)

        # 4. Envío real
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(mi_correo, mi_password)
        server.send_message(msg)
        server.quit()
        return True # Si todo salió bien
        
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
        return False