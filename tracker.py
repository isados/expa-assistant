import time
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from country import *

def submit_tracker(person):
    choice = input('\nDo you want to post to the tracker as well? (y/n) : ').lower().strip()
    if choice != 'y': return
    try:
        #Pre-Enter Gender; Male is 0th element
        gender = ''
        while(gender != 'm' and gender != 'f'):
            gender = input(f"\nEnter {person['Name']}'s Gender(m/f):").lower().strip()

        #Open form
        sheet = webdriver.Chrome(os.getcwd()+"/chromedriver")  # Optional argument, if not specified will search path.
        sheet.implicitly_wait(40) # seconds
        sheet.get('https://goo.gl/forms/CsgDOUWQ6hPWXOCg1');

        #Enter Name
        sheet.find_element_by_name('entry.165305955').send_keys(person['Name'])

        #Enter Email
        sheet.find_element_by_name('entry.1521697799').send_keys(person['Email'])

        toggle_buttons = sheet.find_elements_by_class_name('docssharedWizToggleLabeledLabelText')

        #Enter Gender
        if gender == 'm' : toggle_buttons[0].click()
        else : toggle_buttons[1].click()

        #Enter Job Titles
        from job_des import click_job_desc_elements
        click_job_desc_elements(toggle_buttons[2:], person['Job_Description'])


        #Enter OPP link
        sheet.find_element_by_name('entry.169150500').send_keys(person['Opp_Link'].split('/')[-1])

        #Enter Home_LC
        sheet.find_element_by_name('entry.785093106').send_keys(person['Home_LC'])

        #Enter Country
        ## Check entered country
        while person['Country'] not in COUNTRY_NAMES_LIST:
            person['Country'] = input("Enter the right country name : ").strip()

        ##Click the dropdown_bar and Enter Country
        dropdown = sheet.find_element_by_class_name('quantumWizMenuPaperselectOptionList')
        dropdown.click()

        country_elements = sheet.find_elements_by_class_name("quantumWizMenuPaperselectOption")
        for country_elem in country_elements:
            if country_elem.get_attribute('data-value') == person['Country']:
                ActionChains(sheet).send_keys(person['Country']).perform()
                ActionChains(sheet).send_keys(Keys.ENTER).perform()

        # Enter Phone_Number with country code
        try:
            while '+' in person['Phone_Number']:
                print('\nWARNING : Country Code Detected...\n')
                person['Phone_Number'] = input('\nEnter Right Phone Number :')

            int(person['Phone_Number'].replace(' ',''))
            phone_num = "+{} {}".format(int_calling_code(person['Country']), person['Phone_Number'])
            sheet.find_element_by_name("entry.268692577").send_keys(phone_num)
        except ValueError:
            pass

        # Enter EPM's details
        if len(person['EPM']) != 0:
            #Enter EPM Name
            sheet.find_element_by_name("entry.1782220731").send_keys(person['EPM'][0][0])
            #Enter EPM Email
            sheet.find_element_by_name("entry.980941299").send_keys(person['EPM'][0][1])
        else:
            print('\nNo EPM Details are mentioned... Contact LC!')
            choice = input('Would you like to send an email to the LC now? (y/n):').strip().lower()
            if choice == 'y':
                #send email
                epm_name  = input("Contact's Name:")
                epm_email = input("Contact's Email:")
                # Call mailer and pass this (Name, Email, EP_Name, Home_LC)
            else:
                print(f"\n######Follow up with {person['Name']}'s LC'##############\n")

        # Submit Form
        choice = input('\nAre you absolutely sure you want to post this? (y/n):').lower().strip()
        if choice == 'y':
            sheet.find_element_by_class_name('quantumWizButtonPaperbuttonLabel').click()
            time.sleep(1)
        else:
            print("Oh well.. we'll try the next one\n")

        """'Name' : "entry.165305955"
        'Email' : "entry.1521697799"
        'Phone_Number': add_country_code("entry.268692577")
        'Job_Description' : 'entry.169150500'
        'Home_LC': "entry.785093106"
        'epm_name': "entry.1782220731"
        'epm_email': "entry.980941299"
        'opp_name':
    """
    except KeyboardInterrupt:
        print('\nOops, escape key was pressed.. not going to post details of this applicant\n')
    finally:
        try:
            sheet.quit()
        except Exception as e:
            print('Error :',e)

#Main Code
if __name__ == '__main__':
    person = {
    'Name' : 'Dina Mostafa',
    'Job_Description' : ['Graphic Designer'],
    'Home_LC' : 'AAST Alexandria',
    'Phone_Number' :  '011117777' ,
    'Email' : 'p_6492a6d77b327ca9f72dbb1ac410b59e4b7f24cd@inbound.aiesec.org',
    'Country' : 'Egypt',
    'EPM' : [('Ahmed Asser Wahdan', 'p_8fce094d509d0e58323d219d29075ddadd8c77ae@inbound.aiesec.org'), ('Mohamed saadeldin', 'mohamed.saadeldin@aiesec.net')],
    # 'EPM' : [],
    'Opp_Link' : 'https://aiesec.org/opportunity/1105333'}

    submit_tracker(person)
