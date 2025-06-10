# 📊 Gestor de Suscripciones en COP

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![License](https://img.shields.io/badge/License-MIT-orange)

Aplicación de escritorio para administrar suscripciones y gastos mensuales en pesos colombianos (COP) con interfaz intuitiva.

## ✨ Características principales

- 🏦 **Gestión de múltiples cuentas**
- 💳 **Registro de suscripciones** con:
  - Nombre del servicio
  - Monto en COP (formato colombiano)
  - Fecha de pago
  - Frecuencia (Mensual, Trimestral, etc.)
  - Categoría (Entretenimiento, Software, etc.)
- 📅 **Cálculo automático** de próxima fecha de pago
- 🔎 **Sistema de filtrado** por mes/año
- 📈 **Visualización del total mensual**
- 💾 **Persistencia de datos** (guardado automático en JSON)

## 🖥️ Capturas de pantalla

| Vista principal | Formulario de suscripción |
|-----------------|--------------------------|
| ![Main View](screenshots/main.png) | ![Form View](screenshots/form.png) |

## 🛠️ Requisitos

- Python 3.x
- Módulos estándar:
  - `tkinter`
  - `json`
  - `datetime`

## 🚀 Instalación y uso

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/gestor-suscripciones.git
cd gestor-suscripciones
