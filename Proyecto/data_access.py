import pyodbc
from entities import Gym, User, Clases, ClassEnrollment



class DataAccess:
    def __init__(self):
        self.connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=LAPTOP-DE-DAVID;'
    'DATABASE=proyecto_gym;'
    'UID=sa;'
    'PWD=123456'
)


    def save_gym(self, gym: Gym):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC SaveGym ?, ?", (gym.name, gym.password))
                result = cursor.fetchone()
                if result and result[0] is not None:
                    gym.id = result[0] 
                conn.commit()
                return gym.id
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al guardar Gimnasio: {e}")

    def get_all_gyms(self):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC GetAllGyms")
                rows = cursor.fetchall()
                gyms = [{"id": row[0], "name": row[1], "password": row[2]} for row in rows]
                return gyms
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener Gimnasios: {e}")

    def get_gym_by_id(self, id):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC GetGymById ?", (id,))
                row = cursor.fetchone()
                if row:
                    return Gym(id=row[0], name=row[1], password=row[2])
                return None
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener el Gimnasio: {e}")

    def update_gym(self, id, name, password):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC UpdateGym ?, ?, ?", (id, name, password))
                conn.commit()
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al actualizar Gimnasio: {e}")

    def delete_gym(self, id):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC DeleteGym ?", (id,))
                conn.commit()
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al eliminar Gimnasio: {e}")

    def get_gym_by_name(self, name):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC GetGymByName ?", (name,))
                row = cursor.fetchone()
                if row:
                    return Gym(id=row[0], name=row[1], password=row[2])
                return None
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener Gimnasio: {e}")

    def save_user(self, user: User):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC SaveUser ?, ?, ?, ?", (user.username, user.password, user.cedula, user.gym_id))
                result = cursor.fetchone()
                if result and result[0] is not None:
                    user.id = result[0]  # Si el procedimiento devuelve un ID, lo asigna
                conn.commit()
                return user.id
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al guardar Usuario: {e}")


    def get_all_users(self, gym_id):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC GetAllUsers ?", (gym_id,))
                rows = cursor.fetchall()
                users = [{"id": row[0], "username": row[1], "password": row[2], "cedula": row[3]} for row in rows]
                return users
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener los usuarios: {e}")


    def get_user_by_username(self, username: str):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC GetUserByUsername ?", (username,))
                row = cursor.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "username": row[1],
                        "password": row[2],
                        "cedula": row[3],
                        "gym_id": row[4]
                    }
                return None  # Si no se encuentra el usuario
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener el usuario por username: {e}")


    def get_user_by_id(self, id: int):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC GetUserById ?", (id,))
                row = cursor.fetchone()
                if row:
                    return User(id=row[0], username=row[1], password=row[2], cedula=row[3], gym_id=row[4])
                return None
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener el Usuario: {e}")


    def update_user(self, id: int, username: str, password: str, cedula: str):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC UpdateUser ?, ?, ?, ?", (id, username, password, cedula))
                conn.commit()
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al actualizar Usuario: {e}")


    def delete_user(self, id: int):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC DeleteUser ?", (id,))
                conn.commit()
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al eliminar Usuario: {e}")

    def save_class(self, clase: Clases):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                print("Ejecutando SaveClass")
                cursor.execute(
                    "EXEC SaveClass ?, ?, ?, ?, ?",
                    (clase.name, clase.schedule, clase.capacity, clase.current_participants or 0, clase.gym_id)
                )
                result = cursor.fetchone()
                print("Clase guardada con ID:", result[0])
                if result and result[0] is not None:
                    clase.id = result[0]  # Asignar el ID generado a la clase
                conn.commit()
                return clase.id
        except pyodbc.Error as e:
            print(f"Error al guardar la clase: {e}")
            raise RuntimeError(f"Error al guardar la clase: {e}")


    def get_all_classes(self, gym_id):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC GetAllClasses ?", (gym_id,))
                rows = cursor.fetchall()
                classes = [{"id": row[0], "name": row[1], "schedule": row[2], "capacity": row[3], "current_participants": row[4]} for row in rows]
                return classes
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener las clases: {e}")


    def get_class_by_id(self, id):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC GetClassById ?", (id,))
                row = cursor.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "name": row[1],
                        "schedule": row[2],
                        "capacity": row[3],
                        "current_participants": row[4],
                        "gym_id": row[5]
                    }
                return None  # Si no encuentra la clase
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener la clase por ID: {e}")

    def update_class(self, id, name, schedule, capacity, current_participants):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                print(f"Actualizando clase: {id}, {name}, {schedule}, {capacity}, {current_participants}")
                cursor.execute(
                    "EXEC UpdateClass ?, ?, ?, ?, ?",
                    (id, name, schedule, capacity, current_participants)
                )
                conn.commit()
        except pyodbc.Error as e:
            print(f"Error al actualizar la clase: {e}")
            raise RuntimeError(f"Error al actualizar la clase: {e}")


    def delete_class(self, id):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC DeleteClass ?", (id,))
                conn.commit()
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al eliminar la clase: {e}")

    def get_classes_by_date_not_enrolled(self, user_id, date):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                print(f"Ejecutando GetClassesByDateNotEnrolled con date: {date}, user_id: {user_id}")
                cursor.execute("EXEC GetClassesByDateNotEnrolled ?, ?", (date, user_id))
                rows = cursor.fetchall()
                classes = [
                    {
                        "id": row[0],
                        "name": row[1],
                        "schedule": row[2],
                        "capacity": row[3],
                        "current_participants": row[4],
                    }
                    for row in rows
                ]
                return classes
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al obtener clases no inscritas: {e}")

    def enroll_user_to_class(self, user_id: int, class_id: int):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC EnrollUserToClass ?, ?", (user_id, class_id))
                conn.commit()
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al inscribir al usuario en la clase: {e}")

    def get_classes_enrolled_by_user(self, user_id: int):
        print("Ejecutando SQL para clases inscritas")  # Depuración
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC GetClassesEnrolledByUser ?", (user_id,))
                rows = cursor.fetchall()
                print("Filas obtenidas del SQL:", rows)  # Depuración
                classes = [
                    {
                        "class_id": row[0],
                        "class_name": row[1],
                        "schedule": row[2],
                        "capacity": row[3],
                        "current_participants": row[4],
                    }
                    for row in rows
                ]
                return classes
        except pyodbc.Error as e:
            print(f"Error en la base de datos: {e}")  # Depuración
            raise RuntimeError(f"Error al obtener las clases inscritas: {e}")


    def delete_enrollment(self, user_id: int, class_id: int):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC DeleteEnrollment ?, ?", (user_id, class_id))
                conn.commit()
        except pyodbc.Error as e:
            raise RuntimeError(f"Error al eliminar la inscripción: {e}")
