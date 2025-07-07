from data_access import DataAccess
from entities import Gym, User, Clases

class BusinessLogic:
    def __init__(self):
        self.data_access = DataAccess()

    def register_gym(self, gym: Gym):
        gym.validate()
        self.data_access.save_gym(gym)
        return f"Gimnasio {gym.name} registrado con exito"

    def get_all_gyms(self):
        return self.data_access.get_all_gyms()

    def get_gym_by_id(self, id):
        return self.data_access.get_gym_by_id(id)

    def update_gym(self, gym: Gym):
        self.data_access.update_gym(gym.id, gym.name, gym.password)
        return f"Gimnasio {gym.name}, actualizado correctamente"

    def delete_gym(self, gym_id):
        self.data_access.delete_gym(gym_id)
        return f"Gimnasio eliminado  correctamente"

    def get_gym_by_name(self, name):
        return self.data_access.get_gym_by_name(name)

    def save_user(self, user: User):
        user.validate()
        self.data_access.save_user(user)
        return f"Usuario {user.username} registrado con éxito"

    def get_all_users(self, gym_id: int):
        return self.data_access.get_all_users(gym_id)

    def get_user_by_username(self, username: str):
        user = self.data_access.get_user_by_username(username)
        return user  

    def get_user_by_id(self, id: int):
        return self.data_access.get_user_by_id(id)

    def update_user(self, id: int, username: str, password: str, cedula: str):
        self.data_access.update_user(id, username, password, cedula)

    def delete_user(self, id: int):
        self.data_access.delete_user(id)

    def save_class(self, clase: Clases):
        self.data_access.save_class(clase)
        print(f"Guardando clase: {clase.name}, {clase.schedule}, {clase.capacity}")
        return f"Clase '{clase.name}' registrada con éxito"

    def get_all_classes(self, gym_id: int):
        return self.data_access.get_all_classes(gym_id)

    def get_class_by_id(self, id: int):
        return self.data_access.get_class_by_id(id)

    def update_class(self, id: int, name: str, schedule: str, capacity: int):
        from datetime import datetime
        try:
            schedule = datetime.strptime(schedule, "%Y-%m-%dT%H:%M")  # Validación de formato
        except ValueError:
            raise ValueError("Formato de fecha y hora inválido")

        clase = Clases(id=id, name=name, schedule=schedule, capacity=capacity)
        self.data_access.update_class(clase.id, clase.name, clase.schedule, clase.capacity, clase.current_participants or 0)


    def delete_class(self, id: int):
        self.data_access.delete_class(id)

    def get_classes_by_date_not_enrolled(self, date, user_id):
        return self.data_access.get_classes_by_date_not_enrolled(date, user_id)

    def enroll_user_to_class(self, user_id: int, class_id: int):
        try:
            self.data_access.enroll_user_to_class(user_id, class_id)
            return f"Usuario {user_id} inscrito exitosamente en la clase {class_id}."
        except RuntimeError as e:
            raise RuntimeError(f"No se pudo inscribir al usuario: {e}")

    def get_classes_enrolled_by_user(self, user_id: int):
        return self.data_access.get_classes_enrolled_by_user(user_id)

    def delete_enrollment(self, user_id: int, class_id: int):
        self.data_access.delete_enrollment(user_id, class_id)
        return f"Inscripción a la clase con ID {class_id} eliminada correctamente para el usuario con ID {user_id}."