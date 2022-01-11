from urls_extractor import Exractor
from downloader import Download
from urls_parser import Parser
from converter import Converter
import os

use_url_file = True  # if False then program will extract urls from website [took me 1 hour]
# else it will use my url file

user_id = "shashwatbansal247@gmail.com"
password = "Shashu@247"
time_to_wait = 1


def start_program():
    curr_dir = os.getcwd()

    if (use_url_file == False):
        e = Exractor(user_id=user_id, password=password, time_to_wait=time_to_wait)
        e.start()

    os.chdir(curr_dir)
    parser = Parser()
    if(use_url_file == False):
        urls, dir_list, length = parser.parse_file("urls.txt")
    else:
        urls, dir_list, length = parser.parse_file("urls_7.txt")
    try:
        os.mkdir('ineuron')
    except:
        pass
    os.chdir(os.getcwd() + "\\ineuron")
    driver = Download(urls, dir_list, length)
    driver.run_downloader()

    os.chdir(curr_dir)
    cv = Converter(curr_dir)
    cv.start()


if __name__ == '__main__':
    start_program()
