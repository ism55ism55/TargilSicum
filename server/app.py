import json
from flask import Flask, request
from TargilSicum.server import myworker

json_data_file = ".\\employesObj.json"
myWorker = myworker.Worker(json_data_file)
base_url = "http://127.0.0.1/"
app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Ping-Pong'




@app.route('/addemployee', methods=['POST'])
def add_employee():

    emp_dict = dict()
    json_date = request.get_json()

    # response = app.response_class(
    #     response=json.dumps(json_date),
    #     status=200,
    #     mimetype='application/json'
    # )
    # return response

    myWorker.add_employee(json_date)


@app.route('/updatesalary', methods=['GET'])
def update_salary():
    increment = request.args.get('increment')
    user = request.args.get('user')
    return myWorker.update_salary(user, increment)


@app.route('/update_salary_all', methods=['GET'])
def update_salary_all():
    incprecent = request.args.get('incprecent')
    return myWorker.update_salary_all(incprecent)


@app.route('/deluser', methods=['GET'])
def remove_emp():
    user = request.args.get('user')
    return myWorker.remove_employee(user)


@app.route('/deldb', methods=['POST'])
def delete_database():
    return json.dumps(myWorker.delete_db())


@app.route('/loadnewdb', methods=['POST'])
def load_new_db():
    new_db_file_name = request.args.get('file')
    return json.dumps(myWorker.load_new_db(new_db_file_name))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
