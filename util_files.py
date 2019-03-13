import os
import json


def does_file_exist(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False


def write_file(file_path, data):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)


def write_new_file(file_path, data):
    with open(file_path, 'w+') as outfile:
        json.dump(data, outfile)


def read_json_file(file_path):
    with open(file_path, 'r') as show_file:
        data_str = show_file.read()
        old_show_data = json.loads(data_str)
        return old_show_data


def get_show_file_path(title, year):
    if os.path.isdir(os.path.join(os.getcwd(), 'shows')):
        file_path = os.path.join(os.getcwd(), 'shows', (title + '_' + year + '.json'))
    else:
        os.mkdir(os.path.join(os.getcwd(), 'shows'))
        file_path = os.path.join(os.getcwd(), 'shows', (title + '_' + year + '.json'))

    return file_path


def get_show_file_path_for_upload(title, year):
    if os.path.isdir(os.path.join(os.getcwd(), 'shows_to_upload')):
        file_path = os.path.join(os.getcwd(), 'shows_to_upload', (title + '_' + year + '.json'))
    else:
        os.mkdir(os.path.join(os.getcwd(), 'shows_to_upload'))
        file_path = os.path.join(os.getcwd(), 'shows_to_upload', (title + '_' + year + '.json'))

    return file_path
