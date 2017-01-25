from robobrowser import RoboBrowser
import time

def changePassword(user, oldPw, newPw, br):
    print("Trying to log in")
    
    br.open('http://137.226.183.224/wcd/system_password.xml')
    token = br.find('token').get_text()
    print(token)
    data = { 'func' : 'PSL_S_UPC_USR',
            'H_FAV' : '',
            'h_token' : token,
            'S_UPC_P_CUR' : oldPw,
            'S_UPC_P_NO' : newPw,
        
    }
#     br.session.cookies['ver_expires'] = 'Thu, 11 Jan 2018 17:53:10 GMT'
#     br.session.cookies['adm'] = 'AA_USR'
#     br.session.cookies['uatype'] = 'NN'
#     br.session.cookies['param'] = ''
#     br.session.cookies['access'] = ''
#     br.session.cookies['usr'] = 'S_UPC'
    br.open('http://137.226.183.224/wcd/user.cgi', method='post', data = data)
    br.open('http://137.226.183.224/wcd/preferences.xml')
    br.open('http://137.226.183.224/wcd/top.html')
    
def login(user, password):
    br = RoboBrowser(history=True)
    br.allow_redirects = True
    br.open('http://137.226.183.224/wcd/top.html')
    
    
    form = br.get_forms()
    form = form[0]
    form['username'] = user
    form['password'] = password
    br.submit_form(form)
    
    br.open('http://137.226.183.224/wcd/proglog')
    while 1:
        br.open('http://137.226.183.224/wcd/proglog')
        if(br.parsed.find_all('iframe')):
            break
        br.open('http://137.226.183.224/wcd/preference.xml')
        time.sleep(3)
    print('Logged in')
    br.open("http://137.226.183.224/wcd/system_device.xml");
    return br

def getLimits(br):
    br.open('http://137.226.183.224/wcd/system_authset.xml')
    
    bwLimit = br.find('bwprint').limit.get_text()
    print('Black and White Limit: {}'.format(bwLimit))
    
    colorLimit = br.find('colorprint').limit.get_text()
    print('Color Limit: {}'.format(colorLimit))
    
    bwCounter = br.find('counter').count.get_text()
    print('Black and White used: {}'.format(bwCounter))
    
    counters = br.find_all('counter')
    
    colorCounter = counters[2].count.get_text()
    print('Color used: {}'.format(colorCounter))
    
    limits = {}
    limits['bwLimit'] = bwLimit
    limits['cLimit'] = colorLimit
    limits['bwCount'] = bwCounter
    limits['cCount'] = colorCounter
    
    return limits
    
