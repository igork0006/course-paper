insert into _order (idOrder, status, amount, order_date, cancellation_date, payment_date, idBuyer)
	values(NULL,
	        '2',
	        NULL,
	        curdate(),
	        date_add(curdate(),INTERVAL 3 DAY),
	        curdate(),
			'$user_id');