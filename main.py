from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
from time import sleep

if __name__ == '__main__':

    # get current time
    now = datetime.now()
    # get current day name (eg. Monday, Tuesday, ...)
    current_day = now.strftime("%A")

    # read classes.txt for day names
    with open('classes.txt') as f:
        lines = f.readlines()
        for line in lines:
            line.strip()
            if current_day in line:
                # if current day name matches first token in a line then there is lecture today
                start_hour_string = line.split(' ')[1].strip()
                break
        else:
            # will execute if for loop never reaches break statement
            # which means there is no lecture today
            print('no lecture today')
            input('Press Enter to exit...')
            exit()
    # if there is lecture today check for deltatime until the lecture start
    start_time = datetime.strptime(f'{datetime.now().strftime("%d/%m/%y")} {start_hour_string}', '%d/%m/%y %H:%M:%S')
    # if lecture has not started yet, sleep until it starts
    if start_time > now:
        print(f'sleeping until {start_hour_string}')
        sleep((start_time-now).total_seconds())

    # init driver
    dr = webdriver.Firefox()
    # implicit wait forces driver to wait if it can not find an element
    dr.implicitly_wait(10)
    # wait object is going to use for explicit wait commands
    wait = WebDriverWait(dr, 10)
    # get function makes a request to the url
    dr.get('https://online.yildiz.edu.tr')
    # current handle is going to be used later to change tabs
    original_window = dr.current_window_handle

    try:
        print('1')
        # try to find textbox for mail query
        textbox_mail = wait.until(
            EC.presence_of_element_located((By.ID, 'Data_Mail'))
        )
        print('2')
        # try to find textbox for password query
        textbox_password = wait.until(
            EC.presence_of_element_located((By.ID, 'Data_Password'))
        )
        print('3')
        # try to find button for login
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/div/div/div/div/div/form/div[3]/div[2]/button'))
        )
        print('4')
        # fill in the mail
        textbox_mail.send_keys('bahadir.can@std.yildiz.edu.tr')
        print('5')
        # fill in the password
        textbox_password.send_keys('Bn7r6yPa?7')
        print('6')
        # click login
        login_button.click()
        
        # the welcome page includes a timeline element
        # which includes timeline-row elements for each upcoming lessons
        # however timeline-row elements are not clickable since timeline element overlaps them
        lecture_button = dr.find_element(By.CLASS_NAME, 'timeline-row')
        print('7')
        # thus the driver clicks timeline-content elements
        lecture_button.find_element(By.CLASS_NAME, 'timeline-content').click()
        print('8')
        # now it tries to find `derse katil` button
        # here it is not possible to find the button using classname or tagname or id
        # hence we use the xpath of the button since the view is not going to change in any other occurances
        dr.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[7]/div/div/div/div/div/table/tbody/tr/td[5]/a').click()
        print('9')
        # once we click the button the link is going to be opened in a new tab
        # so we need to change tabs
        # first we need to wait until there are two windows
        wait.until(EC.number_of_windows_to_be(2))
        # we iterate over the window_handles and find the first one that does not match the initial window
        for window_handle in dr.window_handles:
        # here the original_window variable comes into play
            if window_handle != original_window:
                dr.switch_to.window(window_handle)
                break
        # it takes a while to load the second window so we wait until the title bar changes
        # the title bar change can be acquired using a check to see if it includes 'Zoom'
        wait.until(EC.title_contains('Zoom'))
        # the alert that comes up to allow the driver to launch Zoom app can not be accepted using selenium
        # because the alert is an OS level alert
        # accepting the alert can be achieved using other packages (eg. pyAutoGui)
        # but using such libraries makes the app not usable headless
        # (being headless meaning the window needs to be seen on top of the screen at all times)
        current_url = dr.current_url
        # so we modify the current url to launch the zoom app on the browser
        new_url = current_url.replace('w/', 'wc/join/')
        dr.get(new_url)
        print('10')
        # when zoom launches on the browser we now need to fill in the username and then join the call
        # in my case my name was already filled in automatically by the OS preferences
        # if a change is required it can be achieved with following steps
        # find the text box using driver.find_element()
        # type your name using element.send_keys()
        # then resume the program as is
        join_button = wait.until(EC.element_to_be_clickable((By.ID, 'joinBtn')))
        join_button.click()
        # These were forgotten to be removed during debugging you can ignore following 3 lines
        # alert = wait.until(
        #     EC.alert_is_present()
        # )
    except Exception as e:
        # if any error occures while the program is running
        # it is going to be caught in these lines
        # printed on the screen then exit the program
        print(e)
        input('Press Enter to exit...')
        dr.quit()
        exit()
    else:
        pass

    # if the lecture fires up with no problem the program is going to be halted
    input('Press Enter to exit...')
    dr.quit()
    exit()
    # debug numbers can be used to locate wherever the error occured