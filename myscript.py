import pywikibot


# Global variables
site = pywikibot.Site("wikidata", "wikidata")
ptwiki_repo = site.data_repository()

def append_content(new_text, page):
    '''
    Appends chosen text onto the end of a wiki page

    :param new_text: text to be added to page
    :param page: wiki page that will have the added text appended onto it
    '''

    text = page.text
    print(text)

    page.text += "\n" + new_text
    page.save(f"Added {new_text} with pywikibot")

def add_item_property(property_id, value, item):
    '''
    Adds property/value pair to chosen wikidata item

    :param property_id: id of property to be added to item
    :param value: property-linked value to be added to item
    :param item: item that will have property/value pair be added to it
    '''
    item_data = item.get()
    claim_target = pywikibot.ItemPage(ptwiki_repo, value)
    new_claim = pywikibot.Claim(ptwiki_repo, property_id)
    new_claim.setTarget(claim_target)
    item.addClaim(new_claim, summary=f"Added {property_id}")

def output_item_data(item):
    '''
    Outputs item aliases, sitelinks, descriptions, claims and labels to the python console.

    :param item: qualifier value of wikidata item
    '''
    # Used for clearer formatting
    seperator = "-"*50

    # English chosen just for demonstration
    language = "en"
    site_language = "enwiki"

    item_data = item.get()

    aliases = item_data["aliases"]
    sitelinks = item_data["sitelinks"].__dict__
    descriptions = item_data["descriptions"].__dict__
    claims = item_data["claims"].__dict__
    labels = item_data["labels"]

    if language in aliases:
        print("English Aliases:")
        print(aliases[language])
    else:
        print("There are no english aliases for this item!")
    print()

    if site_language in sitelinks["_data"]:
        print("English Sitelinks:")
        print(sitelinks["_data"][site_language])
    else:
        print("There are no english sitelinks for this item!")
    print()

    if language in descriptions["_data"]:
        print("English Descriptions:")
        print(descriptions["_data"][language])
    else:
        print("There are no english descriptions for this item!")
    print()

    print("Claims:")
    for key, value in claims["_data"].items():
        print(f"Property: {key}")
        print(f"Value: {[x.getTarget() for x in value]}")
        print()

    if language in labels:
        print("English Labels:")
        print(labels["en"])
    else:
        print("There are no english labels for this item!")

    print(seperator)

def main():

    link = "User:Amine_hassou/Outreachy_1"
    page = pywikibot.Page(site, link)

    # Appending Hello at the end of https://www.wikidata.org/wiki/User:Amine_hassou/Outreachy_1
    append_content(new_text="Hello", page=page)

    # Outputting wikidata sandbox item data:
    # https://www.wikidata.org/wiki/Q4115189
    sandbox_item = pywikibot.ItemPage(ptwiki_repo, "Q4115189")
    output_item_data(item=sandbox_item)

    # Outputting wikidata zelda breath of the wild item data:
    # https://www.wikidata.org/wiki/Q17185964
    zelda_item = pywikibot.ItemPage(ptwiki_repo, "Q17185964")
    output_item_data(item=zelda_item)

    # Adds instance of wiki sandbox to wikidata sandbox item:
    # https://www.wikidata.org/wiki/Q4115189
    add_item_property(property_id="p31", value="Q3938", item=sandbox_item)

if __name__ == "__main__":
    main()