import urllib2
import re
import os
from bs4 import BeautifulSoup

def get_ty_links():
    
    years = []
    year_links = []
    for i in range(1979,2017):
        years.append(str(i))
        year_links.append('http://agora.ex.nii.ac.jp/digital-typhoon/year/wnp/'+str(i)+'.html.en')

    tys = []
    ty_links = []
    for i in range(0,len(years)):
        html = urllib2.urlopen(year_links[i]).read()
        soup = BeautifulSoup(html,"html.parser")
        row1 = soup.find_all(attrs={"class":"ROW1"})
        row0 = soup.find_all(attrs={"class":"ROW0"})
        # get all typhoon-page links
        number = len(row1)+len(row0)
        for j in range(1,10):
            tys.append(years[i]+'0'+str(j))
            ty_links.append('http://agora.ex.nii.ac.jp/digital-typhoon/summary/wnp/k/'+\
                            years[i]+'0'+str(j)+'.html.en')
        for j in range(10,number+1):
            tys.append(years[i]+str(j))
            ty_links.append('http://agora.ex.nii.ac.jp/digital-typhoon/summary/wnp/k/'+\
                            years[i]+str(j)+'.html.en')

    return tys,ty_links

def download_imgs(tys,ty_links):

    path_ = os.path.abspath('.')
    root = path_ + '/tys_raw/'
    if not os.path.exists(root):
	os.mkdir(root)
    
    for i in range(0,len(ty_links)):
        html = urllib2.urlopen(ty_links[i]).read()
        soup = BeautifulSoup(html,"html.parser")
        a_list = soup.find_all('a')
        # all satellite images for every 6 hour
        for a in a_list:
            if a.string != '\nImage':
                continue
            
            image_link = 'http://agora.ex.nii.ac.jp/'+ a['href']
            html_new = urllib2.urlopen(image_link).read()
            soup_new = BeautifulSoup(html_new,"html.parser")
            tr_list = soup_new.find_all('tr')

            boo = False
            wind = '0'
            for tr in tr_list:
                if tr.string == '\nMaximum Wind\n':
                    tr_next = tr.next_sibling.next_sibling
                    if tr_next.string[0] == '0': # 0kt should be excluded
                        boo = True
                        break
                    wind = str(re.findall(r'\d+',tr_next.string))
            if boo: # 0kt should be excluded
                continue

            pressure = '1000'
            for tr in tr_list:
                if tr.string == '\nCentral Pressure\n':
                    tr_next = tr.next_sibling.next_sibling
                    pressure = str(re.findall(r'\d+',tr_next.string))
            
            pict_list = []
            anew_list = soup_new.find_all('a')
            for anew in anew_list: # find ir images
                if anew.string == 'Magnify this':
                    st = anew['href'].replace('/0/','/1/') # replace vis to ir
                    pict_list.append('http://agora.ex.nii.ac.jp'+ st)
            
            try: # save images
                s = pict_list[2]
                # filename : typhoon-number_time(YYMMDDHH)_wind_pressure.jpg
                filename = tys[i]+'_'+s[len(s)-19:len(s)-11]+'_'+wind+'_'+pressure
                filename = rename(filename)

                f = open(root+filename+'.jpg','wb')
                req = urllib2.urlopen(s)
                buf = req.read()
                f.write(buf)
                f.close()

            except Exception as e:
                print e

	print tys[i],'has been downloaded.'

def rename(fname): # there maybe some unexcepted char in fname, drop them

    new_fname = fname.replace('[','')
    new_fname = new_fname.replace(']','')
    new_fname = new_fname.replace('u','')
    new_fname = new_fname.replace('\'','')
    return new_fname
	    
if __name__ == '__main__':

    ts,links = get_ty_links()
    download_imgs(ts,links)
