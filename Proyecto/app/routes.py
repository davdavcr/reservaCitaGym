from flask import Blueprint, flash, redirect, request, render_template, current_app as app, session, url_for
from business import BusinessLogic
from entities import Gym, User, Clases


business_logic = BusinessLogic()

# Definir el Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']

        if user == 'adminp2024' and password == '123456':
            session['admin_logged_in'] = True
            flash('Inicio de sesión como administrador exitoso', 'success')
            return redirect(url_for('routes.admin_dashboard'))
        else:
            flash('Credenciales de administrador incorrectas', 'danger')

    return render_template('index_admin.html')

@routes.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('routes.admin'))
    gyms = business_logic.get_all_gyms()
    return render_template('admin_dashboard.html', gyms=gyms)


@routes.route('/admin/add-gym', methods=['GET', 'POST'])
def add_gym():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        gym = Gym(name=name, password=password)
        business_logic.register_gym(gym)
        flash('Gimnasio agregado exitosamente', 'success')
        return redirect(url_for('routes.admin_dashboard'))
    return render_template('add_gym.html')

@routes.route('/admin/edit-gym/<int:id>', methods=['GET', 'POST'])
def edit_gym(id):
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        business_logic.update_gym(Gym(id=id, name=name, password=password))
        return redirect(url_for('routes.admin_dashboard'))
    gym = business_logic.get_gym_by_id(id)
    if gym is None:
        flash('El gimnasio no existe', 'danger')
        return redirect(url_for('routes.admin_dashboard'))
    return render_template('edit_gym.html', gym=gym)


@routes.route('/admin/delete-gym/<int:id>', methods=['POST'])
def delete_gym(id):
    business_logic.delete_gym(id)
    return redirect(url_for('routes.admin_dashboard'))

@routes.route('/login_admin_gym', methods=['GET', 'POST'])
def login_admin_gym():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        gym = business_logic.get_gym_by_name(name)
        if gym and gym.password == password:
            session['gym_id'] = gym.id
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('routes.admin_gym_dashboard'))
        else:
            flash('Correo electrónico o contraseña incorrectos', 'danger')
    return render_template('login_admin_gym.html')

@routes.route('/admin_gym_dashboard', methods=['GET'])
def admin_gym_dashboard():
    if 'gym_id' not in session:
        flash("Debes iniciar sesión como gimnasio", "danger")
        return redirect(url_for('routes.login_admin_gym'))

    gym_id = session['gym_id']
    users = business_logic.get_all_users(gym_id)
    return render_template('admin_gym_dashboard.html', users=users)

@routes.route('/admin_gym/users/add', methods=['GET', 'POST'])
def admin_gym_add_user():
    if 'gym_id' not in session:
        flash("Debes iniciar sesión como gimnasio", "danger")
        return redirect(url_for('routes.login_admin_gym'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cedula = request.form['cedula']  # Agregado para capturar la cédula
        gym_id = session['gym_id']

        user = User(username=username, password=password, cedula=cedula, gym_id=gym_id)
        business_logic.save_user(user)

        flash(f"Usuario '{username}' agregado exitosamente", "success")
        return redirect(url_for('routes.admin_gym_dashboard'))

    return render_template('admin_gym_add_user.html')


@routes.route('/admin_gym/users/edit/<int:user_id>', methods=['GET', 'POST'])
def admin_gym_edit_user(user_id):
    if 'gym_id' not in session:
        flash("Debes iniciar sesión como gimnasio", "danger")
        return redirect(url_for('routes.login_admin_gym'))

    gym_id = session['gym_id']
    user = business_logic.get_user_by_id(user_id)

    if not user or user.gym_id != gym_id:
        flash("No tienes permiso para editar este usuario", "danger")
        return redirect(url_for('routes.admin_gym_dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cedula = request.form['cedula']
        business_logic.update_user(user_id, username, password, cedula)

        flash(f"Usuario '{username}' actualizado exitosamente", "success")
        return redirect(url_for('routes.admin_gym_dashboard'))

    return render_template('admin_gym_edit_user.html', user=user)


@routes.route('/admin_gym/users/delete/<int:user_id>', methods=['POST'])
def admin_gym_delete_user(user_id):
    if 'gym_id' not in session:
        flash("Debes iniciar sesión como gimnasio", "danger")
        return redirect(url_for('routes.login_admin_gym'))

    gym_id = session['gym_id']
    user = business_logic.get_user_by_id(user_id)

    if not user or user.gym_id != gym_id:
        flash("No tienes permiso para eliminar este usuario", "danger")
        return redirect(url_for('routes.admin_gym_dashboard'))

    business_logic.delete_user(user_id)
    flash(f"Usuario '{user.username}' eliminado exitosamente", "success")
    return redirect(url_for('routes.admin_gym_dashboard'))

@routes.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Limpia todas las variables de sesión
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('routes.home'))  # Redirige a la página de inicio

@routes.route('/admin_gym_dashboard/clases', methods=['GET'])
def admin_gym_dashboard_clases():
    if 'gym_id' not in session:
        flash("Debes iniciar sesión como gimnasio", "danger")
        return redirect(url_for('routes.login_admin_gym'))

    gym_id = session['gym_id']
    clases = business_logic.get_all_classes(gym_id)
    return render_template('admin_gym_dashboard_clases.html', clases=clases)

@routes.route('/admin_gym_dashboard/clases/add', methods=['GET', 'POST'])
def admin_gym_add_clase():
    if 'gym_id' not in session:
        flash("Debes iniciar sesión como gimnasio", "danger")
        return redirect(url_for('routes.login_admin_gym'))

    if request.method == 'POST':
        print("Formulario recibido")  # Agrega este print
        name = request.form['name']
        schedule = request.form['schedule']
        capacity = request.form['capacity']
        gym_id = session['gym_id']

        from datetime import datetime
        try:
            schedule = datetime.strptime(schedule, "%Y-%m-%dT%H:%M")  # Ajusta al formato HTML
        except ValueError:
            flash("El formato de fecha y hora es inválido.", "danger")
            return render_template('admin_gym_add_clase.html')

        clase = Clases(name=name, schedule=schedule, capacity=capacity, gym_id=gym_id)
        business_logic.save_class(clase)

        flash(f"Clase '{name}' agregada exitosamente", "success")
        return redirect(url_for('routes.admin_gym_dashboard_clases'))

    return render_template('admin_gym_add_clase.html')

@routes.route('/admin_gym_dashboard/clases/edit/<int:clase_id>', methods=['GET', 'POST'])
def admin_gym_edit_clase(clase_id):
    if 'gym_id' not in session:
        flash("Debes iniciar sesión como gimnasio", "danger")
        return redirect(url_for('routes.login_admin_gym'))

    gym_id = session['gym_id']
    clase = business_logic.get_class_by_id(clase_id)
    if request.method == 'POST':
        name = request.form['name']
        schedule = request.form['schedule']
        capacity = request.form['capacity']

        try:
            business_logic.update_class(clase_id, name, schedule, int(capacity))
            flash(f"Clase '{name}' actualizada exitosamente", "success")
            return redirect(url_for('routes.admin_gym_dashboard_clases'))
        except ValueError as ve:
            flash(str(ve), "danger")
        except RuntimeError as re:
            flash(f"Error en la base de datos: {str(re)}", "danger")

    return render_template('admin_gym_edit_clase.html', clase=clase)



@routes.route('/admin_gym_dashboard/clases/delete/<int:clase_id>', methods=['POST'])
def admin_gym_delete_clase(clase_id):
    if 'gym_id' not in session:
        flash("Debes iniciar sesión como gimnasio", "danger")
        return redirect(url_for('routes.login_admin_gym'))
    gym_id = session['gym_id']
    clase = business_logic.get_class_by_id(clase_id)
    business_logic.delete_class(clase_id)
    return redirect(url_for('routes.admin_gym_dashboard_clases'))


@routes.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Obtener el usuario por el nombre de usuario
        user = business_logic.get_user_by_username(username)

        if user and user['password'] == password:  # Verificar si el usuario existe y la contraseña coincide
            session['user_id'] = user['id']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('routes.user_select_date'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')

    return render_template('login_user.html')


@routes.route('/user_select_date', methods=['GET', 'POST'])
def user_select_date():
    if 'user_id' not in session:
        flash("Debes iniciar sesión como usuario", "danger")
        return redirect(url_for('routes.login_user'))

    if request.method == 'POST':
        selected_date = request.form.get('selected_date')  # Obtener la fecha seleccionada del formulario
        if selected_date:
            return redirect(url_for('routes.user_classes_by_date', date=selected_date))
        else:
            flash("Por favor selecciona una fecha válida.", "danger")

    return render_template('user_select_date.html')

@routes.route('/user_classes_by_date/<date>', methods=['GET'])
def user_classes_by_date(date):
    if 'user_id' not in session:
        flash("Debes iniciar sesión como usuario", "danger")
        return redirect(url_for('routes.login_user'))

    from datetime import datetime
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%d")  # Validar formato de fecha recibido
    except ValueError:
        flash("Fecha inválida, intenta nuevamente.", "danger")
        return redirect(url_for('routes.user_select_date'))

    user_id = session['user_id']
    classes = business_logic.get_classes_by_date_not_enrolled(user_id, formatted_date)
    return render_template('user_classes_by_date.html', classes=classes, date=formatted_date)

@routes.route('/user/enroll/<int:class_id>', methods=['POST'])
def user_enroll_class(class_id):

    if 'user_id' not in session:
        flash("Debes iniciar sesión como usuario", "danger")
        return redirect(url_for('routes.login_user'))

    user_id = session['user_id']
    try:
        # Llama a la lógica de negocio para inscribir al usuario
        message = business_logic.enroll_user_to_class(user_id, class_id)
        flash(message, "success")
    except RuntimeError as e:
        flash(str(e), "danger")

    # Redirige al usuario de vuelta a la página de clases disponibles
    return redirect(url_for('routes.user_classes_by_date', date=request.form['date']))

@routes.route('/user_enrolled_classes', methods=['GET'])
def user_enrolled_classes():
    print("Ruta /user_enrolled_classes invocada")  # Depuración
    if 'user_id' not in session:
        print("Sesión no contiene user_id")  # Depuración
        flash("Debes iniciar sesión como usuario", "danger")
        return redirect(url_for('routes.login_user'))

    user_id = session['user_id']
    print(f"user_id en la sesión: {user_id}")  # Depuración

    try:
        enrolled_classes = business_logic.get_classes_enrolled_by_user(user_id)
        print("Clases inscritas obtenidas:", enrolled_classes)  # Depuración
    except Exception as e:
        print(f"Error al obtener clases inscritas: {e}")
        flash("Hubo un error al obtener las clases inscritas.", "danger")
        return redirect(url_for('routes.user_classes_by_date', date='today'))

    return render_template('user_enrolled_classes.html', classes=enrolled_classes)



    return render_template('user_enrolled_classes.html', classes=enrolled_classes)

@routes.route('/user_unenroll_class/<int:class_id>', methods=['POST'])
def user_unenroll_class(class_id):
    if 'user_id' not in session:
        flash("Debes iniciar sesión como usuario", "danger")
        return redirect(url_for('routes.login_user'))

    user_id = session['user_id']

    try:
        # Llamar a la lógica de negocio para eliminar la inscripción
        business_logic.delete_enrollment(user_id, class_id)
        flash("Inscripción eliminada exitosamente.", "success")
    except RuntimeError as e:
        flash(f"Error al eliminar la inscripción: {e}", "danger")

    # Redirigir a la lista de clases inscritas
    return redirect(url_for('routes.user_enrolled_classes'))