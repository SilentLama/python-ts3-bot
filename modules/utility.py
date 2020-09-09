import json

#region util

def save_to_txt(filename, data):
    with open(f"{filename}", "a+") as data_file:
        if type(data) == str:
            data_file.write(data + "\n")
        else:
            json.dump(data, data_file, indent=4)

        

def wipe_json_file(filename):
    with open(f"{filename}", "w") as data_file:
        data_file.truncate(0)


def read_from_json(filename):
    ''' returns a list line by line '''
    with  open(f"{filename}", "r") as data_file:
        data = data_file.readlines()
        return data 


def parse_json(response):
    json_response = json.loads(response.text)
    return json_response

#endregion