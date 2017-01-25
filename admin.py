#!/usr/bin/env python
# -*- coding: utf-8 -*-

from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import time


class C224eAdmin:
    def __init__(self):
        self.token = ''
        self.loggedIn = False
        self.address = ""
        self.br = ""

    def logout(self):
        if not self.loggedIn:
            return
        data = {'func' : 'PSL_ACO_LGO'}
        self.br.open('http://'+self.address+'/wcd/a_user.cgi', method='post', data = data)
        print('Logged out as administrator')

        self.loggedIn = False

    def login(self, password, host):
        if(self.loggedIn):
            self.logout()

        self.address = host
        self.br = RoboBrowser(history=True)
        self.br.allow_redirects = True
        self.br.session.cookies['ver_expires'] = 'Thu, 11 Jan 2099 17:53:10 GMT'
        self.br.session.cookies['adm'] = 'AS_COU'
        self.br.session.cookies['uatype'] = 'NN'
        self.br.session.cookies['param'] = ''
        self.br.session.cookies['access'] = ''
        self.br.session.cookies['usr'] = 'S_INF'
        self.br.session.cookies['lang'] = 'De'
        self.br.session.cookies['favmode'] = 'false'
        self.br.session.cookies['selno'] = 'De'
        self.br.session.cookies['vm'] = 'Html'
        self.br.session.cookies['bm'] = 'Low'
        self.br.session.cookies['wd'] = 'n'
        self.br.session.cookies['help'] = 'off,off,off'
        data = { 'func' : 'PSL_LP1_LOG',
                'R_ADM' : 'AdminAdmin',
                'password' : password
        }
        self.br.open('http://'+self.address+'/wcd/login.cgi', method='post', data = data)
        #print(len(self.br.response.content.decode('UTF-8')))
        soup = BeautifulSoup(self.br.response.content.decode('UTF-8'), 'lxml')
        #print(soup.prettify)
        if(soup.find('message')):
            message = soup.find('message').item.contents

            if(message[0] == 'AdminActiveJobLoginError'):
                print('Can not login as admin: Active job exists')
                self.loggedIn = False
                return False
            if(message[0] == 'CommonLoginError'):
                print('Can not login as admin: Password incorrect')
                self.loggedIn = False
                return False
            if(message[0] == 'AdminAnotherLoginError'):
                print('Can not login as admin: Another admin is already logged in')
                self.loggedIn = False
                return False

        self.loggedIn = True
        print('Logged in as administrator')
        self.updateToken('http://' + self.address + '/wcd/a_system_counter.xml')
        return True

    def createUser(self, username, password):
        if not self.loggedIn:
            return
        print('Creating user {}'.format(username))
        self.updateToken('http://' + self.address + '/wcd/a_system_counter.xml')
        #print(self.token)
        data = {'func' : 'PSL_AA_USR_USR',
                'h_token' : self.token,
                'AA_USR_H_NUM' : 'new',
                'AA_USR_R_RNM' : 'Space',
                'AA_USR_H_UNA' : '',
                'AA_USR_T_UNA' : username,
                'AA_USR_T_ADD' : '',
                'AA_USR_P_UP' : password,
                'AA_USR_P_CMP' : password,
                'AA_USR_S_ACS' : 'Off',
                'AA_USR_S_FCP' : 'All',
                'AA_USR_S_FSC' : 'All',
                'AA_USR_S_FSU' : 'On',
                'AA_USR_S_FUB' : 'On',
                'AA_USR_S_FPR' : 'All',
                'AA_USR_S_FBO' : 'true',
                'AA_USR_S_FPS' : 'All',
                'AA_USR_S_FMI' : 'On',
                'AA_USR_C_CPL' : 'on', #is color restricted?
                'AA_USR_T_CPL' : '1', #number of color copies allowed
                'AA_USR_C_BPL' : 'on', #is b/w restricted?
                'AA_USR_T_BPL' : '1', #number of b/w copies allowed
                'AA_USR_C_RFL' : 'on',
                'AA_USR_S_RPL' : '0'
        }
        self.br.open('http://'+self.address+'/wcd/a_user.cgi', method='post', data = data)
        soup = BeautifulSoup(self.br.response.content.decode('UTF-8'), 'lxml')

        if(soup.find('item')):
            if(soup.find('item').contents[0]=='AuthUserAlreadyExist'):
                print('Can not create user {}: Already existing'.format(username))
                #print(self.br.parsed.prettify())

    def deleteUser(self, username):
        if not self.loggedIn:
            return
        print('Deleting user {}'.format(username))
        user = self.getUserByName(username);
        if not user:
            return
        data = {'func' : 'PSL_AA_USR_DEL',
                'h_token' : self.token,
                'AA_USR_H_NUM' : user['userID'],
                'AA_USR_H_UNA' : user['username'],
                'AA_USR_H_SNM' : ''
        }
        self.br.open('http://'+self.address+'/wcd/a_user.cgi', method='post', data = data)
        soup = BeautifulSoup(self.br.response.content.decode('UTF-8'), 'lxml')
        retCode = soup.find('item')
        if not(retCode and retCode.contents[0] == 'Ok_1'):
            print('Could not delete user {}'.format(username))

        self.br.open('http://'+self.address+'/wcd/a_authentication_user.xml')

    def changePassword(self, username, newPassword):
        if not self.loggedIn:
            return
        print('Changing password for {}'.format(username))
        user = self.getUserByName(username);
        if not user:
            return
        self.updateToken('http://' + self.address + '/wcd/a_system_counter.xml')
        data = {'func' : 'PSL_AA_USR_USR',
                'h_token' : self.token,
                'AA_USR_H_NUM' : user['userID'],
                'AA_USR_T_NUM' : user['userID'],
                'AA_USR_H_UNA' : user['username'],
                'AA_USR_T_UNA' : user['username'],
                'AA_USR_T_ADD' : user['email'],
                'AA_USR_C_CUS' : 'on',
                'AA_USR_P_UP' : newPassword,
                'AA_USR_P_CMP' : newPassword,
                'AA_USR_S_ACS' : 'Off',
                'AA_USR_S_FCP' : 'All',
                'AA_USR_S_FSC' : 'All',
                'AA_USR_S_FSU' : 'On',
                'AA_USR_S_FUB' : 'On',
                'AA_USR_S_FPR' : 'All',
                'AA_USR_S_FBO' : 'true',
                'AA_USR_S_FPS' : 'All',
                'AA_USR_S_FMI' : 'On',
                'AA_USR_C_CPL' : 'on', #is color restricted?
                'AA_USR_T_CPL' : user['numColorAllowed'], #number of color copies allowed
                'AA_USR_C_BPL' : 'on', #is b/w restricted?
                'AA_USR_T_BPL' : user['numBwAllowed'], #number of b/w copies allowed
                'AA_USR_C_RFL' : 'on',
                'AA_USR_S_RPL' : '0'
        }
        self.br.open('http://'+self.address+'/wcd/a_user.cgi', method='post', data = data)
        #TODO: Verify it worked

    def updateToken(self, link):
        if not self.loggedIn:
            return
        self.br.open(link)
        soup = BeautifulSoup(self.br.response.content.decode('UTF-8'), 'lxml')
        if(soup.find('token')):
            self.token = soup.find('token').contents[0]
            #print(self.token)
        else:
            print('Can not read token from server.')
            print(soup.prettify())
            self.logout()

    def getUserByName(self, username):
        if not self.loggedIn:
            return
        # wir können bis zu 1000 user haben, immer in 50 user/seite aufgeteilt.
        self.updateToken('http://' + self.address + '/wcd/a_authentication_user.xml')
        for i in range(0,19):
            data = {'func' : 'PSL_AA_USR_PAG',
            'h_token' : self.token,
            'H_SRT' : str(1+i*50),
            'H_END' : str(50*(i+1))
            }
            self.br.open('http://'+self.address+'/wcd/a_user.cgi', method='post', data = data)
            #get new token
            self.updateToken('http://' + self.address + '/wcd/a_authentication_user.xml')

            self.br.open('http://'+self.address+'/wcd/a_user.xml')
            soup = BeautifulSoup(self.br.response.content.decode('UTF-8'), 'lxml')

            userRaw = soup.find_all('authusersetting')
            #print(soup.find_all('authno'))
            for k in range(0,len(userRaw)):
                name = userRaw[k].contents[6].contents[0]
                if(name == username):
                    user = {}
                    user['username'] = name
                    user['userID'] = soup.find_all('authno')[k].contents[0]
                    #user['email'] = userRaw[k].contents[10].contents[0]
                    user['email'] = ""
                    user['numColorAllowed'] = soup.find_all('colorprint')[k].contents[1].contents[0]
                    user['numBwAllowed'] = soup.find_all('bwprint')[k].contents[1].contents[0]
                    print('Found user: {}'.format(user))
                    return user
            if(len(userRaw)<50):
                break;
        print('Did not find user in database')

    def setLimits(self, username, bw, color, mode='abs'):
        if not self.loggedIn:
            return
        user = self.getUserByName(username)
        if not user:
            return
        self.updateToken('http://' + self.address + '/wcd/a_system_counter.xml')
        if(mode == 'inc'):
            user['numColorAllowed'] = str(int(user['numColorAllowed']) + color)
            user['numBwAllowed'] = str(int(user['numBwAllowed']) + bw)
            print('Increment allowed number of pages to bw: {}, color:{} for {}'.format(user['numBwAllowed'],user['numColorAllowed'], username))
        elif mode == 'abs':
            user['numColorAllowed'] = str(color)
            user['numBwAllowed'] = str(bw)
            print('Set allowed number of pages to bw: {}, color:{} for {}'.format(user['numBwAllowed'],user['numColorAllowed'], username))
        else:
            print('Unknown mode, choose either inc for incremental or abs for absolute')
            self.logout()
            return
        data = {'func' : 'PSL_AA_USR_USR',
                'h_token' : self.token,
                'AA_USR_H_NUM' : user['userID'],
                'AA_USR_T_NUM' : user['userID'],
                'AA_USR_H_UNA' : user['username'],
                'AA_USR_T_UNA' : user['username'],
                'AA_USR_T_ADD' : user['email'],
                'AA_USR_S_ACS' : 'Off',
                'AA_USR_S_FCP' : 'All',
                'AA_USR_S_FSC' : 'All',
                'AA_USR_S_FSU' : 'On',
                'AA_USR_S_FUB' : 'On',
                'AA_USR_S_FPR' : 'All',
                'AA_USR_S_FBO' : 'true',
                'AA_USR_S_FPS' : 'All',
                'AA_USR_S_FMI' : 'On',
                'AA_USR_C_CPL' : 'on', #is color restricted?
                'AA_USR_T_CPL' : user['numColorAllowed'], #number of color copies allowed
                'AA_USR_C_BPL' : 'on', #is b/w restricted?
                'AA_USR_T_BPL' : user['numBwAllowed'], #number of b/w copies allowed
                'AA_USR_C_RFL' : 'on',
                'AA_USR_S_RPL' : '0'
        }
        self.br.open('http://'+self.address+'/wcd/a_user.cgi', method='post', data = data)
        #TODO: Verify everything worked