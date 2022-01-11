import os
import gdown


class Download:
    def __init__(self, urls, dir_list, length):
        self.urls = urls
        self.dir_list = dir_list
        self.length = length

    def run_downloader(self):
        n = 0
        m = 0
        i = 0
        l = 0
        curr_dir = os.getcwd()
        while True:
            try:
                os.chdir(curr_dir + '\\' + self.dir_list[m])
            except:
                os.mkdir(self.dir_list[m])
            else:
                break
        for k, v in self.urls.items():

            name = 'Assignment_{}'.format(l + 1)
            output = '{}.docx'.format(name)
            url = v
            try:
                url = url.replace('/file/d/', '/uc?id=')
                url = url.replace('/view', '')
                gdown.download(url, output, quiet=False)
            except Exception as e:
                pass

            n = n + 1
            l = l + 1
            if self.length[i] == l:
                i = i + 1
                m = m + 1
                os.chdir(curr_dir)
                l = 0
                while True:
                    try:
                        os.chdir(curr_dir + '\\' + self.dir_list[m])
                    except:
                        try:
                            os.mkdir(self.dir_list[m])
                        except:
                            pass
                    else:
                        break
