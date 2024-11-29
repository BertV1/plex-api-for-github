# plex-api-for-github
 get things done with plex via api (another one)

## what can you do

* get (your) server settings
  * xml output
* get a list of your libraries
* get full ocntent of your libraries
  * xml output
* a functional (?) script

## TODO

### prio’s:

* merge mass-film-name-editor-given-a-collection into main script
  * get collections of a library
  * get collection content by key (after having being shown the collections)
* actually use ssl

### interesting:

* get props (any) of given a film name
* change props (any, as in, any that are possible to chg) of a given film by name

### nice to have:

* get collection by name
* create collection by name
* add films to collection by (name,name)
  * eg: 
    * user req: i want all films produced by the **Weinstein** Company in a collection named “**TO AVOID**” 

## request

generic function which ideally should work for every request:
For now, it should be able to handle the following requests:

- server_settings:        https://192.168.0.33:32400/?X-Plex-Token=XXX
- get_libraries:          https://192.168.0.33:32400/library/sections?X-Plex-Token=XXX
- get_library_content:    https://192.168.0.33:32400/library/sections/1/all?X-Plex-Token=XXX
- get_collections:        https://192.168.0.33:32400/library/sections/1/collection?X-Plex-Token=XXX
- get_collection_content: https://192.168.0.33:32400/library/sections/1/all?collection=3441&X-Plex-Token=XXX
- get_collection_content: https://192.168.0.33:32400/library/collections/8469/children?X-Plex-Token=XXX

```python
    make_requests
            (
                "https://192.168.0.33:32400",
                [  # the url parts
                    "library/sections",
                    "1",
                    "all"
                ],
                [  # the args
                    ["collection",3441],
                    ["X-Plex-Token","XXX"]
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

* if a acquired media item isn’t *matched*, certain script functions won’t work for now:
  * get-data-from-xml functions: extract data from xml based on existence of attributes (metadata properties)
  * show functions: needs the above to work
* ~~if a media item is removed (from a collection) through the WEB GUI, it isn’t (immediately?) cascaded to the API data.~~ 

