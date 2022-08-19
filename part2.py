import requests

import csv

import re

from urllib.parse import urljoin

from bs4 import BeautifulSoup

# fields = ['URL', 'Phone', 'Email', 'TT', 'TDD']  #this is an optional header record (labels) for the CSV output #commented out to enable appending

filename = "c:/scrape/myscrapeoutput.csv" #file name and location for the final output file of section 2



# ---- SECTION 1------



olddata=None #assigning a starting NULL value for the variable to check duplicates in the links within homepage that have 'contact' word

#OUTPUT FILE FOR PROGRAM 1 WHICH WILL BE USED AS INPUT FILE FOR PROGRAM 2

f = open("/Users/victoriapuck-karam/Documents/all_links.txt", "w") #file name and location for the interim output file of section 1



#read website from Websites.txt which is the Input for Section 1

with open('/Users/victoriapuck-karam/Documents/all_links.txt') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')

    line_count = 0

    for row in csv_reader:

        URL=row[0]

        #following 2 lines assign redirected URL to original URL

        result = requests.post(URL)

        URL = result.url #if a website gets redirected, this variable stores the redirected value

        ###

        grab = requests.get(URL)

        soup = BeautifulSoup(grab.text, 'html.parser')

        content ='contact' #string variable to identify “contact” on webpage



# writing the home page first into the file



        f.write(URL)

        f.write("\n")

# parse paragraphs from soup to search for any link with the word 'contact' in it

        for link in soup.find_all("a"):

            data = link.get('href') #stores contact link in the webpage

            if data != None: #discards links which dont have a value to prevent program from throwing an exception

                if content in data:

                    if 'http' in data: #checks if the URL is a full URL

                        if data != olddata: #checks if duplicate, if so skips. Else writes the link into file

                            f.write(data)

                            f.write("\n")

                            olddata=data #sets the value of the variable to the latest link with contact word in it for the next check for duplicate

                    else: #if URL is partial URL, it appends the main URL at the beginning

                        if data[0]=='/': #some partial URLs are not starting with / and hence need '/' to be added at beginning. This IF has / at the beginning

                            if (urljoin(URL,data)) != olddata: #checks if duplicate, if so skips. Also uses URL join so as to append contact link to homepage instead of current page

                                # the command urljoin helps append the real homepage to the partial link and not to the current page.

                                f.write(urljoin(URL,data))

                                f.write("\n")

                                olddata=urljoin(URL,data) #sets the value of the variable to the latest link with contact word in it for the next check for duplicate

                        else:

                            if (urljoin(URL,'/'+data)) != olddata: #first appends / and partial link to homepage, and then checks if duplicate, if so skips

                                f.write(urljoin(URL,'/'+data))

                                f.write("\n")

                                olddata=urljoin(URL,'/'+data) #sets the value of the variable to the latest link with contact word in it for the next check for duplicate



    f.close() #closes file after all contact links are written to file



# ----- SECTION 2---------



phone2 = '' #initializing second phone variable

with open(filename, 'a',newline='') as csvfile:

    csvwriter = csv.writer(csvfile)



    # writing the fields as header # commented out to enable appending

    # csvwriter.writerow(fields) # commented out to enable appending



    with open('c/Users/victoriapuck-karam/Documents/all_links.txt') as csv_file: # loop through links in the file generated during Section 1

        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0

        for row in csv_reader:

            URL=row[0]





            page = requests.get(URL)

            source = str(page.content)

            soup = BeautifulSoup(page.content, 'html.parser')



            #get Phone2 and Mainphone. If mainphone is not available, choose Phone2

            form= getForm1(source)
            phone = getPhone2(source)

            mainphone = getPhone(str(soup))

            if mainphone == '':

                mainphone = phone



            #get Email in 5 different ways - Email, Email2, Email3, Email4, Email5

            email= getEmail(str(soup))

            # additional lines added for additional email searches

            email2 = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', str(soup)) # identify email with @

            email3 = re.findall('mailto:',str(soup)) # identify email with ‘mailto’

            if email3:

                email3='Email Available'

            if (str(soup).find('mailto:+') == -1):

                email4 = ''

            else:

                email4 = 'Email Available'

            email5 =''

            for link in soup.find_all("a"):

                data = link.get('href') #data is a variable that stores contact link in the webpage

                if 'email' in str(data):

                    email5= 'Email Available'



            #finalize email to be the first available email

            if not email:

                email=email2

            if not email:

                email=email3

            if not email:

                email=email4

            if not email:

                email=email5



            #search the string for strings "TT " or "TYY"

            if ((str(soup).find("TT ") == -1) and (str(soup).find("/TYY") == -1)) : #no match for either string TT anbd TYY

                TT = 'Not Available'

            else:

                TT = 'Available'



            #search the string for strings "TT " or "TYY"

            if ((str(soup).find("TDD ") == -1) and (str(soup).find("TDD/") == -1)) : #no match for either string TDD anbd TDD/

                TDD = 'Not Available'

            else:

                TDD = 'Available'

            if (form != ''):
                formOutput= 'Available'
            else:
                formOutput= 'Not Available'

            rows = [[URL, mainphone, email, TT, TDD,formOutput]]



            #print(rows)





    # writing the data rows to the output file

            csvwriter.writerows(rows)
