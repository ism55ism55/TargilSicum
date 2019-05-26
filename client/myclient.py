import pytest
import requests
import json

test_db_file = "C:\\Users\\user96\\PycharmProjects\\TargilSicum\\testDB.json"
#myWorker = myworker.Worker(json_data_file)
base_url = "127.0.0.1:5000"


def load_test_db(self):
    with open(test_db_file, 'r') as in_file:
        json_content = in_file.read().translate('UTF-8')
        in_file.close()
    return json_content


def test_cant_add_more_then_10():
    json_in = json.loads(load_test_db())
    for idx in range(10):

        res_json = requests.post(url = base_url + "/loadnewdb?file=morethen10.json", json= json_in)
    assert len(res_json) > 10


def test_high_salary():
    ## test success if i increase sallery by x % and no one pass the 35000 boundery
    assert myWorker.update_salary_all("10") == True


def test_pension_age():
    ## Test success if one or more of the employees are >= age 67
    employee_list = myWorker.employee_age()
    assert len(employee_list) > 0

def test_employee_bd_this_month():
    employee_list = myWorker.birthday_employees('1')
    if len(employee_list) >0:
        print("List of employees with BD this month {}".format(employee_list))
    assert len(employee_list) > 0


def test_del_employee():
    assert myWorker.remove_employee("ilan") == False


def test_add_exisitng_employee():
    assert myWorker.check_if_user_exists("ilan") == True


# if __name__ == "__main__":
#     myProcess = Process()
#     myProcess.CreateNewUser("SelfTest@SelfTestMail.com", "SelfTesUser", "SelfTestPass")
#
