import urllib.parse
import os
import requests
import time
import xml.etree.ElementTree as ET

STATIC_FILES = {
    'SERVER_SETTINGS':'plex_server_settings.xml',
    'LIBRARIES':'plex_library_list.xml',
    'LIB_CONTENT':'plex_lib_content.xml',
    'COLLECTIONS':'plex_collections.xml',
    'COLLECTION':'plex_coll_content.xml'
}
    
def get_epochtime():
    return int(time.time())


#################
#################
##             ##
## |  | |\ |   ##
## |  | |/ |   ##
## |__| |\ |__ ##
##             ##
#################
#################

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

def create_url_args(lst_url_args):
    if not lst_url_args:
        return ""
    
    url_args=""
    for arg in lst_url_args:
        if len(url_args) == 0:
            url_args+="?"+arg[0]+"="+url_encode(arg[1])
        else:
            url_args+="&"+arg[0]+"="+url_encode(arg[1])
    return url_args

def create_base_url_parts(lst_base_url_parts):
    if not lst_base_url_parts:
        return ""
    
    url_parts = ""
    for url_part in lst_base_url_parts:
        if len(url_parts) == 0:
            url_parts += url_part
        else:
            url_parts += "/" + url_part
    return url_parts


# !!!!!!!!!!!!!!!!!!!!!! BASE URL ALWAYS ENDS WITH A FWD SLASH !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!! FIRST LIST ELEM IS ALWAYS PARTS       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!! SECOND LIST ELEM IS ALWAYS ARGS       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def build_request_url_elems(lst_args):
    # lst_base_url_parts, lst_url_args
    str_url_parts = create_base_url_parts(lst_args[0])
    str_url_args = create_url_args(lst_args[1])
    
    url = str_url_parts + str_url_args
    return url
    

######################
######################
##                  ##
## \        / +- |> ##
##  \  /\  /  +- |\ ##
##   \/  \/   +- |/ ##
##                  ##
######################
######################
    
def make_request(str_req_url):
    print(str_req_url)
    req_resp = requests.get(str_req_url, verify=False)
    return req_resp.content

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
# expects xml file with libs
# TODO: maybe merge colls/lib key funcs
def getLibsFromXmL(f_plex_libs):
    f_plex_libs = get_write_dir()+"\\"+f_plex_libs
    plex_libs = ET.parse(f_plex_libs)
    xml_root = plex_libs.getroot()    
    # key, title 
    lst_res = []
    for item in xml_root.findall('./Directory'):
        lst_res.append((item.attrib['key'], item.attrib['title']))
    return lst_res

def getCollectionsFromXmL(f_plex_colls):
    f_plex_colls = get_write_dir()+"\\"+f_plex_colls
    plex_colls = ET.parse(f_plex_colls)
    xml_root = plex_colls.getroot()
    # key, title 
    lst_res = []
    for item in xml_root.findall('./Directory'):
        lst_res.append((item.attrib['ratingKey'],item.attrib['title']))
    return lst_res

# TODO: account for absence of properties
def getCollectionContentFromXmL(f_plex_coll_content):
    f_plex_coll_content = get_write_dir()+"\\"+f_plex_coll_content
    plex_coll_content = ET.parse(f_plex_coll_content)
    xml_root = plex_coll_content.getroot()
    lst_res = []
    x = 0
    for item in xml_root.findall('./Video'):
        try:
            lst_res.append((item.attrib['ratingKey'],item.attrib['title'],item.attrib['originallyAvailableAt']))
        except KeyError:
            print("woops, didn't find some items...")
            lst_res.append(("kak","kak","kak"))
            pass
    return lst_res
    

def check_xml_existence(f_name):
    # TODO: chg path to root of user
    f_path = get_write_dir()+"\\"+f_name
    print(f_path)
    if os.path.isfile(f_path):
        return True
    else:
        False

def lib_key_exists(lib_key):
    if check_xml_existence(STATIC_FILES['LIBRARIES']):
        return lib_key in list(zip(*getLibsFromXmL(STATIC_FILES['LIBRARIES'])))[0]

def coll_key_exists(coll_key):
    if check_xml_existence(STATIC_FILES['COLLECTIONS']):
        return coll_key in list(zip(*getCollectionsFromXmL(STATIC_FILES['COLLECTIONS'])))[0]
    


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
    \n -h\t\t get this help menu. If no args are supplied, also shows this help menu.
    \n -s\t\t get server settings, stored in xml file
    \n -l\t\t get libraries, stored in xml file, and show them.
    \n -l lib_key\t get content of a library, identified by key. Key must be a valid library key. Requires -l to have been executed at least once.
    \n -m film_key\t get film properties by film_key, stored in xml file. Returns NO if film is not found.
    \n -c lib_key\t get all collections of a library, stored in xml file, and show them. Key: see -l.
    \n -c lib_key coll_key get content of a collection identified by coll_key, located in library identified by lib_key.
    \n XML files are stored in user home.
    """
    print(help_string)
    exit(0)

def prepTups(lst_tups):
    tup_for_tup = ['Key: %s --> Name: %s\n' % tup for tup in lst_tups]
    str_tup_for_tup = ', '.join(tup_for_tup).replace(',','')
    return str_tup_for_tup

def show_libraries(fname):
    lst_libs = getLibsFromXmL(fname)
    str_tup_for_tup = prepTups(lst_libs) 
    print(
    """
    AVAILABLE LIBRARIES:\n\n {}
    """.format(str_tup_for_tup)
    )

def show_collections(fname):
    lst_collections = getCollectionsFromXmL(fname)
    str_tup_for_tup = prepTups(lst_collections)
    print(
    """
    COLLECTIONS in this LIBRARY:\n\n {}
    """.format(str_tup_for_tup)
    )

def show_collection_content(fname):
    lst_coll_content = getCollectionContentFromXmL(fname)
    tup_for_tup = ['Key: %s --> Name: %s ---> Released: %s\n' % tup for tup in lst_coll_content]
    str_tup_for_tup = ', '.join(tup_for_tup).replace(',','')
    print(
    """
    FILMS in this COLLECTION:\n\n {}
    """.format(str_tup_for_tup)
    )


