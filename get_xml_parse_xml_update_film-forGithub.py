import ssl
import requests
import xml
import xml.etree.ElementTree as ET
import urllib.parse

ssl.SSLContext.verify_mode == ssl.VerifyMode.CERT_OPTIONAL

# PARSE XML

plex_data = ET.parse('34914-plex_coll_content.xml')
# MediaContainer = Root
xml_root = plex_data.getroot()
film_data = []
# Video element contains required attributes
for item in xml_root.findall('./Video'):
    film_data.append([item.attrib['ratingKey'], item.attrib['title']])
print(len(film_data))


# # FIX TITLES, PREP DATA & UPDATE FILM

def change_title_in_plex(movie_id, correct_title):
    parsed_correct_title = urllib.parse.quote(correct_title)
    update_url = "https:///library/sections/1/all?type=1&id=" + str(
        movie_id) + "&includeExternalMedia=1&title.value=" + parsed_correct_title + "&title.locked=1&X-Plex-Token="
    response = requests.put(update_url, verify=False)
    print(response.text)


cnt = 0
for blob in film_data:
    print(blob[1])
    if "RARBG" in blob[1]:
        lst_blob = blob[1].split('.')
        for elem in lst_blob:
            if elem.isdigit():
                lst_title = lst_blob[:lst_blob.index(elem)]
                title = ' '.join(lst_title)
    # change_title_in_plex(blob[0],title)
        print(str(title) + "->" + str(blob[0]))
    if "nickarad" in blob[1]:
        film_title = blob[1].split(" (")[0]
        print(str(film_title) + "->" + str(blob[0]))
    if "[H264-mp4]" in blob[1]:
        film_title_prep = blob[1].split("- ")[0].split(' ')
        if film_title_prep[0].isdigit():
            film_title_prep.pop(0)
        film_title = ' '.join(film_title_prep)
        print(str(film_title) + "->" + str(blob[0]))
print(cnt)