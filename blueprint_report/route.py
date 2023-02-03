import os
from flask import Blueprint, render_template, current_app, request
from sql_provider import SQLProvider
from db_work import call_proc, select
from access import login_required, group_required

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/view', methods=['GET', 'POST'])
@group_required
def view():
    return render_template('created_reports.html')


@blueprint_report.route('/create', methods=['GET', 'POST'])
@group_required
def create():
    return render_template('create_menu.html')


@blueprint_report.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    return render_template('menu_report.html')


@blueprint_report.route('/report1', methods=['GET', 'POST'])
@group_required
def report1():
    if request.method == 'GET':
        _sql = provider.get('all_reports.sql')
        report, schema = select(current_app.config['db_config'], _sql)
        new_schema = ['Номер отчета', 'Сумма всех заказов поставщика', 'Номер поставщика', 'Месяц отчета', 'Год отчета']
        if report:
            return render_template('report1.html', schema=new_schema, result=
                    report)
        else:
            return 'тут пока что пусто: надо бы создать отчеты('
    else:
        report_month = request.form.get('report_month')
        report_year = request.form.get('report_year')
        if report_month and report_year:
            _sql = provider.get('check_report.sql', rep_month=report_month, rep_year=report_year)
            report, schema = select(current_app.config['db_config'], _sql)
            new_schema = ['Номер отчета', 'Сумма всех заказов поставщика', 'Номер поставщика', 'Месяц отчета', 'Год отчета']
            return render_template('report1_updated.html', schema=new_schema, result=report, month=report_month, year=report_year)


@blueprint_report.route('/report2', methods=['GET', 'POST'])
@group_required
def report2():
    return 'отчет 2'


@blueprint_report.route('/report3', methods=['GET', 'POST'])
@group_required
def report3():
    return 'отчет 3'


@blueprint_report.route('/create1', methods=['GET', 'POST'])
@group_required
def create1():
    if request.method == 'GET':
        return render_template('create_report_form.html')
    else:
        report_month = request.form.get('report_month')
        report_year = request.form.get('report_year')
        if report_month and report_year:
            _sql = provider.get('check_report.sql', rep_month=report_month, rep_year=report_year)
            request_result, schema = select(current_app.config['db_config'], _sql)
            print(request_result, schema)
            if request_result:
                return render_template('report_done.html', text="Такой отчет уже существует")
            else:
                res = call_proc(current_app.config['db_config'], 'order_report', report_month, report_year)
                print(res)
                return render_template('report_done.html', text="Ваш отчет успешно создан")
        else:
            return render_template('report_done.html', text="Некорректно введена дата")


@blueprint_report.route('/create2', methods=['GET', 'POST'])
@group_required
def create2():
    return 'создание отчета 2'


@blueprint_report.route('/create3', methods=['GET', 'POST'])
@group_required
def create3():
    return 'создание отчета 3'

