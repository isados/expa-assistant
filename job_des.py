#Example list
# job_descs = ["Digital Marketing - SmartNakheel","Digital","Graphics Designer - The Lightbulb Project","Business Analyst in Bahrain - Feeh La","Photography",'manager']

# Accepts a list of job titles that a single applicant has applied for
# and picks those titles on the sheet

def click_job_desc_elements(elements, job_descs:list):
    job_keywords = [
    "web", "app",
    "business" ,"talent" ,
    "finance", "digital" ,"graphic" ,"photo" ,
    "sales", "account",
    "other"
    ]
    list_of_elements = []
    for job_title in job_descs:
        for index, keyword in enumerate(job_keywords):
            if keyword in job_title.lower():
                list_of_elements.append(index)
                break
            if keyword == 'other':
                list_of_elements.append(index)
    for index in set(list_of_elements):
        elements[index].click()
