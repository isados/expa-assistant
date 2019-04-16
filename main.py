import time
from selenium import webdriver

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys

import os
import clipboard

from tracker import *
from login_details import *
from mymail import send_mail

def play_welcome_message():
    print("{:#^49}".format(' Welcome to the EXPA Platform Assistant Tool '))
    print("{:#^49}\n".format(' Developed by Isa AlDoseri '))

    if not os.path.exists(secret_file):
        choice = input("""This seems to be your first time :D
That's alright, we just need to setup your login details before we begin.

They will be stored safely in a file called 'secret.txt'
where your passwords will be encrypted using the Vigenere cipher
(the most powerful of the ancient ciphers)

Note: If you wish to change these details later on, you could either:
1) Open the file yourself and amend it.
2) Delete the file to get this welcome message again (Highly Recommended!)

Ready to begin? (y)es / (n)o :""")
        if choice.strip().lower() == 'y':
            details = {}
            print('\nEnter your email login details...')
            details['name'] = input('Enter your name as it should it appear in your email header: ')
            details['email'] = input('Enter your email ID: ')
            details['email_pwd'] = getpass(prompt = "Enter your password: ")

            print('\nNow for your EXPA login details...')
            details['expa_username'] = input('Enter your EXPA ID: ')
            details['expa_pwd'] = getpass(prompt = 'Enter your password: ')

            key = input('\nNow enter a PASSCODE: ')
            create_login_file(details, key)
        else:
            print('\nGoodbye then!')
            exit()

def hover(browser, xpath):
    element_to_hover_over = browser.find_element_by_xpath(xpath)
    hover = ActionChains(browser).move_to_element(element_to_hover_over)
    hover.perform()

def extract_epm_details(browser, info, path):
    info['EPM'] = []
    elems = browser.find_elements_by_xpath(path+'/*')

    #Check for no EPM manager's text
    try:
        temp = browser.find_element_by_css_selector('p.no-managers-text')

        if temp.text == 'This EP has no managers yet.':
            print = temp.text
            return info
    except:
        pass


    # Find 2nd paragraph element
    p = browser.find_element_by_xpath(path+'/p[2]')

    #Check for missing EPM manager text
    for e in elems[1:]:
        if e != p:
            # Extract name
            epm_name = e.find_element_by_class_name('application-managers-name').text

            #Copy the email to clipboard
            e.find_element_by_css_selector('i.cm.cm-copy').click()
            e.find_element_by_css_selector('i.cm.cm-copy').click()
            epm_email = clipboard.paste()

            info['EPM'].append((epm_name,epm_email))
        else:
            return info
    return info

def send_ep_welcome_email(receiver:dict, name_of_sender:str, sender_email:str, sender_pwd:str):
    # Format name
    # send_ep_welcome_email(name, to, cc, bcc, subject, name_of_sender, sender_email, sender_pwd)

    name = receiver['Name'].split()[0] #First Name
    name = name[0].upper() + name[1:] #Captilize the first letter
    to = [receiver['Email']]
    cc = [mail for name, mail in receiver['EPM']]
    bcc = []
    bcc_entry = ''
    while(1):
        print('\nDo you want to send a welcome email to this EP?')
        print(f"""Name: '{name}'
To: {to[0]}
CC: {cc}
{bcc_entry}""")
        choice = input("Yes(y), Change Name(c), Add BCC(b), No(n) :").lower().strip()
        if choice == 'y':
            send_mail(name, to, cc, bcc, name_of_sender, sender_email, sender_pwd)
            return
        elif choice == 'c':
            name = input('Enter Name :')
            continue
        elif choice == 'b':
            bcc = input("Please enter BCC receivers separated by commas and no spaces :").replace(' ','').split(',')
            if bcc != ['']: bcc_entry = 'BCC: ' + str(bcc) + '\n'
            else: bcc = []; bcc_entry = ''
        else:
            print('Email not sent!')
            return




if __name__ == '__main__':
    play_welcome_message()
    login_details = verify_passcode_get_details()

    num_of_applicants = 5
    try:
        num_of_applicants = int(input(f'How many applicants would you like to process? (Default is {num_of_applicants}) :').strip())
    except ValueError:
        print('Invalid value entered, going with default instead.')
    print()

    driver = webdriver.Chrome(os.getcwd()+"/chromedriver")  # Optional argument, if not specified will search path.
    # binary = FirefoxBinary('/usr/bin/firefox')
    # caps = DesiredCapabilities().FIREFOX
    # driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.getcwd()+"/geckodriver")
    driver.get('https://expa.aiesec.org');

    driver.implicitly_wait(60) # seconds

    #Login to the EXPA platform
    email = driver.find_element_by_name('user[email]')
    pwd = driver.find_element_by_name('user[password]')
    email.send_keys(login_details['expa_username'])
    pwd.send_keys(login_details['expa_pwd'])
    # pwd.submit()
    driver.find_element_by_class_name('login-btn').click()




    #Open Applications
    driver.get('https://expa.aiesec.org/applications');

    #Establish alias
    get_element = driver.find_element_by_xpath
    get_elements = driver.find_elements_by_xpath

    try:
        #Display additional fields
        field_elements = {"dropdown_bar":"//div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div/span/span/i",
                    "home_lc":"//div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div[2]/div/div[14]/label/div[2]",
                    'ph_no':  "//div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div[2]/div/div[15]/label/div[2]"}
        field_elements = list(field_elements.values())
        for element in field_elements:
            get_element(element).click()



        elem_location = {  'Name':"div[2]/p",
                    'Job_Description':'div[4]/span[2]',
                    'Home_LC':'div[8]/p',
                    'Phone_Number': 'div[9]/p',
                    'Email' : 'div[3]/div[2]/i'
                    }
        popup_elements = {

        }

        persons=[]
        for row in range(1, num_of_applicants + 1):

            try:
                # driver.implicitly_wait(1) # seconds
                element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, f"//div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/div[3]/div[1]/div[{row}]/div/{elem_location['Name']}")))
            except:
                #Scroll down the page
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                scrolling_panel = driver.find_element_by_id('applications-list').find_element_by_xpath('div')
                TouchActions(driver).scroll_from_element(scrolling_panel, 0, 1000).perform()

            #Check for duplicate entry, and just append the Job title
            ep_name = get_element(f"//div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/div[3]/div[1]/div[{row}]/div/{elem_location['Name']}").text
            # if 'Bob' not in ep_name: continue
            job_des = get_element(f"//div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/div[3]/div[1]/div[{row}]/div/{elem_location['Job_Description']}").text
            list_of_appended_applicants_so_far = {p['Name']:index for index, p in enumerate(persons)}

            if ep_name in list_of_appended_applicants_so_far:
                index = list_of_appended_applicants_so_far[ep_name]
                persons[index]['Job_Description'].append(job_des)
                continue

            # If no duplicate entry then proceed...
            persons.append({})
            for elem in tuple(elem_location):
                xpath_str = f"//div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/div[3]/div[1]/div[{row}]/div/{elem_location[elem]}"
                field = get_element(xpath_str)
                if elem is 'Email':
                    get_element(xpath_str).click()
                    get_element(xpath_str).click()
                    persons[-1][elem] = clipboard.paste()
                elif elem is 'Job_Description':
                    persons[-1][elem] = [field.text]
                else: persons[-1][elem] = field.text

            # Open popup window for a person, just click on their name
            xpath_str = f"//div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/div[3]/div[1]/div[{row}]/div/{elem_location['Name']}"
            get_element(xpath_str).click()

            #Get Country
            xpath_str = '//div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/div[1]/div[1]/div[2]/div[2]'
            persons[-1]['Country'] = get_element(xpath_str).text

            #Get EPM details
            hover(driver,'//div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/img')

            ## EPM & OppM Elements
            persons[-1] = extract_epm_details(driver,persons[-1],'//div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div/div[2]')

            # Opp link
            persons[-1]['Opp_Link'] = get_element('//div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div[1]/a').get_attribute('href')

            # Close the popup
            get_element('//div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[3]/div/div/div[1]/i').click()



        #Print to screen the corrected object
        for p in persons[::-1]:
            for key in tuple(p):
                print('{} : {}'.format(key,p[key]))
            choice = input('\nDo you want to process this applicant or move on? (y/n):').lower().strip()
            if choice == 'y':
                send_ep_welcome_email(p, login_details['name'], login_details['email'], login_details['email_pwd'])
                submit_tracker(p)
            print()

        time.sleep(5) # Let the user actually see something!
    finally:
        driver.quit()



"""
Call with Bob
Ishmael interview him 3 weeks... take snapshots for the conversation
mohith for akalati ... have to contact his LC
june1 to july 15 1st batch boys
Talk to Sarin about Dinesh

july 15th girls
Apurva Muthe call tomorrow
Website content manager add JD, check out Sarin's candidate

27th 23:40
Layka
delmonbn@batelco.com.bh

2nd may :9:20
"""
