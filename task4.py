import pywikibot

# Please note that this code has already been executed, rerunning it will create duplicate claims.

# Global variables
site = pywikibot.Site("wikidata", "wikidata")
ptwiki_repo = site.data_repository()

def add_item_property(property_id, value, item, description, is_image=False, is_numerical_id=False,  is_date=False):
    '''
    Adds property/value pair to chosen wikidata item (Note: taken from my task 2 code with a few modifications)

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

def add_qualifier(property_id, qualifier_id, qualifier_value, item, description):
    '''
    Adds property/value pair to chosen wikidata item (Note: taken from my task 2 code with a few modifications)

    :param property_id: id of property that will have qualifier added to it
    :param qualifier_id: id of qualifier that will be added to property
    :param qualifier_value: value of qualifier
    :param item: item that will have qualifier added to it's properties
    :param description: summary describing the addition
    '''

    item_data = item.get()
    new_qualifier = pywikibot.Claim(ptwiki_repo, qualifier_id)
    target = pywikibot.ItemPage(ptwiki_repo, qualifier_value)
    new_qualifier.setTarget(target)
    for claim in item.claims[property_id]:
        if qualifier_id not in claim.qualifiers:
            claim.addQualifier(new_qualifier, summary=description)

def main():

    # wikidata sandbox item: https://www.wikidata.org/wiki/Q4115189
    sandbox_item = pywikibot.ItemPage(ptwiki_repo, "Q4115189")

    nintendo_switch_item = pywikibot.ItemPage(ptwiki_repo, "Q19610114")
    fire_emblem_item = pywikibot.ItemPage(ptwiki_repo, "Q1768977")
    rogue_heroes_item = pywikibot.ItemPage(ptwiki_repo, "Q105100356")
    iron_gate_item = pywikibot.ItemPage(ptwiki_repo, "Q105725001")


    # Adds display technology property with liquid crystal display value to nintendo switch page:
    # nintendo switch: https://www.wikidata.org/wiki/Q19610114
    print("Adding P5307:Q83341...")
    add_item_property(property_id="P5307", value="Q83341", item=nintendo_switch_item, description="Added display technology (P5307) with value liquid crystal display (Q83341)")
    
    # Adds logo image property with File:Fire Emblem logo.svg value to fire emblem page:
    # fire emblem: https://www.wikidata.org/wiki/Q1768977 
    print("Adding P154:File:Fire Emblem logo.svg...")
    add_item_property(property_id="P154", value="File:Fire Emblem logo.svg", item=fire_emblem_item, description="Added logo image (P154) with value File:Fire Emblem logo.svg", is_image=True)

    # Adds HowLongToBeat ID property with 88752 value to Rogue Heroes: Ruins of Tasos page:
    # Rogue Heroes: Ruins of Tasos: https://www.wikidata.org/wiki/Q105100356 
    print("Adding P2816:88752...")
    add_item_property(property_id="P2816", value="88752", item=rogue_heroes_item, description="Added HowLongToBeat ID (P6783) with value 88752", is_numerical_id=True)

    # Adds inception property with april 2019 value to Iron Gate Studio page:
    # Iron Gate Studio: https://www.wikidata.org/wiki/Q105725001
    print("Adding p571:april 2019...")
    add_item_property(property_id="P571", value={"year": 2019, "month": 4, "day": None}, item=iron_gate_item, description="Added inception property (P571) with value april 2019", is_date=True)
    

    # QUALIFIERS:
    # Could not find any useful qualifiers to add, using it on sandbox just to demonstrate it works
    # wikidata sandbox item: https://www.wikidata.org/wiki/Q4115189
    print("Adding qualifier...")
    add_qualifier("P571", "P447", "Q105584", sandbox_item, "test")

if __name__ == "__main__":
    main()