import pytest
import requests
import json
#import TargilSicum.Logger
import Logger
import operator
from collections import OrderedDict
from datetime import datetime


test_db_file = ".\\testDB.json"
base_url = "http://127.0.0.1:5000"
logger = Logger.get_logger(log_path='.\\', log_name='ClientLogger')

def load_test_db(db_file):
    json_content = dict()
    try:
        with open(db_file, 'r') as in_file:
            json_content = in_file.read().translate('UTF-8')
        if in_file is not None:
                in_file.close()
    except IOError as error:
        logger.debug("Exception: content {}".format(error))

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
                    logger.debug("Test Failed: More then 10, actual number:{}".format(len(json_data['response']['employies'])))
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
                        logger.debug("Test Failed: Found user {} with salary of {}".format(json_data['response']['employies'][empl]['name'], str(json_data['response']['employies'][empl]['salary'])))
                        assert False
        assert True


def test_pension_age():
    ## Test success if one or more of the employees are >= age 67
    found_in_db = False
    curr_year = datetime.now().year
    try:
        res = requests.post(url=base_url + "/loadnewdb?file=reload")
    except requests.exceptions as error:
        logger.debug("Exception: content {}".format(error))

    if res.status_code in [400, 200]:
        json_data = json.loads(res.text)
        obj = json_data['response']['employies']
        if any(obj):
            for empl in obj:
                if curr_year - int(obj[empl]['birthday']['year']) >=67:
                    logger.debug("Test Success: Found user {} with age {}".format(empl, curr_year - int(obj[empl]['birthday']['year'])))
                    found_in_db = True

            logger.debug("Test Failed: Non of the users is 67 or above")

    assert found_in_db


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
                logger.debug("Test Success: Found user {} with birthday - Test".format(empl))
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
                    logger.debug("Test Fail: Wasnt able to remove user {}".format(user_to_remove))
                else:
                    logger.debug("Test Fail: Wasnt able to remove user {} user not found".format(user_to_remove))
            else:
                if user_to_remove in json_data['response']['employies']:
                    logger.debug("Test Fail: Wasnt able to remove user {}".format(user_to_remove))
                else:
                    logger.debug("Test Success: Employee {} was successfully removed".format(user_to_remove))
                    test_res = True
    assert test_res


@pytest.mark.servertest
def test_add_exisitng_employee():

    test_res = False
    ## trying to add an already existing emp if success then failing the test
    json_in = json.loads(load_test_db(test_db_file))

    try:
        res = requests.post(url=base_url + "/addemployee", json=json_in)
    except requests.exceptions as error:
        logger.debug("Exception: content {}".format(error))

    json_data = json.loads(res.text)
    for added_user in json_in['employies']:
        added_user = json_in['employies'][added_user]['name']

    if res.status_code == 200:
        if added_user in json_data['response']['employies']:
           logger.debug("Test Fail: Server responded with success adding existing user {} expected result 4000".format(added_user))
        else:
            logger.debug("Test Fail: Server responded with success adding existing user {} however it isn't found in DB ???".format(added_user))
    else: # response was 400
        if added_user in json_data['response']['employies']:
            test_res = True
            logger.debug("Test Success: User {} found and wasn't added server responded with 400".format(added_user))
        else: # user is not found however server still responded with 400
            logger.debug("Test Fail: Server responded with failure for adding existing user {} however it i'snt found in DB - failing the test".format(added_user))

    assert test_res



@pytest.mark.servertest
def sort_by_salary():
    sort_success = False

    try:
        res = requests.post(url=base_url + "/loadnewdb?file=reload")
    except requests.exceptions as error:
        logger.debug("Exception: content {}".format(error))

    if res.status_code in [400, 200]:
        json_data = json.loads(res.text)
        obj = json_data['response']['employies']
        sorted_obj = dict()
        sorted_obj = OrderedDict(sorted(obj.items(), key=lambda x: x[1]['salary']))

        if any(sorted_obj):
            logger.debug("Test Success: sorted list by Salary{}".format(str(sorted_obj)))
            sort_success = True

        else:
            logger.debug("Test Failed: failed to soart DB by Salary")

    assert sort_success


if __name__ == "__main__":
    sort_by_salary()
