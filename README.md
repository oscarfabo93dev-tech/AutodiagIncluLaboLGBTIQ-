# Autodiagnóstico en Inclusión Laboral LGBTIQ+

Una herramienta de autodiagnóstico desarrollada en Streamlit para evaluar el nivel de madurez de las Agencias de Empleo en inclusión laboral de personas LGBTIQ+.

## 🚀 Características

- **Cuestionario interactivo** con 10 preguntas estructuradas
- **Tres niveles de evaluación**: Inicial, Intermedio y Avanzado
- **Interfaz responsive** adaptada para web, tablet y móvil
- **Generación de PDF** con los resultados del diagnóstico
- **Barra de progreso sticky** para mejor experiencia de usuario
- **Seguridad HTML** con escapado de contenido dinámico

## 📁 Estructura del Proyecto

```
mi_app_inclusiva/
├── app.py                 # Aplicación principal
├── data/                  # Archivos de datos Excel
├── src/
│   ├── data_handler.py    # Manejo de datos Excel
│   ├── quiz_logic.py      # Lógica del cuestionario
│   └── ui_builder.py      # Construcción de interfaz
└── requirements.txt       # Dependencias
```

## 🛠️ Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/oscarfabo93dev-tech/AutodiagIncluLaboLGBTIQ-.git
cd AutodiagIncluLaboLGBTIQ-
```

2. **Crear entorno virtual:**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**

```bash
streamlit run app.py
```

## 📋 Requisitos

- Python 3.8+
- Streamlit
- Pandas
- OpenPyXL
- ReportLab (para generación de PDF)

## 🎯 Uso

1. Abrir la aplicación en el navegador
2. Leer las instrucciones del cuestionario
3. Responder las 10 preguntas sobre inclusión laboral LGBTIQ+
4. Obtener el resultado con nivel de madurez
5. Descargar el PDF con los resultados detallados

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Hacer fork del proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Oscar Fabo** - _Desarrollo inicial_ - [@oscarfabo93dev-tech](https://github.com/oscarfabo93dev-tech)

## 🙏 Agradecimientos

- Comunidad LGBTIQ+ por la inspiración y retroalimentación
- Equipo de desarrollo por las mejoras continuas
