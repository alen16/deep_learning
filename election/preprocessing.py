import os
import json


def read_json_file(file_path):
    data = []
    dir = os.listdir(file_path)
    for file in dir:
        path = os.path.join(file_path, file)
        with open(path) as f:
            test = json.loads(f.readline())

            print(test['title'])


    return data


if __name__ == "__main__":
    file_path = "../StepContent__nocontent_title_desc"
    read_json_file(file_path)