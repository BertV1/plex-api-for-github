import requests
import ssl
import helper_funcs as help
import os
import sys
ssl.SSLContext.verify_mode == ssl.VerifyMode.CERT_OPTIONAL

plex_token=""
plex_url=["","",32400]
plex_token = [["X-Plex-Token",plex_token]]

STATIC_FILES = {
    'SERVER_SETTINGS':'plex_server_settings.xml',
    'LIBRARIES':'plex_library_list.xml',
    'LIB_CONTENT':'plex_lib_content.xml'
    }
# base URL, usually does not change.

def get_server_settings(str_base_url,lst_token):
    print(str_base_url)
    req_url = help.add_args(str_base_url,lst_token)
    print(req_url)
    req_resp = requests.get(req_url, verify=False)
    help.write_xml(req_resp.content,STATIC_FILES['SERVER_SETTINGS'])
    exit(0)

def get_libraries(str_base_url,lst_token):
    bool_lib_file_exists = help.check_xml_existence(STATIC_FILES['LIBRARIES'])
    if not bool_lib_file_exists:
        str_base_url += "library/sections"
        print(str_base_url)
        req_url = help.add_args(str_base_url,lst_token)
        print(req_url)
        req_resp = requests.get(req_url, verify=False)
        help.write_xml(req_resp.content,STATIC_FILES['LIBRARIES'])
    help.show_libraries(STATIC_FILES['LIBRARIES'])

def get_library_content(str_base_url,lst_token,lib_key):
    # TODO: implement
    if not help.check_xml_existence(STATIC_FILES['LIBRARIES']):
        exit(0)
    fpath = help.get_write_dir() + "\\" + STATIC_FILES['LIBRARIES']
    lst_libs = help.getLibsFromXmL(fpath)
    for tup in lst_libs:
        if str(lib_key) == tup[0]:
            print("OK")
            str_base_url += "library/sections/"+lib_key+"/all"
            req_url = help.add_args(str_base_url,lst_token)
            print(req_url)
            req_resp = requests.get(req_url,verify=False)
            help.write_xml(req_resp.content,STATIC_FILES['LIB_CONTENT'])
            
STATIC_ARGS = ['-h','-s','-l']
if __name__ == "__main__":
    # sth akin to init_conn
    base_url = help.create_url(plex_url[1],plex_url[0],plex_url[2])

    if len(sys.argv) == 1:
        help.show_help()
    if len(sys.argv) == 2:
        if sys.argv[1] in STATIC_ARGS:
            if sys.argv[1] == '-h':
                help.show_help()
            if sys.argv[1] == '-s':
                get_server_settings(base_url,plex_token)
            if sys.argv[1] == '-l':
                get_libraries(base_url,plex_token)
                exit(0)
    if len(sys.argv) == 3 and sys.argv[1] == '-l' and sys.argv[2].isdigit():
        get_library_content(base_url,plex_token,sys.argv[2])
    else:
        help.show_help()
            
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    