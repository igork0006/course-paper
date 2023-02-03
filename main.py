from flask import Flask, render_template, request, url_for, redirect, json, session
from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report
from auth.route import blueprint_auth
from access import login_required, group_required
from blueprint_basket.route import blueprint_order

app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/zaproses')
app.register_blueprint(blueprint_report, url_prefix='/reports')
# app.register_blueprint(blueprint_edit, url_prefix='/edit')
app.register_blueprint(blueprint_order, url_prefix='/order')

app.config['db_config'] = json.load(open('data_files/dbconfig.json'))
app.config['access_config'] = json.load(open('data_files/access.json'))


@app.route('/exit')
@login_required
def goodbye():
    session.clear()
    return render_template('hello.html')


@app.route('/')
def start():
    return render_template('hello.html')


@app.route('/menu', methods=['GET', 'POST'])
@login_required
def menu_choice():
    if session.get('user_group') == 'external':
        return render_template('external_user_menu.html')
    else:
        return render_template('internal_user_menu.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
