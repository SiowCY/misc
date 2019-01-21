import socket, subprocess, os, struct, csv, json, sys, argparse, sqlite3, multiprocessing, scapy
import urllib3, ssl, _thread, requests, time, threading, binascii, xml, collections, re
import xml.etree.ElementTree as et
from lxml import etree

# urliib require to import one by one
import urllib.request
import urllib.parse
import urllib.error

#####  SSL Self Sign Error Solution  #####
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

#####                               #####

class Class1():

    # __init__ is special method for Python that will run automatically as default method in Class
    # init_var1 and init_var2 is a must input
    # init_var3 is optional
    # init_var4 is default
    def __init__(self, init_var1, init_var2, init_var3="", init_var4="4th default value at object"):
        self.init_var1 = init_var1
        self.init_var2 = init_var2
        self.init_var3 = init_var3
        self.init_var4 = init_var4
        # init_var5 is default value
        self.init_var5 = "Self declare 5th default value inside function"

    # Every function declare with class is a method
    def method1(self):
        # With title format
        print("Passing the Class Variable 1 at Function Method 1: " + self.init_var1.title())

    def method2(self):
        # Convert int to str = str(int)
        # Convert str to int = int(str)
        total = int(self.init_var1) + self.init_var2
        print("Convertion between string and interger: " + str(total) + " = " + self.init_var1 + " + " + str(self.init_var2))

    def method3(self):
        # Return a neatly formatted descriptive name with lower and upper case
        combine_var1_var2 = str(self.init_var1) + self.init_var2.upper() + " " + self.init_var3.lower()
        return combine_var1_var2

    def method4(self):
        # Print default value
        print("Welcome to forth function with default value: " + self.init_var4 + " and " + self.init_var5)

    def method5(self):
        # Change default value
        print("Changing the default value: " + self.init_var4 + " and " + self.init_var5)

    def method6(self, update_var5):
        # Changing 5th var value if else case
        if len(update_var5) > len(self.init_var5):
            self.init_var5 = update_var5
            print( "Successful changed: " + self.init_var5 )
        else:
            print ("Sorry, you can't change 5th variable! Unchanged: " + self.init_var5)

class Class_independent():
    # Instances as Attributes
    def __init___(self, init_var1):
        self.init_var1 = init_var1

    def ind_method(self):
        print("Independent Class Found!")

class Class2_child(Class1):
    def __init__(self, init_var1, init_var2, init_var3=""):
        # super function is a special function to help connect parent and child
        super().__init__(init_var1, init_var2, init_var3)

        # Calling the indepent class without parent
        self.ind_class = Class_independent()

    # Create child own attribute and method
    def child_method1(self, child_attr):
        self.child_attr1 = child_attr
        print(self.child_attr1)

class list_c():
    def __init__(self, item_1, item_2, item_3, item_4):
        self.item_1 = item_1
        self.item_2 = item_2
        self.item_3 = item_3
        self.item_4 = item_4
      #  self.item_5 = None

    def list_m1(self):
        print("\n[+] Inside Listing Function\n")
        create_list = [self.item_1, self.item_2, self.item_3, self.item_4]
        #print (any(item is None for item in create_list))
        print("First item in list: " + create_list[0])
        print("Second item in list: " + create_list[1])
        print("Third item in list: " + create_list[2])
        print("Forth item in list: " + create_list[3])

        pop_item = create_list.pop()
        print("Pop the last item on the list: " + pop_item)

        create_list.append("Item 5")
        print(create_list)
        # Failed to sort and reverse
        print("Sorting as below: ")
        print(sorted(create_list))
        create_list.reverse()
        print("Reverse as below: ")
        print(create_list)

class dict_c1():
    def __init__(self):
        pass

    def dict_m1(self, key_1, value_1, value_2):
        print("\n[+] Inside dictionary function\n")
        self.key_1 = key_1
        self.value_1 = value_1
        self.value_2 = value_2
        dict1 = {self.key_1: [self.value_1, self.value_2]}
        print(dict1.keys())
        print(dict1.values())

    def nest_dict(self):
        print("\n[+] Inside nesting dictionary function\n")
        nestA = {'birds' : ['eagle','owl','falcon'],'speed' : 'fast', 'genre' : 'hunt'}
        nestB = {'birds' : ['parrot','parrow','pigeon'], 'speed' : 'normal', 'genre' : 'kind'}
        nestC = {'birds' : ['chicken','duck'], 'speed' : 'slow', 'genre' : 'pet'}

        nest_all = [nestA, nestB, nestC]

        for bird in nest_all:
            print(bird)

# Normal Function
def user_input():
    print("\n[+] Inside normal user input function\n")
    name = input("Please insert your name: ")
    print("Hello, " + name + ". Welcome to Python 101!\n")

def looping_input():
    print("\n[+] Inside looping!\n")
    name = ""
    while name != 'quit':
        name = input( "Please insert your name: " )
        if name == 'quit':
            print("Quiting...")
        else:
            print( "Hello, " + name + ". Welcome to Python 101!\n" )

def flag_input():
        print("\n[+] Inside flag looping!\n")
        name = ""
        active = True
        while active:
            name = input( "Please insert your name: " )
            # Use break
            if name == 'break':
                print("Used break to end while loop.")
                break
            elif name == 'quit':
                print("Quiting...")
                active = False
            else:
                print( "Hello, " + name + ". Welcome to Python 101!\n" )

def filling_dict():
    print("\n[+] Inside filling dictionary.\n")
    # Declare blank dictionary
    responses = {}
    # Active True
    active = True
    while active:
        name = input( "Please insert your name: " )
        response = input("Where do you want to go this summer? ")

        # Store the response into dictionary
        # dict[keys] = values
        responses[name] = response

        # Looping to more responses
        looping = True
        while looping:
            repeat = input("Anyone wants to respond? (y/n)")
            if repeat == 'y':
               break
            elif repeat == 'n':
                active = False
                looping = False
            else:
                print("Please reponse using 'y' or 'n'.")

    print("\n=== Final Results ===")
    # for key, value in dictionary.items()
    for name, response in responses.items():
        print(name + " will go to " + response + " in this summer.")

def read_file():
    print ("\n[+] Inside read file function\n")
    with open('readme.txt') as rfile:
        full_read = rfile.read()
        print("Full read contents.")
        print(full_read)

    with open( 'readme.txt' ) as rfile:
        for rline in rfile.readlines():
            print("Read line by line.")
            print("Current line: " + rline)

    with open('readme.txt') as rfile:
        for rline in rfile.readlines():
            rline = rline.rstrip()
            print ("Read line by line with rstrip.")
            print("Current line: " + rline)

    with open('readme.txt') as rfile:
        for rline in rfile.readlines():
            rline = rline.strip('\n')
            print ("Read line by line with strip('\\n').")
            print ("Current line: " + rline)

    with open('writeme.txt','w') as wfile:
        print("Start to write to file!")
        wfile.write("I love to write file.\n")
        wfile.write("I love to write 2 lines.\n")
    with open('writeme.txt') as rfile:
        read_all = rfile.read()
        print (read_all)

def exception_file():
    print ("\n[+] Inside exception function\n")
    try:
        with open('readno.txt') as rfile:
            rlines = rfile.read()
            print(rlines)
    except:
        print("File not found!")

def server_socket():
    host = None
    port = 1337
    s = None
    print ("\n[+] Inside server socket function\n")
    for server_info in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print("Failed to open socket.")
    conn, addr = s.accept()
    with conn:
        print("Successfully connected!")

class lib_socket():

    def __init__(self):
        pass

    def nonssl(self):
        # Set default timeout duration 5 seconds
        socket.setdefaulttimeout( 5 )
        print( "\n[+] Using socket without ssl:\n" )
        # Create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Declare host and port
        target = "google.com"
        port = 80
        # Get address info
        t_info = socket.getaddrinfo(target, port, 0, 0, socket.IPPROTO_TCP)
        print ("Target info: ")
        print (t_info)
        print ("Target IP addr: " + t_info[0][4][0])
        #
        ip_addr = t_info[0][4][0]
        s.connect((ip_addr,port))
        # In python 2, s.send('GET / HTTP/1.0\r\n')
        # In python 3, data has to be send using byte array
        s.send(b'GET / HTTP/1.0\r\n\r\n')
        resp = s.recv(1024)

        print(resp.decode( "utf8" ))

    def sslr(self):
        # Set default timeout duration 5 seconds
        socket.setdefaulttimeout( 5 )
        print("\n[+] Using socket with ssl:\n")
        context = ssl.create_default_context()
        target = "youtube.com"
        port = 443
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_s = context.wrap_socket(s, server_hostname = target)
        ssl_s.connect((target,port))
        ssl_s.send(b'GET / HTTP/1.0\r\n\r\n')
        resp = ssl_s.recv( 1024 )
        print( resp.decode( "utf8" ) )

class web_urllib():
    def __init__(self):
        pass
    def send_req(self):
        print("\n[+] Visit website using urllib: ")
        url = 'https://www.google.com'
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)

        print("Response: " + str(resp.code))

        print("Response headears:")
        for key, value in resp.headers.items():
            print(key + " : " + value)

        # Custom headers
        ua = 'Random UA Value'
        headers = {'User-Agent' : ua}
        req_h = urllib.request.Request(url, headers)

        # Exception
        url_f = 'https://www.google.com/failed'
        req_f = urllib.request.Request(url_f)
        try:
            resp = urllib.request.urlopen(req_f)
        except urllib.error.HTTPError as e:
            print("HTTP Error code: " + str(e.code))
            print("HTML Error: " + str(e.read()))
        except urllib.error.URLError as e:
            print("URL Error of reaching: " + str(e.reason))

    def post_req(self):
        scontext = ssl.SSLContext( ssl.PROTOCOL_TLSv1 )
        print("\n[+] Post request using urllib: \n")
        url = 'https://www.base64decode.org/'
        values = {'input': 'cHl0aG9uIHVybGxpYg==', 'decode': 'decode', 'charset': 'UTF-8'}
        data = urllib.parse.urlencode( values )
        data = data.encode( 'ascii' )
        req3 = urllib.request.Request( url, data)
        resp = urllib.request.urlopen( req3, context=scontext )
        print("Post Request Response HTML: ")
        print(resp.read()[0:50])

class web_urllib3():
    def __init__(self):
        pass
    def send_req(self):
        urllib3.disable_warnings()  # Disable SSL Warning
        print("\n[+] Visit website using urllib3: \n")
        url = 'https://www.google.com'
        http = urllib3.PoolManager() #Default maximum of 10 ConnectionPool (10 hosts)
        req = http.request('GET', url, preload_content=False) #preload_content to stream the response content
        print("Response from urllib3: ")
        print(req.read(32))
        # Proxy
        # proxy = urllib3.ProxyManager('http://proxy.localhost.com:8008')
        # proxy.request('GET', url, preload_content=False)
        # Response Code
        print("HTTP Response Stauts Code: " + str(req.status))
        # Resposnse Headers
        for key, value in req.headers.items():
            print(key + " : " + value)
        # Custom Header request
        req.release_conn() # To release the http connection due to preload_content = False then you can reuse the Pool
        req_h = http.request('GET', url, headers={'Random Headers' : 'Random Value'}, preload_content=False)
        req_h.release_conn()

    def post_req(self):
        pass
        # Post method for urllib wih query parameter can use urllib

class web_request():
    def __init__(self):
        pass
    def send_req_ssl(self):
        print("\n[+] Visit website using requests: \n")
        url = 'https://www.google.com'
        req = requests.get(url, verify=False) # Use verify = False to ignore SSL Error
        resp_code = req.status_code
        print("HTTP Response Code:" + str(resp_code))
        headers = req.headers
        print("Headers information: ")
        for key, value in headers.items():
            print(key + " : " + value)
        print("First 50 strings response in HTML: ")
        resp_html = req.text
        print(resp_html[0:50])
        # Custom Header
        r_headers = {'user-agent' : 'Requests Custom Header Sample/0.0.1'}
        req = requests.get(url, headers=r_headers, verify=False)
        # Proxies
        # proxy = {'http' : 'http://proxy.localhost.com:8080', 'https' : 'https://proxy.localhost.com:8083'}
        #req = requests.get( url, headers=r_headers, proxies=proxy )

    def post_req(self):
        print("\n[+] Post request using requests: \n")
        url = 'https://www.base64decode.org/'
        r_headers = {'Cookie': '_ga=GA1.2.689099105.1532255640; _gid=GA1.2.422439299.1532255641; _gat=1'}
        values = {'input': 'cHl0aG9uIHJlcXVlc3Rz', 'decode': 'decode', 'charset': 'UTF-8'}
        req = requests.post(url, headers=r_headers, data=values)
        print( "Post Request Response HTML: " )
        print( req.text[0:50])

class open_subprocess():
    def __init__(self):
        pass

    def subproc(self):
        print("\n[+] Inside subprocess function \n")
        new_proc = subprocess.Popen(['dir'],shell=True,stdout=subprocess.PIPE)
        byte_proc = new_proc.stdout.read()
        string_proc = byte_proc.decode('utf-8')
        for dirlist in string_proc.strip().split('\r\n'):
            print (dirlist)


class multiprocessing_():
    def __init__(self):
        pass

    def visit(self, url):
        req = requests.get( url, verify=False )
        print( "Visited Website: " + url )

    def more_process(self):
        print("\n[+] Inside multi processing function\n")
        start = time.time()
        processes = []
        urls = [
            'http://www.google.com',
            'http://www.youtube.com',
            'http://www.facebook.com',
            'http://github.com',
            'http://twitter.net',
            'http://outlook.live.com']
        for url in urls:
            p = multiprocessing.Process(target=self.visit( url ))
            processes.append(p)
            p.start()
            print("PID: ", p.pid)
            p.terminate()
        end = time.time()
        duration = end - start
        print( "Total time used for visit with multiprocessing: " + str( duration ) )


class multithreading_():

    def __init__(self):
        pass
    def visit(self, url):
        req = requests.get(url, verify=False)
        print("Visited Website: " + url)
    def no_threading(self):
        print("\n[+] Inside multithreading function\n")
        print( "===== No Threading =====" )
        start = time.time()
        urls = [
            'http://www.google.com',
            'http://www.youtube.com',
            'http://www.facebook.com',
            'http://github.com',
            'http://twitter.net',
            'http://outlook.live.com']
        for url in urls:
            self.visit(url)
        end = time.time()
        duration = end - start
        print("Total time used to visit without threading: " + str(duration))
    def with_threading(self):
        print("===== Threading =====")
        start = time.time()
        THREADS = []
        urls = [
            'http://www.google.com',
            'http://www.youtube.com',
            'http://www.facebook.com',
            'http://github.com',
            'http://twitter.net',
            'http://outlook.live.com']
        for url in urls:
            print( "Start worker threading" )
            wthread = threading.Thread( target=self.visit, args=(url,) )
            THREADS.append(wthread)
            wthread.start()
        end = time.time()
        duration = end - start
        print( "Total time used to visit with threading: " + str( duration ) )

def pyxml():
    print("\n[+] Inside xml.etree.ElementTree\n")
    t = et.parse( 'pyxml.xml' )
    root = t.getroot()
    print( "This is root: " + root.tag )
    for child in root:
        print( "Getting the attribute:" )
        for key, value in child.attrib.items():
            print( key + " " + value )
        print( "This is child tag: " + child.tag )
        # Using get method
        print( "This is child get: " + child.get( 'iamtag' ) )

    # Using findall method
    for thisischild in root.findall( 'thisischild' ):
        # Using find method and text
        findme = thisischild.find( 'findme' ).text
        gethis = thisischild.get( 'iamtag' )
        print( "Inside findall loop" )
        print( "This is findme: " + findme )
        print( "This is getthis: " + gethis )
        # Some tag is not available will mark as None
        try:
            ifnone = thisischild.find( 'ifnone' ).text
            if ifnone != None:
                print( ifnone )
        except:
            print( "No ifnone child" )
        try:
            weird_me = thisischild.find( 'weird_me' ).get( 'name' )
            if weird_me != None:
                print( weird_me )
        except:
            print( "No weird_me child" )

    # Using iter method
    for iter_me in root.iter( 'iter_me' ):
        for key, value in iter_me.attrib.items():
            print( "Inside iter_me: Key= " + key + "\tValue= " + value )

    for iter_you in root.iter( 'iter_you' ):
        for key, value in iter_you.attrib.items():
            print( "Inside iter_you: Key= " + key + "\tValue= " + value )

    print( "" )
    # Using listing format
    print( "This is root[0].tag= " + root[0].tag )
    print( "This is root[0].attrib from " + root[0].tag )
    for key, value in root[0].attrib.items():
        print( "Key: " + key + "\tValue: " + value )
    print( "This is root[0][0].tag= " + root[0][0].tag )
    print( "This is root[0][0].text= " + root[0][0].text )
    print( "This is root[0][1].tag= " + root[0][1].tag )
    print( "This is root[0][1].attrib from " + root[0][1].tag )
    for key, value in root[0][1].attrib.items():
        print( "Key: " + key + "\tValue: " + value )
    print( "This is root[0][2].tag= " + root[0][2].tag )
    print( "This is root[0][2][0].tag= " + root[0][2][0].tag )
    print( "This is root[0][2][0].text= " + root[0][2][0].text )
    print( "This is root[0][2][1].tag= " + root[0][2][1].tag )
    print( "This is root[0][2][1].attrib from " + root[0][2][1].tag )
    for key, value in root[0][2][1].attrib.items():
        print( "Key: " + key + "\tValue: " + value )

def pylxml():
    print("\n[+] Inside lxml etree view by tree list\n")
    xmlfile = open( 'pyxml.xml', 'r' )
    read_xml = xmlfile.read()
    xml_root = etree.fromstring( read_xml )
    raw_tree = etree.ElementTree( xml_root )
    nice_tree = collections.OrderedDict()

    for tag in xml_root.iter():
        path = re.sub( '\[[0-9]+\]', '', raw_tree.getpath( tag ) )
        if path not in nice_tree:
            nice_tree[path] = []
        if len( tag.keys() ) > 0:
            nice_tree[path].extend( attrib for attrib in tag.keys() if attrib not in nice_tree[path] )

    for path, attribs in nice_tree.items():
        indent = int( path.count( '/' ) - 1 )
        print( '{0}{1}: {2} [{3}]'.format( '    ' * indent, indent, path.split( '/' )[-1],
                                           ', '.join( attribs ) if len( attribs ) > 0 else '-' ) )

# Testing on Class1 #
print("[+] Inside class function")
my_class = Class1("this is 1", 1)
print(my_class.method1())

my2_class = Class1('2', 2)
print(my2_class.method2())

my3_class = Class1(3, ") this is return function", "AND THE THIRD VARIABLE!")
print(my3_class.method3())

my4_class = Class1("Unuse var1", "Unuse var2")
my4_class.method4()

my5_class = Class1("Unuse var1", "Unuse var2", init_var4="Change 4th value!")
my5_class.init_var5 = "Changed 5th value!"
my5_class.method5()

my6_class = Class1("Unuse var1", "Unuse var2")
my6_class.method6("Changed 5th variable!")

# Testing on Class2_child
my_class2 = Class2_child(3,") I AM LOWER CASE CHILD CLASSS","I AM UPPER CASE CHILD CLASS ")
print(my_class2.method3())

my2_class2 = Class2_child("Unuse var1", "Unuse var2")
my2_class2.child_method1("Child Self Attr 1")

# Calling independent class method
my_ind_class = Class2_child("Unuse var1", "Unuse var2")
my_ind_class.ind_class.ind_method()

# Listing
my_list = list_c("Item 3", "Item 4", "Item 1", "Item 2")
my_list.list_m1()

# Dictionary
print("\n")
my_dict = dict_c1()
# Dictionary key and value
my_dict.dict_m1("KEY1", "VALUE1", "VALUE2")
# Nesting all dictionaries to one
print("\nCombine multiple dictionaries:")
my_dict.nest_dict()

# Declare function and user input
user_input()
# Looping wait insert quit to quit
looping_input()
# Quit using flag
flag_input()
# Filling dictionary
filling_dict()

# Read file
read_file()

# Exceptional handling
exception_file()

# Using socket library
s = lib_socket()
nonssl = s.nonssl()
ssl_s = s.sslr()
time.sleep(2)

# Using urllib library
u1 = web_urllib()
u1.send_req()
u1.post_req()
time.sleep(2)

# Using urllib3 library
u3 = web_urllib3()
u3.send_req()
time.sleep(2)

# Using requests library
r = web_request()
r.send_req_ssl()
r.post_req()
time.sleep(2)

# Process creation
sp = open_subprocess()
sp.subproc()
time.sleep(2)

# Multiprocessing
p = multiprocessing_()
p.more_process()
time.sleep(2)

# Threading
t = multithreading_()
t.no_threading()
t.with_threading()
time.sleep(2)

# XML parsing
pyxml()

# XML using lxml tree list
pylxml()

# Hex, Decimal and Ascii conversion
Hex2ascII = "41".decode("hex")
Ascii2heX = hex(65)
Decimal2ascII = chr(65)
Ascii2decimaL = int("A")
