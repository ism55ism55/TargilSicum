import pytest
import requests
import json
import TargilSicum.Logger
from datetime import datetime


test_db_file = ".\\inJson.json"
base_url = "http://127.0.0.1:5000"
logger = TargilSicum.Logger.get_logger(log_path='.\\', log_name='ClientLogger')

def load_test_db(db_file):
    try:
        with open(db_file, 'r') as in_file:
            json_content = in_file.read().translate('UTF-8')
    except IOError as error:
        logger.debug("Exception: content {}".format(error))

    if in_file is not None:
        in_file.close()
    return json_content


@pytest.mark.servertest
def test_cant_add_more_then_10():

    ## Using a json::in file and running through the entries trying to add more than 10 users
    ## if is succeed then Test == FAILS

    json_in = json.loads(load_test_db(test_db_file))

    for idx in range(len(json_in['employies'])):
        try:
            res = requests.post(url = base_url + "/addemployee", json= json_in)
        except requests.exceptions as error:
            logger.debug("Exception: content {}".format(error))

        if res.status_code in [400, 200]:
            json_data = json.loads(res.text)
            if any(json_data['response']['employies']):
                if len(json_data['response']['employies']) > 10:
                    logger.debug("More then 10, actual number:{}- Test failed".format(len(json_data['response']['employies'])))
                    assert False
    assert True

@pytest.mark.servertest
def test_high_salary():
    ## Increasing Sallary by 20% to all
    ## Passing the test if found Sallary > 35000
        try:
            res = requests.post(url=base_url + "/update_salary_all?incprecent=20")
        except requests.exceptions as error:
            logger.debug("Exception: content {}".format(error))

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

@pytest.mark.servertest
def test_employee_bd_this_month():

    ## Test is successful is i find emp with BD this month
    today = datetime.now().today()
    found_db = False
    try:
        res = requests.get(url=base_url + "/birthday_employee?month="+str(today.month))
    except requests.exceptions as error:
        logger.debug("Exception: content {}".format(error))

    if res.status_code in [400, 200]:
        json_data = json.loads(res.text)
        if any(json_data['response']):
            for empl in json_data['response']:
                #if int(json_data['response'][empl]['birthday']['month']) == today.month:
                logger.debug("Found user {} with birthday - Test".format(empl))
                found_db = True

    assert found_db


@pytest.mark.servertest
def test_del_employee():

    ## trying to remove user Passing test if success , Failing is remove failed from some reason
    test_res = False
    user_to_remove = "ilan"
    try:
        res = requests.post(url=base_url + "/deluser?user=" + user_to_remove )
    except requests.exceptions as error:
        logger.debug("Exception: content {}".format(error))

    if res.status_code in [400, 200]:
        json_data = json.loads(res.text)
        if any(json_data['response']):
            if res.status_code == 400:
                if user_to_remove in json_data['response']['employies']:
                    logger.debug("Wasnt able to remove user {}".format(user_to_remove))
                else:
                    logger.debug("Wasnt able to remove user {} user not found".format(user_to_remove))
            else:
                if user_to_remove in json_data['response']['employies']:
                    logger.debug("Wasnt able to remove user {}".format(user_to_remove))
                else:
                    logger.debug("Employee {} was successfully removed".format(user_to_remove))
                    test_res = True
    assert test_res


@pytest.mark.servertest
def test_add_exisitng_employee():

    ## trying to add existing emp if success then failing the test 
    json_in = json.loads(load_test_db(test_db_file))

    try:
        res = requests.post(url=base_url + "/addemployee", json=json_in)
    except requests.exceptions as error:
        logger.debug("Exception: content {}".format(error))

    json_data = json.loads(res.text)
    added_user= json_in['employies']['name']

    if res.status_code == 200:
        if added_user in json_data['response']['employies']:
           test_res = True
           logger.debug("User {} ".format(added_user))
        else:
            test_res = False
            logger.debug("Server resondes with success for adding existing user {} however it isnt found in DB ???".format(added_user))

    else:
        if added_user in json_data['response']['employies']:
            test_res = True
            logger.debug("User {} found and was wasnt removed".format(added_user))
                else:
                    test_res = False
                    logger.debug(
                        "Server resondes with success for adding existing user {} however it isnt found in DB ???".format(
                            added_user))

                    assert False
    assert True



if __name__ == "__main__":
    test_add_exisitng_employee()
