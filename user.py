#!/usr/bin/env python
# -*- coding: utf-8 -*-


from robobrowser import RoboBrowser
import time

class C224eUser:
    def __init__(self):
        self.loggedIn = False
        self.address = ""
        self.br = ""

    def changePassword(self, oldPw, newPw):
        if(not self.loggedIn):
            return
        self.br.open('http://'+self.address+'/wcd/system_password.xml')
        token = self.br.find('token').get_text()
        print(token)
        data = { 'func' : 'PSL_S_UPC_USR',
                'H_FAV' : '',
                'h_token' : token,
                'S_UPC_P_CUR' : oldPw,
                'S_UPC_P_NO' : newPw,

        }
    #     self.br.session.cookies['ver_expires'] = 'Thu, 11 Jan 2018 17:53:10 GMT'
    #     self.br.session.cookies['adm'] = 'AA_USR'
    #     self.br.session.cookies['uatype'] = 'NN'
    #     self.br.session.cookies['param'] = ''
    #     self.br.session.cookies['access'] = ''
    #     self.br.session.cookies['usr'] = 'S_UPC'
        self.br.open('http://'+self.address+'/wcd/user.cgi', method='post', data = data)
        self.br.open('http://'+self.address+'/wcd/preferences.xml')
        self.br.open('http://'+self.address+'/wcd/top.html')

    def login(self, user, password, host):
        self.address = host

        self.br = RoboBrowser(history=True,parser='html.parser')
        self.br.allow_redirects = True
        self.br.open('http://'+self.address+'/wcd/top.html')

        form = self.br.get_forms()
        form = form[0]
        form['username'] = user
        form['password'] = password
        self.br.submit_form(form)

        self.br.open('http://'+self.address+'/wcd/proglog')
        while 1:
            self.br.open('http://'+self.address+'/wcd/proglog')
            if(self.br.parsed.find_all('iframe')):
                break
            if(self.br.parsed.find('item').get_text() == 'AuthIllegalAcount'):
                print('Can not login as {}: Password wrong or user does not exist'.format(user))
                self.loggedIn = False
                return False
            self.br.open('http://'+self.address+'/wcd/preference.xml')
            time.sleep(3)
        print('Logged in')
        self.br.open('http://'+self.address+'/wcd/system_device.xml');

        self.loggedIn = True
        return True

    def getLimits(self):
        if not self.loggedIn:
            return
        self.br.open('http://'+self.address+'/wcd/system_authset.xml')

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
        self.br.open('http://'+self.address+'/wcd/user.cgi', method='post', data = data)
        print('Logged out as user')

        self.loggedIn = False

    def __del__(self):
        self.logout()