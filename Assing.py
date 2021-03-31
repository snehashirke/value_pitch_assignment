import requests
from bs4 import BeautifulSoup
import csv


outputFile = open('case_details_output.csv', 'w', newline ='') 
with outputFile:     
    write = csv.writer(outputFile) 
    write.writerow(["DIARY NUMBER", 'CASE NUMBER','PETITION', "RESPONDENT"])





for caseYear in range(2001, 2022):
    for diaryNumber in range(1,101):
        try:
            print(caseYear)
            print(diaryNumber)

            
            captcha_url = "https://main.sci.gov.in/php/captcha_num.php"

            session = requests.session()
            captcha_response = session.post(captcha_url)

            captcha_beautiful_soup = BeautifulSoup(captcha_response.content, "html.parser")
            print(captcha_beautiful_soup.text)


            formFillingData ={
            "d_no" : diaryNumber,
            "d_yr" : caseYear,
            "ansCaptcha" : "",
            }
            formFillingData['ansCaptcha'] = captcha_beautiful_soup.text.strip()
            print(formFillingData)


            mainUrl= "https://main.sci.gov.in/php/case_status/case_status_process.php"


            header_dictionary = {
                "Host" : "main.sci.gov.in", 
                "Origin" : "https://main.sci.gov.in",
                "Referer" : "https://main.sci.gov.in/case-status", 
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
                }
            data_list=[]        
            main_url_response = session.post(mainUrl, headers= header_dictionary ,data = formFillingData)

            main_url_data = BeautifulSoup(main_url_response.text, "html.parser")

            main_table = main_url_data.find('div',{'id':"collapse1"}).find('table')

            # diary_no_row = main_table.findAll('tr')[0]
            # diary_no = diary_no_row.findAll('td')[1].text
            # data_list.append(diary_no)
            # print(diary_no)

            # case_row = main_table.findAll('tr')[1]
            # case_no = case_row.findAll('td')[1].text
            # data_list.append(case_no)
            # print(case_no)

            # petitioners_row = main_table.findAll('tr')[2]
            # petitioners = petitioners_row.findAll('td')[1].text
            # data_list.append(petitioners)
            # print(petitioners)


            # status_row = main_table.findAll('tr')[3]
            # status = status_row.findAll('td')[1].text
            # data_list.append(status)
            # print(status)

            diary_number = ""
            case_num = ""
            petitioner = ""    
            respondent = ""
                    
            for single_row in main_table.findAll('tr'):
                heading = single_row.findAll('td')[0].text.strip()
                if heading == "Diary No.":
                    diary_number = single_row.findAll('td')[1].text.strip()

                if heading == "Case No.":
                    case_num = single_row.findAll('td')[1].text.strip()

                if heading == "Petitioner(s)":
                    petitioner = single_row.findAll('td')[1].text.strip()
                    
                if heading == "Respondent(s)":
                    respondent = single_row.findAll('td')[1].text.strip()
                    

            data_list.append(diaryNumber)
            data_list.append(case_num)
            data_list.append(petitioner)
            data_list.append(respondent)

            print(data_list)
            outputFile = open('case_details_output.csv', 'a', newline ='') 
            with outputFile:     
                write = csv.writer(outputFile) 
                write.writerow(data_list)
        except :
            print("Skipping Error occured ")




