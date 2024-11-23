import ssl
import requests
import xml
import xml.etree.ElementTree as ET
import urllib.parse
ssl.SSLContext.verify_mode == ssl.VerifyMode.CERT_OPTIONAL

# PARSE XML

plex_data = ET.parse('content_of_collection_name.xml')
# MediaContainer = Root
xml_root = plex_data.getroot()
film_data = []
# Video element contains required attributes
for item in xml_root.findall('./Video'):
    film_data.append([item.attrib['ratingKey'],item.attrib['title']])
print(len(film_data))


# # FIX TITLES, PREP DATA & UPDATE FILM

def change_title_in_plex(movie_id, correct_title):
    parsed_correct_title = urllib.parse.quote(correct_title)
    update_url = "https:///library/sections/1/all?type=1&id="+str(movie_id)+"&includeExternalMedia=1&title.value="+parsed_correct_title+"&title.locked=1&X-Plex-Token="
    response = requests.put(update_url,verify=False)
    print(response.text)
    

for blob in film_data:
    lst_blob = blob[1].split('.')
    for elem in lst_blob:
        if elem.isdigit():
            lst_title = lst_blob[:lst_blob.index(elem)]
            title = ' '.join(lst_title)
    change_title_in_plex(blob[0],title)
    print(str(title)+"->"+str(blob[0]))

