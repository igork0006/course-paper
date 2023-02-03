import os
from flask import Blueprint, render_template, current_app, request
from sql_provider import SQLProvider
from db_work import call_proc, select, update
from access import login_required, group_required

blueprint_edit = Blueprint('bp_edit', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_edit.route('/menu', methods=['GET', 'POST'])
def start_page():
    return render_template('edit_menu.html')


@blueprint_edit.route('/edit_order', methods=['GET', 'POST'])
def edit_order():
    if request.method == 'GET':
        _sql = provider.get('all_orders.sql')
        all_result, schema = select(current_app.config['db_config'], _sql)
        return render_template('edit_order.html', result=all_result, schema=schema)
    else:
        idOrder = request.form.get('id')
        status = request.form.get('status')
        if idOrder and status:
            _sql = provider.get('update.sql', status=status, id=idOrder)
            update(current_app.config['db_config'], _sql)
            _sql = provider.get('edited_order.sql', id=idOrder)
            report, schema = select(current_app.config['db_config'], _sql)
            # new_schema = ['Номер отчета', 'Сумма всех заказов поставщика', 'Номер поставщика', 'Месяц отчета',
            #               'Год отчета']
            return render_template('edit_result.html', schema=schema, result=report)


@blueprint_edit.route('/edit_2', methods=['GET', 'POST'])
def edit_2():
    return "заглушка"


@blueprint_edit.route('/edit_3', methods=['GET', 'POST'])
def edit_3():
    return "заглушка"

