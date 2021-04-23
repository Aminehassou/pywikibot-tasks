from pywikibot.data import api
import pywikibot

# Global variables
wikipedia_site = pywikibot.Site("en", "wikipedia")
site = pywikibot.Site("wikidata", "wikidata")

ptwiki_repo = site.data_repository()

# Initial code taken from https://gist.github.com/ettorerizza/7eaebbd731781b6007d9bdd9ddd22713

def search_entities(site, item_title):
    '''
    Searches for entities (using wikidata API) in specified site with specified item title

    :param site: site that will be searched for entities
    :param item_title: title of item that will be searched for in site
    '''
    parameters = { 'action' :'wbsearchentities', 
                'format' : 'json',
                'language' : 'en',
                'type' : 'item',
                'search': item_title}
    request = api.Request(site=site, parameters=parameters)

    return request.submit()

def get_entities(site, item_id):
    '''
    gets entities (using wikidata API) in specified site with specified item ids 

    :param site: site that entities will be gotten from
    :param item_id: item_id that will be searched for in site
    '''
    parameters = {'action' : 'wbgetentities',
            'format' : 'json',
            'ids' : item_id,
            'languages': 'en',
            'props': 'claims|labels',
            'sitefilter': 'enwiki'}

    request = api.Request(site=site, parameters=parameters)

    return request.submit()

def parse_entity_data(entities):
    '''
    parses and filters entity data for ids and returns those ids

    :param entities: entities that will have their data parsed
    '''

    entity_search_text = entities['searchinfo']['search']
    failure_message = f"Failed to find any matching entities for {entity_search_text}"
    matched_ids = {}

    # Checks if the search returned an empty list
    if entities["search"] == []:
        return failure_message

    for entity in entities["search"]:
        result = get_entities(site, entity["id"])

        if result["success"] == 1:
            output = result["entities"]
        else:
            return failure_message

        for qid, value in output.items():
            if "en" in output[qid]["labels"]:

                # Check if the search string and label match completely, this allows for filtering out wrong Qids
                if output[qid]["labels"]["en"]["value"].lower() == entity_search_text.lower():
                    matched_ids[entity_search_text] = qid
            else:
                matched_ids[entity_search_text] = qid

        if not matched_ids:
            return failure_message

    return matched_ids

def main():

    # Counter used to count elements searched from the unconnected pages
    counter = 0

    # Constant used to limit how many elements can be searched
    ELEMENT_LIMIT = 100

    unconnected_pages = wikipedia_site.querypage('UnconnectedPages')

    for page in unconnected_pages:
        item_to_search = page.title()
        entities = search_entities(site, item_to_search)
        print(parse_entity_data(entities))
        print()

        counter += 1

        if counter == ELEMENT_LIMIT:
            break


if __name__ == "__main__":
    main()