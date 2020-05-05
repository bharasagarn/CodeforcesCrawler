import requests
from bs4 import BeautifulSoup

def getFutureContests():
    page = requests.get('https://codeforces.com/contests')
    soup = BeautifulSoup(page.content,'html.parser')
    ctable = soup.find('div',{'class':'datatable'})
    crows = ctable.find_all('tr')
    cntdata = []
    for contest in crows[1:]:
        cn = {}
        cn['cname'] = contest.find('td').text[2:-6]
        atags = contest.find_all('a')
        csched = ''
        for atag in atags:
            if(atag['href'][:16]=='https://www.time'):
                csched = atag.text[1:-1]
                break
        cn['date'] = csched.split(' ')[0]
        cn['time'] = csched.split(' ')[1]
        cntdata.append(cn)
    print('fetching done!')
    return cntdata

def getPastContestsHelper(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    ctable = soup.find_all('div',{'class':'datatable'})[1]
    crows = ctable.find_all('tr')
    cntdata = []
    for contest in crows[1:]:
        cn = {}
        cn['cid'] = contest.get('data-contestid')
        cn['cname'] = contest.find('td').text[2:-6]
        cn['date'] = contest.find_all('td')[2].find('span',{'class':'format-date'}).text.split(' ')[0]
        cn['time'] = contest.find_all('td')[2].find('span',{'class':'format-date'}).text.split(' ')[1]
        cntdata.append(cn)
    return cntdata

def getPages():
    page = requests.get('https://codeforces.com/contests')
    soup = BeautifulSoup(page.content,'html.parser')
    pagelist = soup.find_all('span',{'class':'page-index'})
    cnt = pagelist[-1].find('a')['href'].split('/')[-1]
    return cnt