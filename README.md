# Sistema de empleados de la empresa FullWeb

Este proyecto es una aplicación desarrollada con **Flask** y **PyQt5** que permite gestionar empleados, noticias y sugerencias dentro de una organización. Combina una interfaz web accesible mediante navegador con una ventana gráfica para facilitar su uso.

## Funcionalidades principales

### Gestión de clientes
- **Registro de clientes:** Permite registrar nuevos clientes con sus datos personales y de su proyecto.
- **Listado de clientes:** Muestra clientes activos en la interfaz.
- **Eliminación de clientes.:** Permite marcar a los clientes como "eliminados" sin borrar sus datos de la base.

### Panel de noticias recientes.
- **Visualización de noticias:** Panel que muestra las noticias recientes agregadas por el empleado.

### Panel de sugerencias.
- **Visualización de sugerencias:** Muestra las sugerencias enviadas junto con su respuesta (en caso de haber).
- **Agregar sugerencia:** Permite registrar una sugerencia que el administrador va a poder ver desde su interfaz.

## Requisitos previos

1. **Instalar XAMPP**: Asegúrate de tener los servicios de **Apache** y **MySQL** activados.
2. **Configurar la base de datos**:
   - Crea una base de datos en tu gestor preferido (por ejemplo, **MySQL Workbench** o **phpMyAdmin**).
   - Importa el archivo `.sql` incluido en el proyecto (CARPETA MODELS) para crear las tablas necesarias.

3. **Instalar dependencias del proyecto**:
   - Crea un entorno virtual:
     ```bash
     python -m venv .venv
     ```
   - Activa el entorno virtual:
     - En Windows:
       ```bash
       .venv\Scripts\activate
       ```
     - En macOS/Linux:
       ```bash
       source .venv/bin/activate
       ```
   - Instala las dependencias:
     ```bash
     pip install -r requirements.txt
     ```

## Uso de la aplicación

### Ejecución de la aplicación
1. Asegúrate de que los servicios de **Apache** y **MySQL** estén activos.
2. Ejecuta el script principal:
   ```bash
   python app.py

## Tecnologias utilizadas:
1. Flask: Framework backend para manejar rutas y lógica del servidor.
2. MySQL: Gestión de la base de datos.
3. Werkzeug: Librerías para hash de contraseñas y seguridad.
4. Flask-Mail: Libreria para enviar correos electrónicos.
5. Bootstrap: Diseño responsivo de la interfaz web.
   
