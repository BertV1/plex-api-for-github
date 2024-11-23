import urllib.parse
import os
import xml.etree.ElementTree as ET


#################
#################
##             ##
## |  | |\ |   ##
## |  | |/ |   ##
## |__| |\ |__ ##
##             ##
#################
#################

def write_xml(content_blob,filename):
    with open(filename+'.xml', 'wb') as f:
        f.write(content_blob)

def url_encode(str_elem):
    return urllib.parse.quote(str_elem)

def create_url(str_host,str_http_type,int_port):
    if create_url.__code__.co_argcount != 3:
        exit(0)
        print("This function requires 3 arguments.")
    try:
        str(int_port)
    except:
        exit(0)
        print("The port should be a number.")
    str_url = str_http_type+"://"+str_host+":"+str(int_port)+"/"
    return str_url
    

def add_args(str_url,tuples_args):
    url_arg=""
    for arg in tuples_args:
        if len(url_arg) == 0:
            url_arg+="?"+arg[0]+"="+url_encode(arg[1])
        else:
            url_arg+="&"+arg[0]+"="+url_encode(arg[1])
    str_url+= url_arg
    return str_url

############################
############################
##                        ##
## \        / |\ | -+- +- ##
##  \  /\  /  |/ |  |  +- ##
##   \/  \/   |\ |  |  +- ##
##                        ##
############################
############################

def get_write_dir():
    write_dir = os.path.expanduser("~")
    return write_dir

def write_xml(content_blob,filename):
    write_dir = get_write_dir()
    f_2_w = write_dir+"\\"+filename
    with open(f_2_w, 'wb') as f:
        f.write(content_blob)



####################
####################
##                ##
## \ / |\  /| |   ##
##  x  | \/ | |   ##
## / \ |    | |__ ##
##                ##
####################
####################

# retruns tuple list of lib name and key
def getLibsFromXmL(f_plex_libs):
    plex_libs = ET.parse(f_plex_libs)
    xml_root = plex_libs.getroot()    
    # key, title 
    lst_res = []
    for item in xml_root.findall('./Directory'):
        lst_res.append((item.attrib['key'], item.attrib['title']))
    return lst_res

def check_xml_existence(f_name):
    # TODO: chg path to root of user
    f_path = get_write_dir()+"\\"+f_name
    print(f_path)
    if os.path.isfile(f_path):
        return True
    else:
        False


##########################
##########################
##                      ##
## / | |  /\ \        / ##
## \ +-+ |  | \  /\  /  ##
## / | |  \/   \/  \/   ##
##                      ##
##########################
##########################

def show_help():
    help_string ="""
    PLEX SCRIPTOR: python script.py [args]\n
    \n -h\t get this help menu. If no args are supplied, also shows this help menu.
    \n -s\t get server settings, stored in xml file
    \n -l\t get libraries, stored in xml file, and show them.
    \n -l key\t get content of a library, identified by key. Key must be a valid library key. Requires -l to have been executed at least once.
    \n XML files are stored in user home.
    """
    print(help_string)
    exit(0)

def show_libraries(fname):
    fpath = get_write_dir() + "\\" + fname
    lst_libs = getLibsFromXmL(fpath)
    tup_for_tup = ['Key: %s --> Name: %s\n' % tup for tup in lst_libs]
    str_tup_for_tup = ', '.join(tup_for_tup).replace(',','')
    print(
    """
    AVAILABLE LIBRARIES:\n\n {}
    """.format(str_tup_for_tup)
    )

