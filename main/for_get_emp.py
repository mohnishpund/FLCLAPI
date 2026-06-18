from database_conn import get_db_connection
from app import app
from flask import jsonify, json, request

from is_log_in import is_logged_in

@app.route('/employee', methods=['GET'])
@is_logged_in
def employee_data():
    conn = get_db_connection()

    if conn is None:
        return jsonify({"error": "Database is currently offline."}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT JSON_OBJECT(*) FROM employees")
        raw_data = cursor.fetchall()
        
        # This converts every row into a curly-brace dictionary {}
        data = [json.loads(row[0]) for row in raw_data]
        
        # CHOOSE YOUR STARTING POINT HERE:
        return jsonify({"Result": data})  # Starts with {
        # OR use: return jsonify(data)    # Starts with [

    except Exception as e:
        print("Error fetching employees:", e)
        return jsonify({"error": "Could not fetch data"}), 500
        
    finally:
        if conn:
            conn.close()


@app.route('/employee_get/<int:employee_id>', methods=['GET'])
@is_logged_in
def emp_get_id(employee_id):
	conn = get_db_connection()

	if conn is None:
		return jsonify({'error': 'Database is currently offline.'}), 500

	try:
		cursor = conn.cursor()
		cursor.execute("SELECT JSON_OBJECT(*) FROM employees where employee_id = :1", [employee_id])
		row = cursor.fetchone()
		if row is None:
			return jsonify({"error": "Employee not found"}), 404
		data = json.loads(row[0])
		return json.dumps(data, indent=2), 200
	except Exception as e:
		print('Error fetching employees:', e)
		return jsonify({"error": "Could not fetch data"}), 500
	finally:
		if conn:
			conn.close()




@app.route('/emp_post', methods=['POST'])
@is_logged_in
def post_emp():
	try:	
		#install connection
		conn = get_db_connection()

		# start form input
		forms = request.form
		_employee_id = forms['employee_id']
		_first_name = forms['first_name']
		_last_name = forms['last_name']
		_email = forms['email']
		_phone_number = forms['phone_number']
		_hire_date = forms['hire_date']
		_job_id = forms['job_id']
		_salary = forms['salary']
		_commission_pct = forms['commission_pct']
		_manager_id = forms['manager_id']
		_department_id = forms['department_id']

		#add request and sql Query
		cursor = conn.cursor()

		if _employee_id and _first_name and _last_name and _email and _phone_number and _hire_date and _job_id and _salary and _commission_pct and _manager_id and _department_id and request.method == 'POST':
			sql_orcl_query = """INSERT INTO EMPLOYEES (
						        employee_id, first_name, last_name, email, phone_number, 
						        hire_date, job_id, salary, commission_pct, manager_id, department_id
						    ) VALUES (
						        :employee_id, :first_name, :last_name, :email, :phone_number, 
						        TO_DATE(:hire_date, 'DD-MON-RR'), :job_id, :salary, :commission_pct, :manager_id, 
						        :department_id
						    )"""

			bind_data = (_employee_id, _first_name, _last_name, _email, _phone_number, 
						_hire_date, _job_id, _salary, _commission_pct, _manager_id, _department_id)


			cursor.execute(sql_orcl_query, bind_data)
			conn.commit()
			msg = ({
                "Result": "Your data was successfully inserted into table employees",
                "Inserted Data": bind_data, 
                "status": "success"
            }), 201

		else:

			msg = ({"error": "Body not found"}), 400
			

	except Exception as e:
		print('Error adding employees data:', e)
		return jsonify({"error": "Could not add data"}), 500
	finally:
		return jsonify(msg)
		if conn:
			conn.close()



@app.route('/emp_update/<int:employee_id>', methods=['PUT'])
@is_logged_in
def put_emp(employee_id):
	try:	
		#install connection
		conn = get_db_connection()

		# start form input
		forms = request.form

		_employee_id = employee_id
		_first_name = forms['first_name']
		_last_name = forms['last_name']
		_email = forms['email']
		_phone_number = forms['phone_number']
		_hire_date = forms['hire_date']
		_job_id = forms['job_id']
		_salary = forms['salary']
		_commission_pct = forms['commission_pct']
		_manager_id = forms['manager_id']
		_department_id = forms['department_id']

		#add request and sql Query
		cursor = conn.cursor()

		if _first_name and _last_name and _email and _phone_number and _hire_date and _job_id and _salary and _commission_pct and _manager_id and _department_id and request.method == 'PUT':
			sql_orcl_query = """UPDATE EMPLOYEES SET  
									first_name=:first_name, 
									last_name=:last_name, 
									email=:email, 
									phone_number=:phone_number, 
									hire_date=:hire_date, 
									job_id=:job_id, 
									salary=:salary, 
									commission_pct=:commission_pct, 
									manager_id=:manager_id, 
									department_id=:department_id where employee_id=:employee_id"""

			bind_data = (_first_name, _last_name, _email, _phone_number, 
						_hire_date, _job_id, _salary, _commission_pct, _manager_id, _department_id, _employee_id)

			data  = json.dumps(bind_data, indent=4)

			cursor.execute(sql_orcl_query, bind_data)
			conn.commit()

			pretty_data = json.dumps(bind_data, indent=4)

			msg = {
				"Result": "Your data was successfully updated into table",
				"Updated Data": bind_data,
				"status": "success"}

			return jsonify(msg), 200

		else:

			msg = ({"error": "Body not found"}), 400
			

	except Exception as e:
		print('Error updated employees data:', e)
		return jsonify({"error": "Could not put data"}), 500
	finally:
		return jsonify(msg)
		if conn:
			conn.close()



@app.route('/emp_delete/<int:employee_id>', methods=['DELETE'])
@is_logged_in
def emp_delete(employee_id):
	conn = get_db_connection()
	try:
		cursor = conn.cursor()
		if request.method == "DELETE":
			emp_d = "DELETE FROM EMPLOYEES WHERE employee_id = :employee_id"
			cursor.execute(emp_d, {"employee_id": employee_id})
			conn.commit()

			if cursor.rowcount == 0:
				msg = ({"error": f"Employee ID {employee_id} not found"}), 404

			msg = ({
                "Result": f"Employee {employee_id} deleted successfully.",
                "status": "success"
           }), 200

		else:

			msg = ({'error': "request query not found"})

	except Exception as e:
		print('Error deleted employee data:', e)
		return jsonify({"error": "Could not delete data"}), 500
	finally:
		return jsonify(msg)
		if conn:
			conn.close()



