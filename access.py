from functools import wraps

from flask import session, render_template, current_app, request, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('blueprint_auth.start_auth'))
    return wrapper


def group_validation(config: dict) -> bool:
    endpoint_func = request.endpoint
    print('endpoint_func', endpoint_func) # имя блюпринта.имя обработчика
    endpoint_app = request.endpoint.split('.')[0]
    print('endpoint_app', endpoint_app) # имя блюпринта
    if 'user_group' in session:
        user_group = session['user_group']
        print(user_group)
        if user_group in config and endpoint_app in config[user_group]:
            return True #если есть имя блюпринта
        elif user_group in config and endpoint_func in config[user_group]:
            return True  #если есть имя блюпринта+обработчика
    return False


def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return f(*args, **kwargs)
        return render_template('error_report.html', text="У вас недостаточно прав доступа")
    return wrapper
