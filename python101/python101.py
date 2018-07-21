import socket, subprocess, os, struct, csv, json, sys, argparse, sqlite3, urllib, multiprocessing, scapy
import urllib3, ssl, _thread, requests, time, threading
import xml.etree.ElementTree as ET

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
        self.key_1 = key_1
        self.value_1 = value_1
        self.value_2 = value_2
        dict1 = {self.key_1: [self.value_1, self.value_2]}
        print(dict1.keys())
        print(dict1.values())

    def nest_dict(self):
        nestA = {'birds' : ['eagle','owl','falcon'],'speed' : 'fast', 'genre' : 'hunt'}
        nestB = {'birds' : ['parrot','parrow','pigeon'], 'speed' : 'normal', 'genre' : 'kind'}
        nestC = {'birds' : ['chicken','duck'], 'speed' : 'slow', 'genre' : 'pet'}

        nest_all = [nestA, nestB, nestC]

        for bird in nest_all:
            print(bird)

# Normal Function
def user_input():
    name = input("Please insert your name: ")
    print("Hello, " + name + ". Welcome to Python 101!\n")

def looping_input():
    print("Inside looping!")
    name = ""
    while name != 'quit':
        name = input( "Please insert your name: " )
        if name == 'quit':
            print("Quiting...")
        else:
            print( "Hello, " + name + ". Welcome to Python 101!\n" )

def flag_input():
        print("Inside flag looping!")
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
    print("Inside filling dictionary.")
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
        print( "\nUsing socket without ssl:\n" )
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
        print("\nUsing socket with ssl:\n")
        context = ssl.create_default_context()
        target = "youtube.com"
        port = 443
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_s = context.wrap_socket(s, server_hostname = target)
        ssl_s.connect((target,port))
        ssl_s.send(b'GET / HTTP/1.0\r\n\r\n')
        resp = ssl_s.recv( 1024 )
        print( resp.decode( "utf8" ) )

class multithreading_():

    def __init__(self):
        pass
    def visit(self, url):
        req = requests.get(url)
        print("Visited Website: " + url)
    def no_threading(self):
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


# Testing on Class1 #
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

# Process creation


# Threading
t = multithreading_()
t.no_threading()
t.with_threading()
