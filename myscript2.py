import pywikibot
import re

# Global variables
wikipedia_site = pywikibot.Site("en", "wikipedia")
wikidata_site = pywikibot.Site("wikidata", "wikidata")
ptwiki_repo = wikidata_site.data_repository()

# Statements properties found in task 1 that need to be parsed for in the text
statement_properties = {"P1476": "title"}

def parse_article_text(page, property_info):
    '''
    Parses chosen wikipedia article text with regex and prints out property information
    in the form "property = property_value"

    :param page: The chosen wikipedia page that will be parsed for properties
    :param property_info: Name of chosen property that will be parsed for in the page
    '''
    text = page.text

    # regex search for getting infobox statements:
    infobox_text = re.search(fr"{{Infobox[\w|\W]*\|\s*(| {property_info})\s*=\S*(.*)",text)

    item_property_value = infobox_text.group(2).lstrip()        
    return item_property_value

def main():

    pedia_link = "The_Legend_of_Zelda:_Breath_of_the_Wild"
    data_link = "Q17185964"

    wikipedia_page = pywikibot.Page(wikipedia_site, pedia_link)

    # Accesses the wikidata claims for the chosen item
    item = pywikibot.ItemPage(ptwiki_repo, data_link).get()["claims"].__dict__["_data"]

    # Accesses the specified property statement for the chosen item
    data_title = item["P1476"][0].getTarget()

    data_title_text = data_title.__dict__["text"]

    title = parse_article_text(wikipedia_page, statement_properties["P1476"])

    print(f"P1476: {title}, Wikidata value: {data_title_text}")
    #print(f"P179: {series}")



if __name__ == "__main__":
    main()