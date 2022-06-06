from bs4 import BeautifulSoup
import requests
import re

""" 
open input txt file
find urls
open site form url
parse html
find all paragraphs that have <h3> or <h2> as an immediate sibling
format the paragraphs:
    lowercase
    remove punctuation and citations except  '
write paragraphs to txt file

"""

test_p=""" In the late 1950s, Dunstan became well known for his campaign against the death penalty being imposed on Max Stuart, who was convicted of rape and murder of a small girl, opposing then-Premier Thomas Playford IV over the matter. During Labor's time in opposition, Dunstan was prominent in securing some reforms in Aboriginal rights and in Labor abandoning the White Australia policy."""
"""
desired output: [Original]: in the late 1950s dunstan became well known for his campaign against the death penalty being imposed on max stuart who was convicted of rape and murder of a small girl opposing thenpremier thomas playford iv over the matter during labor's time in opposition dunstan was prominent in securing some reforms in aboriginal rights and in labor abandoning the white australia policy dunstan became attorneygeneral after the 1965 election and replaced the older frank walsh as premier in 1967 despite maintaining a much larger vote over the liberal and country league lcl labor lost two seats at the 1968 election with the lcl forming government with support of an independent dunstan responded by increasing his attacks on the playmander convincing the lcl into watering down the malapportionment with little change in labor's vote but with the playmander removed labor won 27 of 47 seats at the 1970 election and again in 1973 1975 and 1977 
                [Punctuated]: In the late 1950s, Dunstan became well known for his campaign against the death penalty being imposed on Max Stuart, who was convicted of rape and murder of a small girl, opposing then-Premier Thomas Playford IV over the matter. During Labor's time in opposition, Dunstan was prominent in securing some reforms in Aboriginal rights and in Labor abandoning the White Australia policy.. ### 
"""



def scrape_page(page_url):
    """Extracts HTML from a webpage"""
    
    response = requests.get(page_url)
    content = response.content
    soup = BeautifulSoup(content, features='html.parser')
    soup.encode('utf-8')
    return soup

def find_chunks(soup):
    """ Finds the chunks of paragraphs and formats each paragraph """
    def form_string(str1,str2):
        return "[Original]: " + str1 +'\n'+"[Punctuated]: " +str2.rstrip('\n') + " ###" +"\n" + "<|endoftext|> "+"\n\n" 
    chunks=[]
    paragraphs=[]
    main=soup.find('div',class_="mw-parser-output")
    toc=soup.find('div',class_='toc')

    first_chunk=toc.find_previous_siblings('p')
    first_chunk.pop()
    first_chunk.reverse()
    headings=main.find_all('h2')
    headings.pop(0)
    headings.pop(-1)
    chunks.append(first_chunk)
    for h in headings:
        span=h.find('span')
        if  not span['id']=='External_links':
            chunks.append(h.find_next_siblings('p'))
    def format_chunks(chunk):    
        for p in chunk:
            if (not p.attrs=='class') and len(p.get_text())>2 :
                print(p)
                p_text=p.get_text()
                punctuated=re.sub("\[(.*?)\]",'',p_text)
                original=p_text.casefold().rstrip('\n')        
                new_o=re.sub(r'[^\w\s]', '',original) #remove punctuation
                formatted=re.sub("\[(.*?)\]",'',new_o) #remove citations
                text=form_string(formatted,punctuated)
                paragraphs.append(text)

    for c in chunks:
        format_chunks(c)
    return paragraphs

output=[]
with open( r'input_file.txt','r',) as i:
    """Read URLs, Scrape the Pages,  """
    urls=i.readlines()
    
    for url in urls:
        my_url=url.rstrip() #remove '\n' from url
        page=scrape_page(my_url)
        output.append(find_chunks(page))   




with open(r"output.txt",'w',encoding='utf-8') as f:
     for item in output:
         for text in item:
             f.write(text)        