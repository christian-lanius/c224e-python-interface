#!/usr/bin/env python
# -*- coding: utf-8 -*-


from robobrowser import RoboBrowser
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class C224eUser:
    def __init__(self):
        self.loggedIn = False
        self.address = ""
        self.br = ""
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def changePassword(self, oldPw, newPw):
        if(not self.loggedIn):
            return
        self.br.open('https://'+self.address+'/wcd/system_password.xml', verify=False)
        token = self.br.find('token').get_text()
        print(token)
        data = { 'func' : 'PSL_S_UPC_USR',
                'H_FAV' : '',
                'h_token' : token,
                'S_UPC_P_CUR' : oldPw,
                'S_UPC_P_NO' : newPw,

        }
        self.br.open('https://'+self.address+'/wcd/user.cgi', method='post', data = data, verify=False)
        if( not (self.br.parsed.find('item').get_text() == 'Ok_1')):
                print('Error occured changing password: {}'.format(self.br.parsed.find('item').get_text()))

    def login(self, user, password, host):
        self.address = host

        self.br = RoboBrowser(history=True,parser='html.parser')
        self.br.allow_redirects = True
        self.br.open('https://'+self.address+'/wcd/top.html', verify=False)

        form = self.br.get_forms()
        form = form[0]
        form['username'] = user
        form['password'] = password
        self.br.submit_form(form)

        self.br.open('https://'+self.address+'/wcd/proglog', verify=False)
        i = 0
        while i < 20:
            self.br.open('https://'+self.address+'/wcd/proglog', verify=False)
            if(self.br.parsed.find_all('iframe')):
                break
            if(self.br.parsed.find('item').get_text() == 'AuthIllegalAcount'):
                print('Can not login as {}: Password wrong or user does not exist'.format(user))
                self.loggedIn = False
                return False
            self.br.open('https://'+self.address+'/wcd/preference.xml', verify=False)
            time.sleep(3)
            i = i + 1
        if( i == 20):
            print('Timeout occured during login of user')
            self.loggedIn = False
            return False
        print('Logged in')
        self.br.open('https://'+self.address+'/wcd/system_device.xml', verify=False);
        self.loggedIn = True
        return True

    def getLimits(self):
        if not self.loggedIn:
            return
        self.br.open('https://'+self.address+'/wcd/system_authset.xml', verify=False)

        bwLimit = self.br.find('bwprint').limit.get_text()
        print('Black and White Limit: {}'.format(bwLimit))

        colorLimit = self.br.find('colorprint').limit.get_text()
        print('Color Limit: {}'.format(colorLimit))

        bwCounter = self.br.find('counter').count.get_text()
        print('Black and White used: {}'.format(bwCounter))

        counters = self.br.find_all('counter')

        colorCounter = counters[2].count.get_text()
        print('Color used: {}'.format(colorCounter))

        limits = {}
        limits['bwLimit'] = bwLimit
        limits['cLimit'] = colorLimit
        limits['bwCount'] = bwCounter
        limits['cCount'] = colorCounter

        return limits

    def logout(self):
        if not self.loggedIn:
            return
        data = {'func' : 'PSL_ACO_LGO'}
        self.br.open('https://'+self.address+'/wcd/user.cgi', method='post', data = data, verify=False)
        print('Logged out as user')

        self.loggedIn = False

    def __del__(self):
        self.logout()