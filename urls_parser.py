import json


class Parser:
    def __init__(self):
        """
        This class is to get data from url file
        """
        pass

    def parse_file(self, f_name):
        """
        :return: res, dir_list_data_new, length_data_new
        """
        f = open(f_name, 'r')
        data_2 = f.read()
        f.close()
        data_2 = data_2.replace("'", '"')

        json_data = data_2[data_2.find('data:') + len("data:"):data_2.find('dir_list')]
        dir_list_data = data_2[data_2.find('dir_list:') + len("dir_list:"):data_2.find('length')]
        length_data = data_2[data_2.find('length:') + len("length:"):]
        res = json.loads(json_data)
        res = dict(res)

        dir_list_data = dir_list_data.replace('[', '')
        dir_list_data = dir_list_data.replace(']', '')
        dir_list_data = dir_list_data.replace('"', '')
        dir_list_data = dir_list_data.split(',')
        dir_list_data_new = []
        for i in dir_list_data:
            i = i.lstrip()
            dir_list_data_new.append(i)

        length_data = length_data.replace('[', '')
        length_data = length_data.replace(']', '')
        length_data = length_data.replace(',', '')
        length_data_new = []
        for i in length_data.split():
            length_data_new.append(int(i))

        return res, dir_list_data_new, length_data_new
