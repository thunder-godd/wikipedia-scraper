from bs4 import BeautifulSoup
import requests
import re

""" 
open input txt file
find urls
open site form url
parse html
find all paragraphs
format the paragraphs:
    lowercase
    remove punctuation and citations except  '
write paragraphs to txt file

"""

def scrape_page(page_url):
    """Extracts HTML from a webpage"""
    
    response = requests.get(page_url)
    content = response.content
    soup = BeautifulSoup(content, features='html.parser')
    soup.encode('utf-8')
    return soup
""" 
[Original]:  here is the original text [Punctuated]: Here is the punctuated text. ### 
"""
test_p=""" In the late 1950s, Dunstan became well known for his campaign against the death penalty being imposed on Max Stuart, who was convicted of rape and murder of a small girl, opposing then-Premier Thomas Playford IV over the matter. During Labor's time in opposition, Dunstan was prominent in securing some reforms in Aboriginal rights and in Labor abandoning the White Australia policy."""

def format_paragraphs(soup):
    """ Formats the HTML to the desired output """
    def form_string(str1,str2):
        return "[Original]:" + str1 +"[Punctuated]:" +str2 + "###" +"\n"  + "<|endoftext|> ""\n\n" 

    
    paragaphs=soup.find_all('p')
    new_paragraphs=[]
    for p in paragaphs:
        p_text=p.get_text().rstrip('\n')
        punctuated=p_text
        original=p_text.casefold().rstrip('\n')    

        new_o=re.sub(r"[^\w\s']", '',original)

        text=form_string(new_o,punctuated)
        new_paragraphs.append(text)

    return new_paragraphs

output=[]
with open( r'input_file.txt','r',) as i:
    """Read URLs, Scrape the Pages,  """
    urls=i.readlines()
    #print(urls)
    for url in urls:
        my_url=url.rstrip()#remove '\n' from url
        #print(my_url)
        page=scrape_page(my_url)

        output.append(format_paragraphs(page))

print(output)

    


with open(r"output.txt",'w',encoding='utf-8') as f:
    for item in output:
        for text in item:
            f.write(text)        