import sys, urllib2, base64, re
import xml.etree.ElementTree as ET

def printFlush(msg):
    print msg
    sys.stdout.flush()

def getTagName(element):
    return element.tag[element.tag.rfind('}')+1:].title()
    

def addAuthHeader(request, user, password):
    pwd_hash = base64.encodestring('%s:%s' % (user, password)).strip()
    request.add_header('Authorization', 'Basic %s' % pwd_hash)


def checkElementSitemap(element, user = '', password = ''):
    
    for child in element:
        if getTagName(child) == 'Loc':
            loadSitemap(child.text, user, password)
            break


def checkElementUrl(element, user = '', password = ''):
    url = element[0].text
    request = urllib2.Request(url)
  
    if user and password:
        addAuthHeader(request, user, password)
    
    try:
        resource = urllib2.urlopen(request)
        data = resource.read()
        data_len = len(data)
        
        msg = resource.msg
        
        if msg != 'OK' or data_len == 0:
            msg = 'NOK'
        
        printFlush('%s %s %s %s' % (msg,
                                    resource.getcode(),
                                    data_len,
                                    url))
        
        
    except urllib2.URLError, e:
        printFlush('NOK %s %s' % (url, e.code))


def parseSitemap(xml_text, user = '', password = ''):
    
    root = ET.fromstring(xml_text)
    
    for i in root:
        
        tag = getTagName(i)
        
        func_name = 'checkElement%s' % tag
        
        if func_name in check_functions:
            check_functions[func_name](i, user, password)


def loadSitemap(url, user = '', password = ''):
    
    printFlush('Loading sitemap %s' % url)
    
    request = urllib2.Request(url)
    
    if user and password:
        addAuthHeader(request, user, password)
    
    try:
        resource = urllib2.urlopen(request)
        
    except urllib2.URLError, e:
        printFlush('%s: %s' % (url, e.code))
        quit()
    
    parseSitemap(resource.read(), user, password)
    
    

if __name__ == '__main__':
    
    arg_len = len(sys.argv)

    if arg_len < 2:
        print "No url defined"
        print "Usage: python sitemap-check.py url [username] [password]"
    else:
        
        # get list of check functions
        function_pattern = re.compile('^checkElement.+$')
        check_functions = { f:getattr(sys.modules[__name__], f) for f in dir(sys.modules[__name__]) if function_pattern.search(f) }
        
        if arg_len == 2:
            loadSitemap(sys.argv[1])
        elif arg_len == 3:
            print "No password defined"
        elif arg_len == 4:
            loadSitemap(sys.argv[1], sys.argv[2], sys.argv[3])
