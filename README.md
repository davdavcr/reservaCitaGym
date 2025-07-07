The user has provided an image containing a detailed README for a gym class reservation system called "reservaCitaGym". I will extract and present the key information from this README in a structured format.

## reservaCitaGym: Gym Class Reservation System

This is a simple project for managing gym class reservations, with a primary focus on the database.

### User Types and Access

The system supports three types of users:

  * **Administrator**: Special user with access to the `/admin` route.
      * Username: `adminp2024`
      * Password: `123456`
  * **Employees**: Can add users and classes (along with their capacities).
  * **Users**: Can log in, view available classes by date, and reserve a spot in a class, provided there's availability.

**Note:** This project does not include advanced security protocols as its main focus is on the database. Security measures will be added if the program is intended for sale.

### Installation and Configuration

#### 1\. Clone the Repository

```bash
git clone https://github.com/davdavcr/reservaCitaGym.git
cd reservaCitaGym
```

#### 2\. Create and Activate a Python Virtual Environment

The project uses Python, and the virtual environment is named `venv`.

  * **On Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
  * **On Linux/macOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

#### 3\. Install Dependencies

If a `requirements.txt` file exists, install dependencies with:

```bash
pip install -r requirements.txt
```

**Important:** If the project uses Django or a similar web framework, change `.django` extensions to `.html` or adjust front-end routes accordingly for correct functionality.

#### 4\. Database Configuration

This project is designed to use **SQL Server**. To ensure correct functionality, you must modify the connection string in the `data_access.py` file with your specific computer's details:

```python
class DataAccess:
    def __init__(self):
        self.connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=TU_SERVIDOR;'  # Change 'TU_SERVIDOR' to your SQL server's name or IP
            'DATABASE=proyecto_gym;'
            'UID=TU_USUARIO;'      # Change 'TU_USUARIO' to your SQL Server username
            'PWD=TU_CONTRASEÑA;'   # Change 'TU_CONTRASEÑA' to your SQL Server password
        )
```

### Project Structure

  * `__init__.py`: Initializes the package or main module of the application.
  * `routes.py`: Defines the application's routes or endpoints, controlling the flow between views and business logic.
  * `business.py`: Contains the business logic, processing data and coordinating operations between the database and the interface.
  * `data_access.py`: Handles functions related to connecting to and querying the SQL Server database, using stored procedures, triggers, and validations.
  * `entities.py`: Defines the data entities or models in Python that represent the database tables.
  * `run.py`: The main file to start the application.
  * `static/`: Folder containing static resources:
      * `css/`: Style files.
      * `js/`: JavaScript files.

### Database Details

The system uses an SQL Server database named `proyecto_gym` which contains tables for gyms, users, classes, and class enrollments.

#### Key Features

  * **Stored Procedures**: Used for CRUD (Create, Read, Update, Delete) operations on all entities.
  * **Triggers**: Implemented for maintaining referential integrity and data validation (e.g., preventing duplicate users, controlling class capacities, cascading deletions of related data).
  * **Validations**:
      * Specific format for usernames.
      * Prevention of duplicates for gyms, users, and IDs.
      * Control of class capacities and prevention of duplicate enrollments.

The complete database script is included in the project documentation or in the `script_bd.sql` file.

### Usage

1.  **Initialize the database**: Execute the SQL script to create the tables, procedures, and triggers.
2.  **Configure the connection string**: In `data_access.py`.
3.  **Run the application**:
    ```bash
    python run.py
    ```
4.  **Access the application**: Open it in your browser.
5.  **Access the administrative panel**: Use the `/admin` route with the administrator username and password provided above.

### Authors

  * David Arturo Brenes Angulo
  * Andrés Solano Contreras
  * Andrey Aguilar Aguirre
