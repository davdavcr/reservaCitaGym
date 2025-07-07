class Gym:
    def __init__(self, id=None, name=None, password=None):
        self.id = id
        self.name = name
        self.password = password

    def validate(self):
        if not self.name or len(self.name) == 0:
            raise ValueError("El nombre no puede estar vacio")
        if not self.password or len(self.password) == 0:
            raise ValueError("La contraseña no puede estar vacia")

class User:
    def __init__(self, id=None, username=None, password=None, cedula = None, gym_id=None):
        self.id = id
        self.username = username
        self.password = password
        self.cedula = cedula
        self.gym_id = gym_id

    def validate(self):
        if not self.username or len(self.username) == 0:
            raise ValueError("El usuario no puede estar vacio")
        if not self.password or len(self.password) == 0:
            raise ValueError("La contraseña no puede estar vacia")

class Clases:
    def __init__(self, id=None, name=None, schedule=None, capacity=None, current_participants=None, gym_id=None ):
        self.id = id
        self.name = name
        self.schedule = schedule
        self.capacity = capacity
        self.current_participants = current_participants
        self.gym_id = gym_id

    def validate(self):
        if not self.name or len(self.name) == 0:
            raise ValueError("El nombre de la clase no puede estar vacío")
        if not self.schedule or len(self.schedule) == 0:
            raise ValueError("El horario de la clase no puede estar vacío")
        if self.capacity is None or self.capacity <= 0:
            raise ValueError("La capacidad debe ser un número mayor a 0")

class ClassEnrollment:
    def __init__(self, id=None, user_id=None, class_id=None, enrollment_date=None):
        self.id = id
        self.user_id = user_id
        self.class_id = class_id
        self.enrollment_date = enrollment_date

    def validate(self):
        if not self.user_id:
            raise ValueError("El ID del usuario no puede estar vacío.")
        if not self.class_id:
            raise ValueError("El ID de la clase no puede estar vacío.")