from bs4 import BeautifulSoup
import requests
import re
import shutil

params_login = {
    'username' : "username",
    'password' : "password"
}

session = requests.Session()

s = session.post('http://dsu.edu.in/moodle29/login/index.php', data=params_login)

s = session.get('http://dsu.edu.in/moodle29/course/view.php?id=4')

bsObj = BeautifulSoup(s.text)

sectionArray = []
activityinstance_array = []


for i in range(1,len(bsObj.findAll(id=""))):

    #sectionArray.append(bsObj.findAll(id="section-" + str(i)))
    try:
        sectionArray.append(bsObj.find(id="section-" + str(i)).findAll('div', {'class':'activityinstance'}))

    except AttributeError:
        pass


#now converting it into text and sending it again to bs4 parser

for i in range(0, len(sectionArray)):

    newBsObj = BeautifulSoup(str(sectionArray[i]))

    for instance in newBsObj.findAll('div', {"class":"activityinstance"}):
    
        #print(BeautifulSoup(str(instance)).find('span', {"class":"instancename"}).get_text())
        file_name = BeautifulSoup(str(instance)).find('span', {"class":"instancename"}).get_text() + ".pdf"
    
        #print(BeautifulSoup(str(instance)).find('a').attrs['href'])
        url_name = str(BeautifulSoup(str(instance)).find('a').attrs['href'])

        if re.search("/resource/", url_name):
        
            s = session.get(url_name, stream=True)
            with open('pdf/' + file_name, 'wb') as f:
                shutil.copyfileobj(s.raw, f)