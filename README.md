# 🧾 Sistema de Facturación Automatizado (Invoice Generator)

¡Bienvenid@! Este es un sistema de facturación profesional desarrollado en **Python**. Permite generar facturas personalizadas, convertirlas a PDF, enviarlas automáticamente por correo electrónico y mantener un registro organizado en Excel.

## ✨ Características Principales

* **Interfaz Gráfica Moderna:** Construida con `CustomTkinter` para una experiencia de usuario fluida y estética.
* **Generación de Documentos:** Crea facturas en formato `.docx` y las convierte automáticamente a `.pdf`.
* **Automatización de Correo:** Envía la factura generada directamente al cliente a través de Gmail.
* **Seguimiento de Pagos:** Registra cada factura en un historial de Excel para un control contable sencillo.
* **Seguridad:** Uso de variables de entorno (`.env`) para proteger las credenciales del usuario.

## 🛠️ Tecnologías Utilizadas

* **Python 3.x**
* **CustomTkinter** (Interfaz de usuario)
* **Python-docx** (Creación de documentos Word)
* **Comtypes** (Conversión robusta a PDF)
* **Smtplib** (Envío de correos electrónicos)

## 🚀 Cómo usarlo

1.  **Configuración:** Crea un archivo `.env` basado en el ejemplo del repositorio.
2.  **Ejecución:** Corre el archivo `app.py` o abre el ejecutable generado.
3.  **Facturación:** Ingresa los servicios, las horas y la tarifa. ¡El sistema se encarga del resto!

---
Desarrollado con ❤️ por Altecral.
