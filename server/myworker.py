import json
#import TargilSicum.Logger
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
        if not json_file_path:
            json_file_path = self.global_db_path

        json_from_dict = json.dumps(self.json_data,indent=4)
        try:
            with open(json_file_path, 'w') as out_file:
                out_file.write(json_from_dict)
                out_file.close()
        except IOError as error:
            self.logger.debug("Exception: content {}".format(error))



    def get_json_data_from_file(self, json_file_path):
        try:
            with open(json_file_path, 'r') as in_file:
                json_content = in_file.read().translate('UTF-8')
                in_file.close()
        except IOError as error:
            self.logger.debug("Exception: content {}".format(error))
        return json_content


    def check_if_user_exists(self, username):
        obj = self.json_data['employies']

        if username in obj:
            self.logger.debug("User exists - not adding the new user {}".format(username))
            return True
        return False


    def check_num_of_employees(self):
        return len(self.json_data['employies'])


    def add_employee(self, json_obj):
        # Suggested "fix"
        # if self.check_num_of_employees() >=10:
        #     return  False

        for entry in json_obj['employies']:
            for field in json_obj['employies'][entry]:
                if not any(field):
                    self.logger.debug("Failed Adding new user one of the values is empty: " + str(json_obj))
                    break;
            if not self.check_if_user_exists(json_obj['employies'][entry]['name']):
                if self.json_data['employies'].update(json_obj['employies']) is None:
                    self.write_to_json_file (json_file_path="")
                    self.logger.debug("Adding user {} to DB".format(json_obj['employies'][entry]))

                    return True
            else:
                self.logger.debug("Failed Adding user {} values already exists".format(json_obj['employies'][entry]))

        return False



    def remove_employee (self, username):

        if username != "":
            obj = self.json_data['employies']
            if username in obj:
                    del self.json_data['employies'][username]
                    self.logger.debug("Found user {} removing user".format(username))
                    self.write_to_json_file(json_file_path="")
                    return True
            else:
                self.logger.debug("User {} not found".format(username))
                return False
        else:
            self.logger.debug("Failed removing user - values is empty {}".format(username))
            return False


    def update_salary (self, destEmpt, increment):

        if destEmpt != "":
            for username in (self.json_data['employies']):
                        if username == destEmpt and self.json_data['employies'][username]['salary'] is not None:
                            new_salary = int(self.json_data['employies'][username]['salary']) + int(increment)
                            self.json_data['employies'][username]['salary'] = str(new_salary)
                            self.write_to_json_file(json_file_path="")
                        else:
                            self.logger.debug("Found user {} no salary defined {}".format(username,self.json_data['employies'][username]['salary']))
                            return None
        else:
            self.logger.debug("User {} not found ".format(destEmpt))
            return None

        return self.json_data


    def update_salary_all (self, percentage):
        if int(percentage) > 0:
            for username in self.json_data['employies']:
                if self.json_data['employies'][username]['salary']:
                    if self.json_data['employies'][username]['salary'] is not None:
                        new_salary = int(self.json_data['employies'][username]['salary'])
                        new_salary += new_salary * int(percentage)/100
                        self.json_data['employies'][username]['salary'] = new_salary
                        self.write_to_json_file(json_file_path="")
                        self.logger.debug("Found user {} Adding Salary, new Salry is {}".format(self.json_data['employies'][username]['name'], self.json_data['employies'][username]['salary']))
                    else:
                        self.logger.debug("Found user {} no salary defined {}".format(self.json_data['employies'][username]['Name'],self.json_data['employies'][username]['salary']))
        else:
            self.logger.debug("Increment is 0 nothing to do ")


        return self.json_data



    def birthday_employees(self, month):
        bd_this_month = dict()
        for name in self.json_data['employies']:
            if int(month) == self.json_data['employies'][name]['birthday']['month']:
                    bd_this_month[name] = self.json_data['employies'][name]
                    self.logger.debug("Found user {} is celebrating birthday this month".format(self.json_data['employies'][name]['name']))
        return bd_this_month


    def add_programming_laguage (self, username, program):
        if username and program:
            for name in self.json_data['employies']:
                if name == username:
                    self.json_data['employies'][name]['programs'].append(program)
                    self.logger.debug("Found user {} adding programming language, new programs list is ".format(username,self.json_data['employies'][name]['programs']))
                    self.write_to_json_file(json_file_path="")

        else:
            self.logger.debug("Username is empty - nothing to do {}".format(username))
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
