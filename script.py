from bs4 import BeautifulSoup
import requests
import json
import time

def parse():
    f = open('brTanner Conference Application.html','r')
    
    html = f.read().replace('\n','')
    f.close()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    tables = soup.find_all('table')
    
    result=[]
    
    country={}
    d={}
    for t in range(len(tables)):
        if tables[t].text.find('Additional Presenters')==-1:
            trs=tables[t].find_all('tr')
            for tr in trs:
                pair=tr.text.split(':')
                if len(pair)==2:
                    d[str(pair[0].encode('utf-8')).strip()]=str(pair[1].encode('utf-8','ignore')).strip()
                elif len(pair)>2:
                    d[str(pair[0].encode('utf-8')).strip()]=str(''.join(pair[1:]).encode('utf-8','ignore')).strip()
                key='The primary country the primary presenter were located in'
                if key in d:
                    countryName=d[key]
                    if countryName not in country:
                        url='http://maps.googleapis.com/maps/api/geocode/json?address='+countryName
                        response=requests.get(url)
                        d['location']=response.json()['results'][0]['geometry']['location']
                        country[countryName]=d['location']
                        time.sleep(10)
                    else:
                        d['location']=country[countryName]
            if t+1<len(tables) and tables[t+1].text.find('Additional Presenters')==-1:
                result.append(d)
                d={}
            
        else:
            tds=tables[t].find_all('td')
            l=[]
            sub={}
            for i in range(len(tds)):
                if i%3==0:
                    sub['Presenter Info']=str(tds[i].text.encode('utf-8')).strip()
                elif i%3==1:
                    sub['Organization']=str(tds[i].text.encode('utf-8')).strip()
                else:
                    sub['Country/State']=str(tds[i].text.encode('utf-8')).strip()
                    countryName=sub['Country/State']
                    if countryName not in country:
                        url='http://maps.googleapis.com/maps/api/geocode/json?address='+countryName
                        response=requests.get(url)
                        sub['location']=response.json()['results'][0]['geometry']['location']
                        time.sleep(10)
                    else:
                        sub['location']=country[countryName]
                    l.append(sub)
                    sub={}
            d['Additional Presenters']=l
            result.append(d)
            d={}
    with open('tanner.json','w') as out_file:    
        json.dump(result,out_file)

def toGeoJSON():
    with open('tanner.json') as data_file:    
        data = json.load(data_file)
    outfile=open('tanner.geojson','w')
    json.dump({ "type": "FeatureCollection",
                        "features": [ 
                                        {"type": "Feature",
                                         "geometry": { "type": "Point",
                                                       "coordinates": [ el['location']['lat'],
                                                                        el['location']['lng']]},
                                         "properties": { key: value 
                                                         for key, value in el.items()
                                                         if key !='location' }
                                         } 
                                     for el in data
                                     ]
                                    },outfile)
                                    
    outfile.close()