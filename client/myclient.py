import pytest
from server import myworker
import requests

json_data_file = "C:\\Users\\user96\\PycharmProjects\\TargilSicum\\employesObj.json"
myWorker = myworker.Worker(json_data_file)




def test_cant_add_more_then_10():

    assert myWorker.add_employee("ilan", "10000", "qa", "10//10//1973", "python", "Haifa") >= 10


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
