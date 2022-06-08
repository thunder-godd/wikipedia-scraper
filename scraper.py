from bs4 import BeautifulSoup
import requests
import re

def scrape_page(page_url):
    """Extracts HTML from a webpage"""
    
    response = requests.get(page_url)
    content = response.content
    soup = BeautifulSoup(content, features='html.parser')
    soup.encode('utf-8')
    return soup

def form_string(str1,str2):
    """ Forms the output string """   
    return  "[Original]: " +''.join(str1)+'\n' +"[Punctuated]: "+''.join(str2).rstrip('\n')+ " ###" +"\n" + "<|endoftext|> "+"\n\n" 

def find_chunks(soup):
    """ Finds the chunks of paragraphs and formats each paragraph """    
    chunks=[]
    new_paragraphs=[]

    main=soup.find('div',class_="mw-parser-output")

    toc=soup.find('div',class_='toc')
    """find first chunk i.e all paragraphs above the ToC  """
    first_chunk=toc.find_previous_siblings('p')
    first_chunk.reverse()
    first_chunk.pop(0)
    chunks.append(first_chunk)
    #paragraghs=toc.find_next_siblings('p')
    headings=main.find_all('h2')
    headings.pop(0)
    headings.pop(-1)#remove reference heading


    def create_chunk(h):
        my_chunk=[]
        def rec(h):
            p=h.find_next_sibling()
            if p.name=='p' :
                my_chunk.append(p)
                return rec(p)
            else:
                return   
        rec(h)

        chunks.append(my_chunk)



    def format_chunk(chunk):
        """ Formats individual paragraphs,remove newlines,punctuation and """
        punctuated_chunk=[]   
        original_chunk=[] 
        if len(chunk) != 0:
     
            for p in chunk:
                p_text=p.get_text()
                punctuated=re.sub(r"\[(.*?)\]",'',p_text) + '\n' #remove citations
                original=punctuated.casefold().rstrip('\n')        
                formatted=re.sub(r'[^\w\s]', '',original) #remove punctuation
                original_chunk.append(formatted.rstrip('\n'))
                punctuated_chunk.append(punctuated)
            
            text=form_string(original_chunk,punctuated_chunk)   
        else:
            text=''     
        return text

    for h in headings:
        create_chunk(h)
    
    for c in chunks:
        new_paragraphs.append(format_chunk(c))  
        
    return new_paragraphs
output=[]
with open( r'input_file.txt','r',) as i:
    """Read URLs, Scrape the Pages,  """
    urls=i.readlines()
    for url in urls:
        my_url=url.rstrip() #remove '\n' from url
        print(my_url)
        page=scrape_page(my_url)   
        output.append(find_chunks(page))

#print(len(output))


with open(r"output.txt",'w',encoding='utf-8') as f:
    for i in output:
        f.write(''.join(i))
