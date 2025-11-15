
# Optimización de Asignación de Tareas  
## Proyecto Final – Investigación de Operaciones  
**Streamlit + PuLP + Python 3.11**

Este proyecto implementa un modelo de **asignación óptima de tareas** utilizando Programación Lineal Entera con **PuLP**, visualizado mediante una interfaz web creada en **Streamlit**.

Permite:

* Editar programadores y disponibilidad  
* Ajustar tiempos estimados por tarea  
* Resolver el modelo con un clic  
* Visualizar:
    * Tiempo total óptimo  
    * Asignación de tareas  
    * Carga de trabajo  
    * Matriz binaria de decisión  

---
## 🎥 Video demostrativo

Puedes ver un video corto del funcionamiento de la aplicación en el siguiente enlace:

[▶ Ver demo en GitHub](media/demo.mp4)

---

## Instalación (Windows 10/11)

### 1️⃣ Instalar Python 3.11

Abrir CMD:

```
Win + R → cmd → Enter
```

Ejecutar:

```bat
py install 3.11
```

Verificar instalación:

```bat
py -3.11 --version
```

Debe mostrar:

```
Python 3.11.x
```

---

### 2️⃣ Clonar o descargar este repositorio

Clonar:

```bash
git clone https://github.com/saulbarbero/io_asignacion_streamlit.git
cd io_asignacion_streamlit
```

---

### 3️⃣ Crear un entorno virtual

```bat
py -3.11 -m venv venv311
```

---

### 4️⃣ Activar el entorno virtual

```bat
venv311\Scripts\activate
```

Verificar versión:

```bat
python --version
```

---

### 5️⃣ Instalar dependencias

```bat
python -m pip install --upgrade pip
python -m pip install streamlit pandas pulp
```

---

## ▶️ 6️⃣ Ejecutar la aplicación

```bat
python -m streamlit run app.py
```

La aplicación estará disponible en:

```
http://localhost:8501
```

---

#  Uso de la Aplicación

### Editar programadores
* Nombres  
* Disponibilidad  

### Modificar tiempos estimados
* Tiempos por programador y tarea  
* Si un tiempo es **0**, el programador **no puede realizar** esa tarea  

### Resolver el modelo
* Calcula la asignación óptima  
* Minimiza el tiempo total  

### Resultados mostrados
* Tiempo total óptimo  
* Asignación óptima  
* Matriz binaria  
* Gráfica de carga por programador  

---

# Ejecución diaria (ya instalado)

```bat
cd ruta/del/proyecto
venv311\Scripts\activate
python -m streamlit run app.py
```

---

# Solución de Problemas

### ❌ Error: “pyarrow / cmake / numpy dtype error”
Causa: usar Python 3.12 o 3.14.  
Solución: usar **Python 3.11**.

---

### ❌ Error: “No module named streamlit”
No activaste el entorno virtual:

```bat
venv311\Scripts\activate
```

---

### ❌ La app no se abre sola
Abrir manualmente:

```
http://localhost:8501
```

---

Activar entorno:

```bat
venv311\Scripts\activate
```

Ejecutar app:

```bat
python -m streamlit run app.py
```




```
si tiempo[p,t] = 0 → x[p,t] = 0
```


