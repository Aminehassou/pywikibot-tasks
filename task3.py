import pywikibot
import re

# Global variables
wikipedia_site = pywikibot.Site("en", "wikipedia")
wikidata_site = pywikibot.Site("wikidata", "wikidata")
ptwiki_repo = wikidata_site.data_repository()

# Statements properties found in task 1 that need to be parsed for in the text
zelda_statement_properties = [{"id": "P1476", "value": "title", "infobox_flag": True},
                              {"id": "P31", "value": "is a", "infobox_flag": False},
                              {"id": "P179", "value": "series", "infobox_flag": True},
                              {"id": "P162", "value": "producer", "infobox_flag": True},
                              {"id": "P57", "value": "director", "infobox_flag": True},
                              {"id": "P577", "value": "released", "infobox_flag": True}]

candy_statement_properties = [{"id": "P31", "value": "is a", "infobox_flag": False},
                              {"id": "P577", "value": "released", "infobox_flag": True}]

def parse_article_text(page, property_info, infobox_search):
    '''
    Parses chosen wikipedia article text with regex and prints out property information
    in the form "property = property_value"

    :param page: The chosen wikipedia page that will be parsed for properties
    :param property_info: Name of chosen property that will be parsed for in the page
    :param infobox_search: Boolean flag, true if searching the infobox, false otherwise
    '''
    text = page.text

    if infobox_search:
        reg_pattern = fr"{{Infobox[\w|\W]*\|\s*(?:| {property_info})\s*=\S*(.*)"
    else:
        reg_pattern = fr"{property_info}.*?\[\[(.*?)\]\]"
        
    # regex search for parsing text
    captured_text = re.search(reg_pattern, text, re.IGNORECASE)

    if captured_text:
        item_property_value = captured_text.group(1).lstrip()
    else:
        return "No value found"

    return item_property_value

def check_claims(item, wikipedia_page, statement_properties):
    '''
    Checks claim type for parsed information and prints out item data

    :param item: Item that will have it's claims type checked and printed out
    :param wikipedia_page: The wikipedia page that will be used
    :param statement_properties: List of dictionaries that contain property data that will be used for wikidata calls on specified page

    '''
    for prop in statement_properties:
        result = parse_article_text(page=wikipedia_page, property_info=prop["value"], infobox_search=prop["infobox_flag"])

        data_values = []
        claims = item["claims"].get(prop["id"])

        for claim in claims:
            if claim.type == "monolingualtext":
                data_value = claim.getTarget().text
            elif claim.type == "wikibase-item":
                data_value = claim.getTarget().id
            elif claim.type == "time":
                data_value = claim.getTarget().toTimestr()

            data_values.append(data_value)

        print(f"{prop['id']}: {result}, Wikidata value(s): {' ; '.join(data_values)}")
        
    print("--------------------------------------------------------------------------")

def main():

    pedia_link = "The_Legend_of_Zelda:_Breath_of_the_Wild"
    data_link = "Q17185964"

    wikipedia_page = pywikibot.Page(wikipedia_site, pedia_link)

    # Accesses the wikidata claims for the chosen item
    item = pywikibot.ItemPage(ptwiki_repo, data_link).get()


    # Accesses the specified property statement for the chosen item
    check_claims(item, wikipedia_page, zelda_statement_properties)

    pedia_link = "Candy_Crush_Saga"
    data_link = "Q8768018"

    wikipedia_page = pywikibot.Page(wikipedia_site, pedia_link)

    # Accesses the wikidata claims for the chosen item
    item = pywikibot.ItemPage(ptwiki_repo, data_link).get()


    # Accesses the specified property statement for the chosen item
    check_claims(item, wikipedia_page, candy_statement_properties)

if __name__ == "__main__":
    main()