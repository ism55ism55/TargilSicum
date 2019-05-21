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

    if res is True:
        response = json.dumps({'Server Status:': 'Success', 'response': val})
        status = 200
    else:
        response = json.dumps({'Server Status:': 'Success', 'response': val})
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

    response = dict()
    json_data = request.get_json()
    res = myWorker.add_employee(json_data)
    return handle_response(res)




@app.route('/updatesalary', methods=['GET'])
def update_salary():

    res_json = dict()
    status = 400
    increment = request.args.get('increment')
    user = request.args.get('user')

    res_json = myWorker.update_salary(user,increment )

    if any(res_json):
        status = 200

    response = handle_response(status, res_json)

    return response




@app.route('/update_salary_all', methods=['POST'])
def update_salary_all():
    response = dict()
    status = 400

    incprecent = request.args.get('incprecent')
    res_json = myWorker.update_salary_all(incprecent)

    if any(res_json):
        status = 200

    response = app.response_class(
        response=json.dumps(res_json),
        status=200,
        mimetype='application/json; charset=utf-8'
    )

    return response


@app.route('/deluser', methods=['POST'])
def remove_emp():
    user = request.args.get('user')
    res = myWorker.remove_employee(user)
    bRest = False
    if res > 0:
        bRest = True

    return handle_response(bRest, "")


@app.route('/deldb', methods=['POST'])
def delete_database():
    return json.dumps(myWorker.delete_db())


@app.route('/loadnewdb', methods=['POST'])
def load_new_db():
    new_db_file_name = request.args.get('file')
    return json.dumps(myWorker.load_new_db(new_db_file_name))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
