import os  # работа с объектами операционной системы

from flask import Blueprint, request, render_template, current_app  # глобальная переменная с конфигом app
from db_work import select
from sql_provider import SQLProvider
from access import login_required, group_required


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')  # создание blueprint'а

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))  # создание словаря для текущего blueprint'а


@blueprint_query.route('/')
@login_required
def menu():
    return render_template('query_menu.html')


@blueprint_query.route('/product', methods=['GET', 'POST'])
@group_required
def product():
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
            _sql = provider.get('product.sql', input_product=input_product)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if product_result:
                new_schema = ['Штрих-код продукта', 'Название', 'Единица изменения', 'Цена за единицу']
                return render_template('query_result.html', name="Описание искомого вами продукта", schema=new_schema,
                                       result=product_result)
            else:
                return render_template('error_query.html')
        else:
            return "Repeat input"


@blueprint_query.route('/buyer', methods=['GET', 'POST'])
@group_required
def buyer():
    if request.method == 'GET':
        return render_template('buyer_form.html')
    else:
        input_buyer = request.form.get('buyer_name')
        if input_buyer:
            _sql = provider.get('buyer.sql', input_buyer=input_buyer)
            buyer_result, schema = select(current_app.config['db_config'], _sql)
            if buyer_result:
                new_schema = ['Номер поставщика', 'Имя', 'Адрес', 'Номер телефона', 'Реквизиты', 'Дата регистации']
                return render_template('query_result.html', name="Данные поставщика " + input_buyer, schema=new_schema,
                                       result=buyer_result)
            else:
                return render_template('error_query.html')
        else:
            return "Repeat input"


@blueprint_query.route('/order', methods=['GET', 'POST'])
@group_required
def order():
    if request.method == 'GET':
        return render_template('order_form.html')
    else:
        input_order = request.form.get('order_id')
        if input_order:
            _sql = provider.get('order.sql', input_order=input_order)
            order_result, schema = select(current_app.config['db_config'], _sql)
            if order_result:
                new_schema = ['Номер заказа', 'Статус', 'Сумма', 'Дата получения заказа', 'Дата отмены заказа',
                              'Дата оплаты', 'Номер поставщика']
                return render_template('query_result.html', name="Данные заказа ", schema=new_schema, result=
                order_result)
            else:
                return render_template('error_query.html')
        else:
            return "Repeat input"