import pytest
import requests
import json
import TargilSicum.Logger
from datetime import datetime


test_db_file = ".\\inJson.json"
base_url = "http://127.0.0.1:5000"
logger = TargilSicum.Logger.get_logger(log_path='.\\', log_name='ClientLogger')

def load_test_db(db_file):
    with open(db_file, 'r') as in_file:
        json_content = in_file.read().translate('UTF-8')

    in_file.close()
    return json_content


def test_cant_add_more_then_10():
    json_in = json.loads(load_test_db(test_db_file))

    for idx in range(len(json_in['employies'])):
        res = requests.post(url = base_url + "/addemployee", json= json_in)
        if res.status_code in [400, 200]:
            json_data = json.loads(res.text)
            if any(json_data['response']['employies']):
                if len(json_data['response']['employies']) > 10:
                    logger.debug("More then 10, actual number:{}- Test failed".format(len(json_data['response']['employies'])))
                    assert False
    assert True


def test_high_salary():
    ## test success if i increase sallery by x % and no one pass the 35000 boundery
        res = requests.post(url=base_url + "/update_salary_all?incprecent=20")
        if res.status_code in [400, 200]:
            json_data = json.loads(res.text)
            if any(json_data['response']['employies']):
                for empl in json_data['response']['employies']:
                    if int(json_data['response']['employies'][empl]['salary']) > 35000:
                        logger.debug("Found user {} with salary of {} - Test Failed".format(json_data['response']['employies'][empl]['name'], str(json_data['response']['employies'][empl]['salary'])))
                        assert False
        assert True

#
# def test_pension_age():
#     ## Test success if one or more of the employees are >= age 67
#     employee_list = myWorker.employee_age()
#     assert len(employee_list) > 0
#

def test_employee_bd_this_month():

    today = datetime.now().today()
    found_db = False

    res = requests.get(url=base_url + "/birthday_employee?month="+str(today.month))
    if res.status_code in [400, 200]:
        json_data = json.loads(res.text)
        if any(json_data['response']):
            for empl in json_data['response']:
                #if int(json_data['response'][empl]['birthday']['month']) == today.month:
                logger.debug("Found user {} with birthday - Test".format(empl))
                found_db = True

    assert found_db


#
# def test_del_employee():
#     assert myWorker.remove_employee("ilan") == False
#
#
# def test_add_exisitng_employee():
#     assert myWorker.check_if_user_exists("ilan") == True


if __name__ == "__main__":
    test_employee_bd_this_month()
