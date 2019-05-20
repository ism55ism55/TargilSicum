import datetime
import json
import Logger

class Worker:

    json_data = dict()
    logger = Logger.get_logger(log_path='.\\', log_name='ServerLogger')

    def __init__(self, json_file_path ):
        self.logger.debug("Starting Server")
        self.logger.debug("Loading DB")
        self.global_db_path = json_file_path
        self.json_data = json.loads(self.get_json_data_from_file(self.global_db_path))


    def write_to_json_file(self, json_file_path):
        json_from_dict = json.dumps(self.json_data,indent=4)
        with open(json_file_path, 'w') as out_file:
            out_file.write(json_from_dict)
        out_file.close()


    def get_json_data_from_file(self, json_file_path):
        with open(json_file_path, 'r') as in_file:
            json_content = in_file.read().translate('UTF-8')
            in_file.close()
        return json_content


    def check_if_user_exists(self, username):

        obj = self.json_data['employies']

        if username in obj:
            print("User exists - not adding the new user {}".format(username))
            self.json_data("User exists - not adding the new user {}".format(username))
            return True
        return False

        ##for entry in self.json_data['employies']:
        ##range(len(self.json_data['employies'])):
        #if username == self.json_data['employies'][entry]['name']:



    def check_num_of_employees(self):
        return len(self.json_data['employies'])

    def add_employee(self, json_obj):
        for entry in json_obj['employies']:
            if json_obj['employies'][entry]['name'] != "" and json_obj['employies'][entry]['salary'] != "" and json_obj['employies'][entry]['department'] != "" \
                and json_obj['employies'][entry]['programs'] != "" and json_obj['employies'][entry]['birthday'] != "" and json_obj['employies'][entry]['adress']:

                if not self.check_if_user_exists(json_obj['employies'][entry]['name']):
                    if self.json_data['employies'].update(json_obj['employies']) is None:
                        return True
            else:
                    self.logger.debug("Failed Adding new user one of the values is empty: " + str(json_obj) )
                    print("Failed Adding new user one of the values is empty: " + str(json_obj))

        return False



    def remove_employee (self, username):
        if username != "":
            for i in range(len(self.json_data['employies'])):
                if username == self.json_data['employies'][i]['name']:
                    print("Found user {} removing user".format(username))
                    self.logger.debug("Found user {} removing user".format(username))
            self.json_data.pop(self.json_data['employee'][i]['name'])
            return True

        else:
            self.logger.debug("Failed removing user - values is empty {}".format(username))
            print("Failed removing user - values is empty {}".format(username))
            return False


    def update_salary (self, username, increment):

        if username != "":
            for i in range(len(self.json_data['employies'])):
                if username == self.json_data['employies'][i]['name']:
                        if self.json_data['employies'][i]['salary'] is not None:
                            new_salary = int(self.json_data['employies'][i]['salary']) + int (increment)
                            self.json_data['employies'][i]['salary'] = str(new_salary)
                            if new_salary > 35000:
                                print("Found user {} with Salary > 350000, Salry is {}".format(username,self.json_data['employies'][i]['salary']))
                                self.logger.debug("Found user {} with Salary > 350000, Salry is {}".format(username,self.json_data['employies'][i]['salary']))
                            print("Found user {} Adding Salary, new Salry is {}".format(username, self.json_data['employies'][i]['salary']))
                            self.logger.debug("Found user {} Adding Salary, new Salry is {}".format(username, self.json_data['employies'][i]['salary']))
                        else:
                            print("Found user {} no salary defined {}".format(username,self.json_data['employies'][i]['salary']))
                            self.logger.debug("Found user {} no salary defined {}".format(username,self.json_data['employies'][i]['salary']))

        else:
            self.logger.debug("User {} not found ".format(username))
            print("User {} not found ".format(username))

        return new_salary


    def update_salary_all (self, percentage):
        high_salary = False
        if int(percentage) > 0:
            for idx in self.json_data['employies']:
                if self.json_data['employies'][idx]['salary']:
                    if self.json_data['employies'][idx]['salary'] is not None:
                        new_salary = int(self.json_data['employies'][idx]['salary'])
                        new_salary += new_salary * int(percentage)/100
                        self.json_data['employies'][idx]['salary'] =  new_salary
                        print("Found user {} Adding Salary, new Salry is {}".format(self.json_data['employies'][idx]['name'], self.json_data['employies'][idx]['salary']))
                        self.logger.debug("Found user {} Adding Salary, new Salry is {}".format(self.json_data['employies'][idx]['name'], self.json_data['employies'][idx]['salary']))
                    else:
                        print("Found user {} no salary defined {}".format(self.json_data['employies'][idx]['Name'],self.json_data['employies'][idx]['salary']))
                        self.logger.debug("Found user {} no salary defined {}".format(self.json_data['employies'][idx]['Name'],self.json_data['employies'][idx]['salary']))
        else:
            self.logger.debug("Increment is 0 nothing to do ")
            print("Increment is 0 nothing to do ")

        return self.json_data



    def employee_age(self, month):
        pension_emp = []
        now = datetime.datetime.now()
        for i in range(len(self.json_data['employies'])):
           if int(now.year) - int(self.son_data['employies'][i]['birthday']['year']) >= 67:
                pension_emp.append("self.son_data['employies'][i]['name']")
        return pension_emp



    def birthday_employees(self, month):
        bd_this_month = []
        for i in range(len(self.json_data['employies'])):
            if month == self.json_data['employies'][i]['birthday']['month']:
                    bd_this_month.append(self.json_data['employies'][i]['name'])
                    print("Found user {} is celebrating birthday this month".format(self.json_data['employies'][i]['name']))
                    self.logger.debug("Found user {} is celebrating birthday this month".format(self.json_data['employies'][i]['name']))
        return bd_this_month


    def add_programming_laguage (self, username, program):
        if username != "":
            for i in range(len(self.json_data['employies'])):
                if username == self.json_data['employies'][i]['name']:
                    self.json_data['employies'][i]['programs'].append(program)
                    print("Found user {} adding programming language, new programs list is ".format(username, self.json_data['employies'][i]['programs']))
                    self.logger.debug("Found user {} adding programming language, new programs list is ".format(username,self.json_data['employies'][i]['programs']))
        else:
            self.logger.debug("Username is empty - nothing to do {}".format(username))
            print("Username is empty - nothing to do {}".format(username))
        return  self.json_data


    def delete_db(self):
        self.json_data.clear()
        self.write_to_json_file(self.global_db_path)

        return self.json_data


    def load_new_db(self, newJSONPath):
        self.json_data.clear()
        self.global_db_path = newJSONPath
        json_content = self.get_json_data_from_file(self.global_db_path)
        self.json_data = json.loads(json_content)
        return self.json_data
