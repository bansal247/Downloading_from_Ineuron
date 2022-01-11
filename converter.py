import os
import json
from docx import Document


class Converter:
    def __init__(self, curr_dir):
        self.curr_dir = curr_dir
        os.chdir(curr_dir + "\\ineuron")
        self.dir_list = os.listdir()

    def edit(self, z):
        curr_dir = os.getcwd()
        doc = Document('Assignment_{}.docx'.format(z))
        text = []
        for i in doc.paragraphs:
            if len(i.text) > 0:
                text.append(i.text)

        os.chdir(self.curr_dir)
        f1 = open('demo.ipynb', 'r')
        f1.seek(0)
        d = f1.read()
        d = d.replace('null', 'None')
        data_2 = eval(d)

        j = 0
        for i in data_2['cells']:
            if i['cell_type'] == 'markdown' and len(text) > j:
                i['source'] = text[j]
                j = j + 1

        d2 = json.dumps(data_2, indent=1)
        os.chdir(curr_dir)
        f = open('Assignment_{}.ipynb'.format(z), 'w+')
        f.write(d2)
        f.close()

    def make_ipynb(self, folder):
        curr_dir = os.getcwd()
        os.chdir(folder)
        files_list = os.listdir()
        for i in files_list:
            try:
                num = int(i[i.find('_') + 1:i.find('.')])
                print(os.getcwd())
                self.edit(num)
            except Exception as e:
                print(e)

    def start(self):
        for i in self.dir_list:
            if i.find('.') > -1:
                continue
            else:
                curr_dir = os.getcwd()
                self.make_ipynb(curr_dir + "\\" + i)
                os.chdir(curr_dir)
