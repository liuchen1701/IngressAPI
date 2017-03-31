# -*- coding: utf-8 -*-
import config
import json
import re
import dotenv
import math
from collections import OrderedDict
try:
    from gpsoauth import perform_master_login, perform_oauth
except:
    print ('[!] only google_login_v1')

ZOOM_TO_NUM_TILES_PER_EDGE = [64, 64, 64, 64, 256, 256, 256, 1024, 1024, 1536, 4096, 4096, 6500, 6500, 6500, 9000, 9000, 9000, 9000, 9000]


usr = "ingressvragent1@gmail.com"
pwd = "ingressvr"
lat = 32.87111
lng = -117.2029
zoom = 19
v = "a3d6e9e025fd26d48d95d04ca0fbf9bd67575e2b"

def get_mercator_tile(lat, lng ,zoom=17, pMinLevel=0, pMaxLevel=8, maxHealth=100):
    z = ZOOM_TO_NUM_TILES_PER_EDGE[zoom]
    lg = ((lng + 180) / 360 * z)
    lt = ((1 - math.log(math.tan(lat * math.pi / 180) + 1 / math.cos(lat * math.pi / 180)) / math.pi) / 2 * z)
    tileKey = str(str(zoom) + "_" + str(int(lg)) + "_" + str(int(lt)) + "_" + str(pMinLevel) + "_" + str(pMaxLevel) + "_" + str(maxHealth))
    return tileKey

def login_google(email,passw,lat, lng, zoom, v):
    config.s.headers.update({'User-Agent':'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143'})
    first = "https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/#identifier"
    second='https://accounts.google.com/AccountLoginInfo'
    third='https://accounts.google.com/signin/challenge/sl/password'
    last='https://accounts.google.com/o/oauth2/token'
    intelEntry='https://accounts.google.com/ServiceLogin?service=ah&passive=true&continue=https%3A%2F%2Fappengine.google.com%2F_ah%2Fconflogin%3Fcontinue%3Dhttps%3A%2F%2Fingress.com%2Fintel&ltmpl=gm&shdf=ChMLEgZhaG5hbWUaB0luZ3Jlc3MMEgJhaCIUcMYuYO1Lk5u7SiOb-WORYbrbL78oATIUZZlamMUM8jHROORFU4jGUaaxstg#identifier'
    r=config.s.get(first)

    GALX= re.search('<input type="hidden" name="GALX" value=".*">',r.content.decode())
    gxf= re.search('<input type="hidden" name="gxf" value=".*:.*">',r.content.decode())
    cont = re.search('<input type="hidden" name="continue" value=".*">',r.content.decode())

    GALX=re.sub('.*value="','',GALX.group(0))
    GALX=re.sub('".*','',GALX)

    gxf=re.sub('.*value="','',gxf.group(0))
    gxf=re.sub('".*','',gxf)

    cont=re.sub('.*value="','',cont.group(0))
    cont=re.sub('".*','',cont)

    data1={'Page':'PasswordSeparationSignIn',
            'GALX':GALX,
            'gxf':gxf,
            'continue':cont,
            'ltmpl':'embedded',
            'scc':'1',
            'sarp':'1',
            'oauth':'1',
            'ProfileInformation':'',
            '_utf8':'?',
            'bgresponse':'js_disabled',
            'Email':email,
            'signIn':'Next'}
    r1=config.s.post(second,data=data1)

    profile= re.search('<input id="profile-information" name="ProfileInformation" type="hidden" value=".*">',r1.content.decode())
    gxf= re.search('<input type="hidden" name="gxf" value=".*:.*">',r1.content.decode())

    gxf=re.sub('.*value="','',gxf.group(0))
    gxf=re.sub('".*','',gxf)

    profile=re.sub('.*value="','',profile.group(0))
    profile=re.sub('".*','',profile)

    data2={'Page':'PasswordSeparationSignIn',
            'GALX':GALX,
            'gxf':gxf,
            'continue':cont,
            'ltmpl':'embedded',
            'scc':'1',
            'sarp':'1',
            'oauth':'1',
            'ProfileInformation':profile,
            '_utf8':'?',
            'bgresponse':'js_disabled',
            'Email':email,
            'Passwd':passw,
            'signIn':'Sign in',
            'PersistentCookie':'yes'}
    r2=config.s.post(third,data=data2)
    fourth=r2.history[len(r2.history)-1].headers['Location'].replace('amp%3B','').replace('amp;','')
    # print(fourth)

    r3=config.s.request("GET", intelEntry, allow_redirects=True)
    # print(r3.content.decode())

    intel2=str('https://www.ingress.com/intel?ll='+ str(lat) + ',' + str(lng) + '&z=' + str(zoom))
    r4=config.s.get(intel2)
    # print(r4.content.decode())
    csrf = re.search("<input type='hidden' name='csrfmiddlewaretoken' value='.*' />",r4.content.decode())
    csrf=re.sub(".*value='",'',csrf.group(0))
    csrf=re.sub("'.*",'',csrf)
    print(csrf)

    #config.s.headers.update({'x-csrftoken':csrf})
    config.s.headers.update({'referer':'https://ingress.com/intel'})
    config.s.headers.update({'x-csrftoken':csrf})
    config.s.cookies.update({'csrftoken':csrf})

    getEntites='https://ingress.com/r/getEntities'
    print(get_mercator_tile(lat, lng, zoom))
    payload={'tileKeys': [get_mercator_tile(lat, lng, zoom)],
        'v': v}
    r5=config.s.post(getEntites, json=payload)
    print("r5: " + r5.content.decode())
    # print("r5: " + r5.json())


login_google(usr, pwd, lat, lng, zoom, v)
