import json
from flask import Flask, request
from TargilSicum.server import myworker

json_data_file = ".\\employesObj.json"
success_json = ".\\success.json"
fail_json = ".\\fail.json"

myWorker = myworker.Worker(json_data_file)
base_url = "http://127.0.0.1/"
app = Flask(__name__)

json_success_res = json.loads(myWorker.get_json_data_from_file(success_json))
json_fail_res = json.loads(myWorker.get_json_data_from_file(fail_json))


def handle_response(res, val):

    if res is 200:
        response = json.dumps({'response': val})
        status = 200
    else:
        response = json.dumps({'response': val})
        status = 400

    response = app.response_class(
        response=response,
        status=status,
        mimetype='application/json; charset=utf-8'
    )

    return response


@app.route('/', methods=['GET'])
def hello_world():
    return 'Ping-Pong'




@app.route('/addemployee', methods=['POST'])
def add_employee():

    status = 400
    json_data = dict()

    json_data = request.get_json()
    if any(json_data):
        res = myWorker.add_employee(json_data)
        if res:
            status = 200
    json_data = myWorker.load_new_db(json_data_file)
    return handle_response(status, json_data)




@app.route('/updatesalary', methods=['GET'])
def update_salary():
    res_json = dict()
    status = 400
    increment = request.args.get('increment')
    user = request.args.get('user')

    if increment and user:
        res_json = myWorker.update_salary(user,increment )
        if res_json != None:
            if any(res_json):
                status = 200

    response = handle_response(status, res_json)

    return response


@app.route('/update_languages', methods=['POST'])
def update_prog_lang():
    res_json = dict()
    status = 400
    programs = request.args.get('prog')
    user = request.args.get('user')

    if user and programs:
        res_json = myWorker.add_programming_laguage(user, programs)
        if res_json != None:
            if any(res_json):
                status = 200

    response = handle_response(status, res_json)

    return response


@app.route('/birthday_employee', methods=['GET'])
def get_bd_employees():
    res_json = dict()
    status = 400

    month = request.args.get('month')
    if month:
        res_json = myWorker.birthday_employees(month)
        if any(res_json):
                status = 200

    response = handle_response(status, res_json)
    return response



@app.route('/update_salary_all', methods=['POST'])
def update_salary_all():
    res_json = dict()
    status = 400

    incprecent = request.args.get('incprecent')
    if incprecent:
        res_json = myWorker.update_salary_all(incprecent)
        if any(res_json):
            status = 200

    response = handle_response(status, res_json)

    return response


@app.route('/deluser', methods=['POST'])
def remove_emp():

    status = 400
    result = False
    user = request.args.get('user')
    if user:
        result = myWorker.remove_employee(user)
        if result:
            status = 200
    json_data = myWorker.load_new_db(json_data_file)
    return handle_response(status, json_data)



@app.route('/deldb', methods=['POST'])
def delete_database():
    return json.dumps(myWorker.delete_db())


@app.route('/loadnewdb', methods=['POST'])
def load_new_db():
    res_json = dict()
    status = 400
    result = False
    new_db_file_name = request.args.get('file')
    if new_db_file_name:
        res_json = json.dumps(myWorker.load_new_db(new_db_file_name))
        if any(res_json):
                status = 200

    return handle_response(status, res_json)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
