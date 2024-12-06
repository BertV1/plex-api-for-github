# plex-api-for-github
admin script for a plex server. quick and easy data viewing, manipulation.

## what can you do

* get (your) server settings
* get a list of your libraries
* get full content of your libraries
* get a list of your collections (by library)
* get a list of films in your collections
* get a film by key
* get film(s) by search term(s)
* clean film titles by collection

## TODO

### prio’s:

merge mass-film-name-editor-given-a-collection into main script
- [x] get collections of a library
- [x] get collection content by key (after having being shown the collections)
- [x] search by terms
- [x] update film titles

use “”“ssl”“” …

other:

- [x] add the option to use new data if existing data is already present on user system. 
- [ ] use a more efficient and clean way to interact with the data, but avoid outgrowing the scope of the project with tech like databases.
  - [ ] checkout: memcached, cachetools
- [ ] 

### interesting:

- [x] get props (any) of a film given a name (search term)
- [ ] change props (any, as in, any that are possible to chg) of a given film by name

### nice to have:

- [ ] get collection by name
- [ ] create collection by name
- [ ] add films to collection by (name,name)
  * user req: i want all films produced by the **Weinstein** Company in a collection named “**TO AVOID**” 

## request

Request builder functions handle all kinds of API requests:

| func                        | url                                                          |
| --------------------------- | ------------------------------------------------------------ |
| server_settings             | https://192.168.0.33:32400/?X-Plex-Token=XXX                 |
| get_libraries               | https://192.168.0.33:32400/library/sections?X-Plex-Token=XXX |
| get_library_content         | https://192.168.0.33:32400/library/sections/lib_id/all?X-Plex-Token=XXX |
| get_collections             | https://192.168.0.33:32400/library/sections/lib_id/collection?X-Plex-Token=XXX |
| get_collection_content      | https://192.168.0.33:32400/library/sections/lib_id/all?collection=coll_id&X-Plex-Token=XXX |
| get_collection_content      | https://192.168.0.33:32400/library/collections/coll_id/children?X-Plex-Token=XXX |
| get_a_film                  | https://192.168.0.33:32400/library/metadata/mov_id?X-Plex-Token=XXX |
| search_films_by_terms       | https://192.168.0.33:32400/hubs/search/?X-Plex-Token=XXX&query=stringstringstring&limit=100&sectionId=1 |
| update_filmTitles_by_collId | https:///library/sections/1/all?type=1&id=mov_id&includeExternalMedia=1&title.value=stringstring&title.locked=1&X-Plex-Token=XXX |

```python
    make_requests
            (
                base_url,
                [  # the url parts
                    "library/sections",
                    lib_id,
                    "all"
                ],
                [  # the args
                    ["collection",coll_id],
                    plex_token
                ]
            )
```

## Write

files are written to user home. Most files should have stdrdized naming convention, <coll_key>-plex_coll_content.xml is one example for the content of a plex collection identified with coll key.

## Oddities

* get_collections (API) has a different output
  * browser: static collection only, minimal amount of keys
  * script: diff. between smart & static collections, high level of detail, completely different url to actually get the content
    * different rating key
    * no mention of lib key

* ~~if a acquired media item isn’t *matched*, certain script functions won’t work for now:~~
  * ~~get-data-from-xml functions: extract data from xml based on existence of attributes (metadata properties)~~
  * ~~show functions: needs the above to work~~
* ~~if a media item is removed (from a collection) through the WEB GUI, it isn’t (immediately?) cascaded to the API data.~~ 

