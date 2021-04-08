import pywikibot
import re

# Global variables
site = pywikibot.Site("en", "wikipedia")
ptwiki_repo = site.data_repository()

def parse_article_text(page):
    #regex for getting infobox statements:
    #{{Infobox[\w|\W]*\|\s*(series)\s*=\S*(.*)
    text = page.text
    infobox_text = text[text.index("Infobox"):text.index("==")]        
    print(infobox_text)

def main():

    link = "The_Legend_of_Zelda:_Breath_of_the_Wild"
    page = pywikibot.Page(site, link)
    parse_article_text(page)


if __name__ == "__main__":
    main()