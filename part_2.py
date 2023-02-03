from bs4 import BeautifulSoup
import pandas as pd
import requests

# Function to extract Product Title
def get_asin(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={'class' : 'a-text-bold'})

		# Inner NavigatableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value


	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Product Price
def get_desc(soup):

	try:
		price = soup.find("span", attrs={'class':'aplus-v2 desktop celwidget'}).string

	except AttributeError:
	
		price = ""	

	return price

# Function to extract Product Rating
def man(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-list-item'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews

if __name__ == '__main__':


	HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US'})

	m=pd.read_csv('result.csv')

    l=m['link']
	a=[]
	b=[]
	c=[]
	for URL in l:
        #URL = "https://www.amazon.in/s?k=bags&page="+str(i)+"crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
   
	# HTTP Request
	    webpage = requests.get(URL, headers=HEADERS)

        soup = BeautifulSoup(webpage.content, "lxml")

        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

        links_list = []

        for link in links:
            links_list.append(link.get('href'))

        for link in links_list:

            new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "lxml")
            #res=[]
            a.append(get_asin(new_soup))
            b.append(get_desc(new_soup))
            c.append(get_man(new_soup))
            #li.append(res)
    field_names = ['ASIN', 'Product Description', 'Manufacturer']
	m['ASIN']=a
	m['Product Description']=b
	m['Manufacturer']=c
    with open('res.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(m)
