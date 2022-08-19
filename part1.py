phone2 = '' #initializing second phone variable

with open(filename, 'a',newline='') as csvfile:

    csvwriter = csv.writer(csvfile)



    # writing the fields as header # commented out to enable appending

    # csvwriter.writerow(fields) # commented out to enable appending



    with open('/Users/victoriapuck-karam/Documents/all_links.txt') as csv_file: # loop through links in the file generated during Section 1

        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0

        for row in csv_reader:

            URL=row[0]





            page = requests.get(URL)

            source = str(page.content)

            soup = BeautifulSoup(page.content, 'html.parser')



            #get Phone2 and Mainphone. If mainphone is not available, choose Phone2

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

            rows = [[URL, mainphone, email, TT, TDD]]



            #print(rows)





    # writing the data rows to the output file

csvwriter.writerows(rows)

def getPhone(string):

    #function for scanning for telephone patterns within the string

    phone = ''

    phoneRegEx = re.compile('\"tel\:[\(\)\-0-9\ ]{1,}\"')

    m = phoneRegEx.search(string)

    if m:

        phone = m.group(0)[5:-1]

    return phone

def getForm1(string):
    #indentify a form with text input
    form= ''

    formRegEx= re.compile('function([a-z]*')
    x= formRegEx.search(string)

    if x:
        form= x.group()

    return form


def getEmail(string):

    #function for scanning for email indicators within the string

    email = ''

    emailRegEx = re.compile('\"mailto\:[0-9a-zA-Z\@\.]{1,}\"')

    m = emailRegEx.search(string)

    if m:

        email = m.group(0)[8:-1]

    return email



def getPhone2(string):

    #catch function for scanning for phones

    phone = ''

    reg = re.compile(".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?")

    phone = reg.findall(string)

    #return phone

    for i in phone:

        if i.lower()==i.upper(): #check for alphabet elements

            if len(i)>=10: #we need a minimum 10 digits number or 11 digits if we include '1' at the beginning

                if (i.count('.')==2 or i.count('.')==3): #Looking for a minimum two dots in the string, avoids false matches with single dot returns

                    return i

                if (i.count('(') + i.count(')')+i.count('-')>=2): # if the format is like (123)456-8679, then return the value

                    return I
