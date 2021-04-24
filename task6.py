from pywikibot.data import api
import pywikibot
import re


# Global variables
wikipedia_site = pywikibot.Site("en", "wikipedia")
site = pywikibot.Site("wikidata", "wikidata")

ptwiki_repo = site.data_repository()

CATEGORY = "L'Équipe football player ID not in Wikidata"
TERM = "Lequipe"


def parse_article_text(page, property_info, infobox_search):
    '''
    Parses chosen wikipedia article text with regex and returns the matched value (note: taken from prior code)

    :param page: The chosen wikipedia page that will be parsed for properties
    :param property_info: Name of chosen property that will be parsed for in the page
    :param infobox_search: Boolean flag, true if searching the infobox, false otherwise
    '''
    text = page.text

    if infobox_search:
        reg_pattern = fr"{{Infobox[\w|\W]*\|\s*(?:| {property_info})\s*=\S*(.*)"
    else:
        reg_pattern = fr"(?<={{{property_info}\|)(.*?)(?=[\||}}])"
        
    # regex search for parsing text
    captured_text = re.search(reg_pattern, text, re.IGNORECASE)

    if captured_text:
        item_property_value = captured_text.group(1).lstrip()
    else:
        return "No value found"

    return item_property_value

def add_item_property(property_id, value, item, description, is_image=False, is_numerical_id=False,  is_date=False):
    '''
    Adds property/value pair to chosen wikidata item (Note: taken from my task 4 code)

    :param property_id: id of property to be added to item
    :param value: property-linked value to be added to item
    :param item: item that will have property/value pair be added to it
    :param description: summary describing the addition
    :param is_image: flag describing if image will be added or not, false by default
    :param is_numerical_id: flag describing if numerical id will be added or not, false by default
    :param is_date: flag describing if date will be added or not, false by default
    '''

    item_data = item.get()

    if is_image:
        claim_target = pywikibot.FilePage(ptwiki_repo, title=value)
    elif is_numerical_id:
        claim_target = value
    elif is_date:
        claim_target = pywikibot.WbTime(year=value["year"],month=value["month"],day=value["day"],site=site)
    else:
        claim_target = pywikibot.ItemPage(ptwiki_repo, value)

    new_claim = pywikibot.Claim(ptwiki_repo, property_id)
    new_claim.setTarget(claim_target)
    item.addClaim(new_claim, summary=description)

def add_category_ids(category, term):
    '''
    Adds the ids of the chosen categories to wikidata

    :param category: The wikipedia category being looked through
    :param term: term being searched for in the wikipedia articles of said category
    '''
    category = pywikibot.Category(wikipedia_site, category)
    category_pages = category.articles()
    for page in category_pages:
        parsed_id = parse_article_text(page=page, property_info=term, infobox_search=False)

        # Filters out any non-digit characters from the returned regex captured text
        filtered_id = ''.join(i for i in parsed_id if i.isdigit())

        item = pywikibot.ItemPage.fromPage(page)
        add_item_property(property_id="P3665", value=str(filtered_id), item=item, description=f"Added P3665:{filtered_id}", is_numerical_id=True)

        


def main():

    add_category_ids(category=CATEGORY, term=TERM)

if __name__ == "__main__":
    main()