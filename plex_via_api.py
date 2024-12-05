import ssl
import helper_funcs as help
import helper_creds as creds
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
    'COLLECTIONS':'plex_collections.xml',
    'COLLECTION':'plex_coll_content.xml',
    'FILM':'plex_film_content.xml',
    'FILM_SEARCH':'plex_film_search_list.xml'
    }
# base URL, usually does not change.
UPDATE = True

def get_server_settings(str_base_url,lst_token):
    
    if help.check_xml_existence(STATIC_FILES['SERVER_SETTINGS']) and not UPDATE:
        print("file already exists")
        exit(0)
    url_elems = ['',lst_token]
    
    req_url = str_base_url + help.build_request_url_elems(url_elems)
    req_resp = help.get_request(req_url)
    help.write_xml(req_resp,STATIC_FILES['SERVER_SETTINGS'])
    exit(0)
    
    
def get_libraries(str_base_url,lst_token):
    
    if help.check_xml_existence(STATIC_FILES['LIBRARIES']) and not UPDATE:
        help.show_libraries(STATIC_FILES['LIBRARIES'])
        exit(0)
    
    url_elems = [["library","sections"],lst_token]
    req_url = str_base_url + help.build_request_url_elems(url_elems)
    req_resp = help.get_request(req_url)
    
    help.write_xml(req_resp,STATIC_FILES['LIBRARIES'])
    help.show_libraries(STATIC_FILES['LIBRARIES'])


# TODO: dynamic filename based on libkey
def get_library_content(str_base_url,lst_token,lib_key):
    if help.check_xml_existence(STATIC_FILES['LIB_CONTENT']) and not UPDATE:
        print("file already exists.")
        exit(0)
    
    url_elems = [["library","sections",lib_key,"all"],lst_token]
    req_url = str_base_url + help.build_request_url_elems(url_elems)
    req_resp = help.get_request(req_url)
    
    help.write_xml(req_resp,STATIC_FILES['LIB_CONTENT'])
    
    
def get_collections(str_base_url,lst_token,lib_key):
    
    if help.check_xml_existence(STATIC_FILES['COLLECTIONS']) and not UPDATE:
        help.show_collections(STATIC_FILES['COLLECTIONS'])
        exit(0)
    
    url_elems = [["library","sections",lib_key,"collections"],lst_token]
    req_url = str_base_url + help.build_request_url_elems(url_elems)
    req_resp = help.get_request(req_url)
    
    help.write_xml(req_resp,STATIC_FILES['COLLECTIONS'])
    help.show_collections(STATIC_FILES['COLLECTIONS'])

def get_collection_content(str_base_url,lst_token,lib_key,coll_key):
    fname = coll_key+"-"+STATIC_FILES['COLLECTION']
    if help.check_xml_existence(fname) and not UPDATE:
        print("file already exists.")
        help.show_collection_content(fname)
        exit(0)

    url_elems = [["library","collections",coll_key,"children"],lst_token]
    req_url = str_base_url + help.build_request_url_elems(url_elems)
    req_resp = help.get_request(req_url)

    help.write_xml(req_resp,fname)
    help.show_collection_content(fname)

def get_film_by_key(str_base_url,lst_token,mov_key):
    
    fname = mov_key+"-"+STATIC_FILES['FILM']
    if help.check_xml_existence(fname) and not UPDATE:
        exit(0)
    
    url_elems=[["library","metadata",mov_key],lst_token]
    req_url = str_base_url + help.build_request_url_elems(url_elems)
    req_resp = help.get_request(req_url)
    
    help.write_xml(req_resp,fname)

def get_films_by_terms(str_base_url,lst_token,str_terms):
    
    fname = str_terms.replace(' ','-')+"-"+STATIC_FILES['FILM_SEARCH']
    
    if help.check_xml_existence(fname) and not UPDATE:
        help.show_film_search_content(fname)
        exit(0)
    
    lst_token.append(["query",str_terms])
    lst_token.append(["limit","100"])
    lst_token.append(["sectionId","1"])
    
    url_elems=[["hubs","search"],lst_token]
    req_url = str_base_url + help.build_request_url_elems(url_elems,end_slash=True)
    req_resp = help.get_request(req_url)
    
    help.write_xml(req_resp,fname)
    help.show_film_search_content(fname)

# update_url = "https:///library/sections/1/all?type=1&id=" + str(movie_id) + "&includeExternalMedia=1&title.value=" + parsed_correct_title + "&title.locked=1&X-Plex-Token="
def update_filmTitles_by_collId(str_base_url, lst_token,lib_key,coll_key):
    fname = coll_key+"-"+STATIC_FILES['COLLECTION']
    if help.check_xml_existence(fname) and not UPDATE:
        print("file already exists.")
    else:
        url_elems = [["library","collections",coll_key,"children"],lst_token]
        req_url = str_base_url + help.build_request_url_elems(url_elems)
        req_resp = help.get_request(req_url)
        help.write_xml(req_resp,fname)
    # update films

    coll_content = help.getCollectionContentFromXmL(fname)
    updated_movies = help.parse_titles(coll_content)

    for updated_film in updated_movies:
        lst_token.append(["type","1"])
        lst_token.append(["id",updated_film[0]])
        lst_token.append(["includeExternalMedia","1"])
        lst_token.append(["title.value",updated_film[1]])
        lst_token.append(["title.locked","1"])
        url_elems = [["library","sections",lib_key,"all"],lst_token]
        req_url = str_base_url+help.build_request_url_elems(url_elems)
        print(req_url)
        # req_resp = help.put_request(req_url)



            
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
                get_server_settings(base_url,plex_token)
            if lst_args[1] == '-l':
                get_libraries(base_url,plex_token)
                exit(0)
    if arg_count == 3:
        if lst_args[1] == '-l' and help.lib_key_exists(lst_args[2]):
            get_library_content(base_url,plex_token,lst_args[2])
        if lst_args[1] == '-c' and help.lib_key_exists(lst_args[2]):
            get_collections(base_url,plex_token,lst_args[2])
    if arg_count == 4:
        if lst_args[1] == '-c' and help.lib_key_exists(lst_args[2]) and help.coll_key_exists(lst_args[3]):
            get_collection_content(base_url,plex_token,lst_args[2],lst_args[3])
        if lst_args[1] == '-m':
            if lst_args[2] == '-key' and lst_args[3].isdigit():
                get_film_by_key(base_url,plex_token,lst_args[3])
                print("IN GETTING A FkILM BY KEY FUNC")
            if lst_args[2] == '-term':
                get_films_by_terms(base_url,plex_token,lst_args[3])
                print("GETTING A FILM BY TERM")
    if arg_count == 5:
        # -c lib_key coll_key -update
        print("updating titles by coll")
        if lst_args[1] == '-c' and help.lib_key_exists(lst_args[2]) and help.coll_key_exists(lst_args[3]) and lst_args[4] == '-update':
            print("args OK")
            update_filmTitles_by_collId(base_url,plex_token,lst_args[2],lst_args[3])
    else:
        help.show_help()
            
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    