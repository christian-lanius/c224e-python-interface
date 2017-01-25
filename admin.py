from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import time
token = ''
loggedIn = False
address = ""
def logout(br):
    global loggedIn
    if loggedIn:
        data = {'func' : 'PSL_ACO_LGO'}
        br.open('http://'+address+'/wcd/a_user.cgi', method='post', data = data)
        print('Logged out as administrator')
        
        loggedIn = False
    
def login(password, ipaddress):
    global address
    address = ipaddress
    br = RoboBrowser(history=True)
    br.allow_redirects = True
    br.session.cookies['ver_expires'] = 'Thu, 11 Jan 2099 17:53:10 GMT'
    br.session.cookies['adm'] = 'AS_COU'
    br.session.cookies['uatype'] = 'NN'
    br.session.cookies['param'] = ''
    br.session.cookies['access'] = ''
    br.session.cookies['usr'] = 'S_INF'
    br.session.cookies['lang'] = 'De'
    br.session.cookies['favmode'] = 'false'
    br.session.cookies['selno'] = 'De'
    br.session.cookies['vm'] = 'Html'
    br.session.cookies['bm'] = 'Low'
    br.session.cookies['wd'] = 'n'
    br.session.cookies['help'] = 'off,off,off'
    data = { 'func' : 'PSL_LP1_LOG',
            'R_ADM' : 'AdminAdmin',
            'password' : password
    }
    br.open('http://'+address+'/wcd/login.cgi', method='post', data = data)
    global loggedIn
#     print(len(br.response.content.decode('UTF-8')))
    soup = BeautifulSoup(br.response.content.decode('UTF-8'), 'lxml')
#     print(soup.prettify)
    if(soup.find('message')):
        message = soup.find('message').item.contents
        
        if(message[0] == 'AdminActiveJobLoginError'):
            print('Can not login as admin: Active job exists')
            loggedIn = False
            return br
        if(message[0] == 'CommonLoginError'):
            print('Can not login as admin: Password incorrect')
            loggedIn = False
            return br
        if(message[0] == 'AdminAnotherLoginError'):
            print('Can not login as admin: Another admin is already logged in')
            loggedIn = False
            return br
    
    loggedIn = True
    print('Logged in as administrator')
    _updateToken(br, 'http://'+address+'/wcd/a_system_counter.xml')
    return br

def createUser(username, password, br):
    if loggedIn:
        print('Creating user {}'.format(username))
        _updateToken(br, 'http://'+address+'/wcd/a_system_counter.xml')
    #     print(token)
        data = {'func' : 'PSL_AA_USR_USR',
                'h_token' : token,
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
        br.open('http://'+address+'/wcd/a_user.cgi', method='post', data = data)
        soup = BeautifulSoup(br.response.content.decode('UTF-8'), 'lxml')
    
        if(soup.find('item')):
            if(soup.find('item').contents[0]=='AuthUserAlreadyExist'):
                print('Can not create user {}: Already existing'.format(username))
    #     print(br.parsed.prettify())
    
def deleteUser(username, br):
    if loggedIn:
        print('Deleting user {}'.format(username))
        user = _getUserByName(username, br);
        if not user:
            return
        data = {'func' : 'PSL_AA_USR_DEL',
                'h_token' : token,
                'AA_USR_H_NUM' : user['userID'],
                'AA_USR_H_UNA' : user['username'],
                'AA_USR_H_SNM' : ''
        }
        br.open('http://'+address+'/wcd/a_user.cgi', method='post', data = data)
        soup = BeautifulSoup(br.response.content.decode('UTF-8'), 'lxml')
        retCode = soup.find('item')
        if  not(retCode and retCode.contents[0] == 'Ok_1'):
            print('Could not delete user {}'.format(username))
        
        br.open('http://'+address+'/wcd/a_authentication_user.xml')
        
def changePassword(username, newPassword, br):
    if loggedIn:
        print('Changing password for {}'.format(username))
        user = _getUserByName(username, br);
        if not user:
            return
        _updateToken(br, 'http://'+address+'/wcd/a_system_counter.xml')
        data = {'func' : 'PSL_AA_USR_USR',
                'h_token' : token,
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
        br.open('http://'+address+'/wcd/a_user.cgi', method='post', data = data)
        #TODO: Verify it worked

def _updateToken(br, link):
    if loggedIn:
        br.open(link)
        global token 
        soup = BeautifulSoup(br.response.content.decode('UTF-8'), 'lxml')
        if(soup.find('token')):
            token = soup.find('token').contents[0]
    #         print(token)
        else:
            print('Can not read token from server.')
            print(soup.prettify())
            logout(br)
            
            
def _getUserByName(username, br):
    if loggedIn:
    # wir können bis zu 1000 user haben, immer in 50 user/seite aufgeteilt.
        _updateToken(br, 'http://'+address+'/wcd/a_authentication_user.xml')
        for i in range(0,19):
            data = {'func' : 'PSL_AA_USR_PAG',
            'h_token' : token,
            'H_SRT' : str(1+i*50),
            'H_END' : str(50*(i+1))
            }
            br.open('http://'+address+'/wcd/a_user.cgi', method='post', data = data)
            #get new token
            _updateToken(br,'http://'+address+'/wcd/a_authentication_user.xml')
            
            br.open('http://'+address+'/wcd/a_user.xml')
            soup = BeautifulSoup(br.response.content.decode('UTF-8'), 'lxml')
            
            userRaw = soup.find_all('authusersetting')
#             print(soup.find_all('authno'))
            for k in range(0,len(userRaw)):
                name = userRaw[k].contents[6].contents[0]
                if(name == username):
                    user = {}
                    user['username'] = name
                    user['userID'] = soup.find_all('authno')[k].contents[0]
    #                 user['email'] = userRaw[k].contents[10].contents[0]
                    user['email'] = ""
                    user['numColorAllowed'] = soup.find_all('colorprint')[k].contents[1].contents[0]
                    user['numBwAllowed'] = soup.find_all('bwprint')[k].contents[1].contents[0]
                    print('Found user: {}'.format(user))
                    return user
            if(len(userRaw)<50):
                break;
        print('Did not find user in database')
        
        
def setLimits(username, bw, color, mode, br):
    if loggedIn:
        user = _getUserByName(username, br);
        if not user:
            return
        _updateToken(br, 'http://'+address+'/wcd/a_system_counter.xml')
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
            logout(br)
            return
        data = {'func' : 'PSL_AA_USR_USR',
                'h_token' : token,
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
        br.open('http://'+address+'/wcd/a_user.cgi', method='post', data = data)    
        #TODO: Verify everything worked