import requests
import ssl
import helper_funcs as help
import helper_creds as creds
import os
import sys

ssl.SSLContext.verify_mode == ssl.VerifyMode.CERT_OPTIONAL

plex_token_instance=creds.get_plex_token()
plex_url=[creds.get_plex_url()[0],creds.get_plex_url()[1],32400]
plex_token = [["X-Plex-Token",plex_token_instance]]

# TODO: rewrite this so that we can create dynamic filenames,
# eg: 'libraries':['plex_lib_list','.xml']
STATIC_FILES = {
    'SERVER_SETTINGS':'plex_server_settings.xml',
    'LIBRARIES':'plex_library_list.xml',
    'LIB_CONTENT':'plex_lib_content.xml',
    'COLLECTIONS':'plex_collections.xml'
    }
# base URL, usually does not change.

def get_server_settings_new(str_base_url,lst_token):
    
    if help.check_xml_existence(STATIC_FILES['SERVER_SETTINGS']):
        print("file already exists")
        exit(0)
    url_elems = ['',lst_token]
    
    req_url = str_base_url + help.build_request_url_elems(url_elems)
    req_resp = help.make_request(req_url)
    help.write_xml(req_resp,STATIC_FILES['SERVER_SETTINGS'])
    exit(0)
    
    
def get_libraries_new(str_base_url,lst_token):
    
    if help.check_xml_existence(STATIC_FILES['LIBRARIES']):
        help.show_libraries(STATIC_FILES['LIBRARIES'])
        exit(0)
    
    url_elems = [["library","sections"],lst_token]
    req_url = str_base_url + help.build_request_url_elems(url_elems)
    req_resp = help.make_request(req_url)
    
    help.write_xml(req_resp,STATIC_FILES['LIBRARIES'])
    help.show_libraries(STATIC_FILES['LIBRARIES'])


# TODO: dynamic filename based on libkey
def get_library_content_new(str_base_url,lst_token,lib_key):
    if help.check_xml_existence(STATIC_FILES['LIB_CONTENT']):
        print("file already exists.")
        exit(0)
    
    url_elems = [["library","sections",lib_key,"all"],lst_token]
    req_url = str_base_url + help.build_request_url_elems(url_elems)
    req_resp = help.make_request(req_url)
    
    help.write_xml(req_resp,STATIC_FILES['LIB_CONTENT'])
    
    
def get_collections_new(str_base_url,lst_token,lib_key):
    
    if help.check_xml_existence(STATIC_FILES['COLLECTIONS']):
        help.show_collections(STATIC_FILES['COLLECTIONS'])
        exit(0)
    
    url_elems = [["library","sections",lib_key,"collections"],lst_token]
    req_url = str_base_url + help.build_request_url_elems(url_elems)
    req_resp = help.make_request(req_url)
    
    help.write_xml(req_resp,STATIC_FILES['COLLECTIONS'])
    help.show_collections(STATIC_FILES['COLLECTIONS'])

def get_collection_content(str_base_url,lst_token,lib_key,str_collection_name):
    print("yes, you are COLLECTING THE COLLECTION for {}.".format(str_collection_name))
    # https://192.168.0.33:32400/library/sections/1/all?collection=3441&X-Plex-Token=XXX
    # str_base_url +=
    



def get_film(str_base_url,lst_token):
    return -1
    
            
STATIC_ARGS = ['-c','-h','-s','-l','-m']
if __name__ == "__main__":
    # sth akin to init_conn
    base_url = help.create_url(plex_url[1],plex_url[0],plex_url[2])
    
    lst_args = sys.argv
    arg_count = len(sys.argv)

    if arg_count == 1:
        help.show_help()
    if arg_count == 2:
        if lst_args[1] in STATIC_ARGS:
            if lst_args[1] == '-h' or lst_args[1] == '-m':
                help.show_help()
            if lst_args[1] == '-s':
                get_server_settings_new(base_url,plex_token)
            if lst_args[1] == '-l':
                get_libraries_new(base_url,plex_token)
                exit(0)
    if arg_count == 3:
        if lst_args[1] == '-l' and help.lib_key_exists(lst_args[2]):
            get_library_content_new(base_url,plex_token,lst_args[2])
        if lst_args[1] == '-m':
            print("IN GETTING A FILM BY NAME FUNC")
        if lst_args[1] == '-c' and help.lib_key_exists(lst_args[2]):
            get_collections_new(base_url,plex_token,lst_args[2])
    if arg_count == 4 and \
       lst_args[1] == '-c' and \
       help.lib_key_exists(lst_args[2]) and \
       help.coll_key_exists(lst_args[3]):
        get_collection_content(base_url,plex_token,lst_args[2],lst_args[3])
    else:
        help.show_help()
            
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    