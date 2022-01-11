from selenium import webdriver
from selenium.webdriver.common.by import By
from google_drive_downloader import GoogleDriveDownloader as gdd
import os
import time
import shutil


class Exractor:
    def __init__(self, user_id, password, time_to_wait=1):

        """

        :param user_id: user id of ineuron
        :param password: password of ineuron
        :param time_to_wait: waiting time in seconds depends upon internet speed
        """
        self.user_id = user_id
        self.password = password
        self.time_to_wait = time_to_wait
        self.dict_to_use = {}
        self.urls = {}
        self.dir_list = []
        self.length = []

        # driver controls new chrome window
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()



    def sign_in(self):
        """
        this is to sign in ineuron
        :return: none
        """
        self.driver.get("https://ineuron.ai/")
        time.sleep(self.time_to_wait)

        self.driver.find_element(by=By.LINK_TEXT, value="Sign in").click()
        time.sleep(self.time_to_wait)

    def rem_frame(self):
        """
        This function is to remove pop up window
        :return: none
        """

        self.driver.switch_to.frame(5)
        self.driver.find_element(By.XPATH, 'html/body/div/div/div/div/div/i').click()
        self.driver.switch_to.default_content()

    def find_by_tag(self, tag, to_find_name=None, to_fill_data=None, show=False):
        """
        This function find the tag and their associated names
        :param tag: can be 'input' , 'button'
        :param to_find_name: can be a list of names ["Email Address","Enter Password"] or a name 'Sign In'
        :param to_fill_data: can be a list of data [user_id,password] or a data 'Password'
        :param show: This shows the accessible_name of current tag. True or False
        :return:  none
        """

        k = self.driver.find_elements(by=By.TAG_NAME, value=tag)
        # if to_find_name is a list then click on every item
        if type(to_find_name) == list:
            j = 0
            for i in k:
                if j < len(to_find_name) and i.accessible_name == to_find_name[j]:
                    while True:
                        try:
                            i.click()
                            # if there is fill data then fill the data
                            if to_fill_data:
                                i.send_keys(to_fill_data[j])
                            j = j + 1
                        except Exception as e:
                            self.rem_frame()
                        else:
                            break
        else:
            for i in k:
                if show:
                    print(i.accessible_name)
                    continue
                if i.accessible_name == to_find_name:
                    while True:
                        try:
                            i.click()
                            if to_fill_data:
                                i.send_keys(to_fill_data)
                        except Exception as e:
                            self.rem_frame()
                        else:
                            break

                elif i.text == to_find_name:
                    while True:
                        try:
                            i.click()
                            if to_fill_data:
                                i.send_keys(to_fill_data)
                        except Exception as e:
                            self.rem_frame()
                        else:
                            break

    def go_to_assignments(self):
        self.find_by_tag('input', ["Email Address", "Enter Password"], [self.user_id, self.password])

        self.find_by_tag('button', 'Sign In')
        time.sleep(self.time_to_wait)

        self.driver.get("https://learn.ineuron.ai/")
        time.sleep(self.time_to_wait)

        self.driver.find_element(By.CLASS_NAME, "Home_course-title__3tSE-").click()
        time.sleep(self.time_to_wait)

        self.find_by_tag('li', 'Assignments')
        time.sleep(self.time_to_wait)
        for k in self.driver.find_elements(By.CLASS_NAME, 'Assignments_title__xGAqZ'):
            self.dir_list.append(k.text)

        assignments = self.driver.find_elements(By.CLASS_NAME, 'Assignments_classes__2tC8z.Global_grid__2KDqG')

        for assignment in assignments:
            self.length.append(len(assignment.find_elements(By.CLASS_NAME, 'Assignments_class-title__PwgJi')))

    def download(self):
        """
        :return: name of file and url
        """
        time.sleep(self.time_to_wait)
        name = self.driver.find_element(By.CLASS_NAME, "UploadAssignment_info__V5TWV").text
        j = self.driver.find_element(By.CLASS_NAME, "UploadAssignment_assignment-file__1bReg")
        k = j.find_element(By.TAG_NAME, 'a')
        k.click()

        self.driver.switch_to.window(self.driver.window_handles[1])

        url = self.driver.current_url
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        self.driver.find_element(By.CLASS_NAME, "fas.fa-times").click()
        return name, url

    def start(self):
        """
        This function starts the url extracting process
        :return: none
        """
        self.sign_in()
        self.go_to_assignments()
        curr_dir = os.getcwd()
        try:
            os.mkdir('ineuron')
            os.chdir(os.getcwd() + '\\ineuron')
            T_length = len(self.driver.find_elements(By.CLASS_NAME, 'Assignments_class-card__1YQQg'))
            for k in self.dir_list:
                os.mkdir(k)

            i = 0
            while i < T_length:
                while True:
                    try:
                        self.driver.find_elements(By.CLASS_NAME, 'Assignments_class-card__1YQQg')[i].click()
                        name, url = self.download()
                        self.urls[str(i + 1) + '\\' + name] = url
                        i = i + 1
                    except Exception as e:
                        pass
                    else:
                        break

        except Exception as e:
            print(e)
            os.chdir(curr_dir)
            location = os.getcwd()
            direc = "ineuron"
            path = os.path.join(location, direc)
            shutil.rmtree(path)
            time.sleep(self.time_to_wait)
        os.chdir(curr_dir)
        f = open("urls.txt", 'w+')
        f.write("data:" + str(self.urls))
        f.write("dir_list:" + str(self.dir_list))
        f.write("length:" + str(self.length))
        f.close()



