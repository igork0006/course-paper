import os
from flask import *
from db_work import *
from sql_provider import *
from access import *


blueprint_order = Blueprint('bp_order', __name__, template_folder='templates', static_folder='static')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order.route('/', methods=['GET', 'POST'])
@group_required
def order_index():
    db_config = current_app.config['db_config']
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)

        print('items = ', items)
        basket_items = session.get('basket', {})
        return render_template('basket_order_list.html', items=items, basket=basket_items)
    else:
        idProduct = request.form['idProduct']
        amount = request.form['amount']
        print(amount)
        sql = provider.get('select_item.sql', prod_id=idProduct)
        items = select_dict(db_config, sql)
        print('items = ', items)
        add_to_basket(idProduct, items, amount)
        return redirect(url_for('bp_order.order_index'))


def add_to_basket(idproduct, items: dict, amount):
    curr_basket = session.get('basket', {})
    if idproduct in curr_basket:
        if curr_basket[idproduct]['productcol'] < items[0]['productcol']:
            curr_basket[idproduct]['productcol'] = curr_basket[idproduct]['productcol']+int(amount)
        else:
            return True
    else:
        curr_basket[idproduct] = {
            'name': items[0]['name'],
            'price': items[0]['price'],
            'productcol': int(amount)
        }
        session['basket'] = curr_basket
        session.permanent = True
    return True


@blueprint_order.route('/save_order', methods=['GET', 'POST'])
@group_required
def save_order():
    user_id = session.get('user_id')
    current_basket = session.get('basket', {})
    order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket)
    if order_id:
        session.pop('basket')
        return render_template('order_created.html', order_id=order_id)
    else:
        return 'something went wrong'


def save_order_with_list(dbconfig: dict, user_id: int, current_basket):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Cursor not created')
        print("created")
        print(user_id)
        _sql1 = provider.get('insert_order.sql', user_id=user_id)
        print(_sql1)
        result1 = cursor.execute(_sql1)
        if result1 == 1:
            _sql2 = provider.get('select_order_id.sql', user_id=user_id)
            cursor.execute(_sql2)
            order_id = cursor.fetchall()[0][0]
            print('order_id= ', order_id)
            if order_id:
                for key in current_basket:
                    print(current_basket[key])
                    print(key, current_basket[key]['productcol'])
                    prod_amount = current_basket[key]['productcol']
                    _sql3=provider.get('insert_order_list.sql', prod_amount=prod_amount, order_id=order_id, prod_id=key)
                    print(_sql3)
                    cursor.execute(_sql3)
                return order_id


@blueprint_order.route('/clear_basket')
@group_required
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_order.order_index'))