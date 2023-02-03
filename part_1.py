from bs4 import BeautifulSoup
import requests

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle','class' : 'a-size-large product-title-word-break'})

		# Inner NavigatableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value


	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Product Price
def get_price(soup):

	try:
		price = soup.find("span", attrs={'class':'a-offscreen'}).string

	except AttributeError:
	
		price = ""	

	return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

if __name__ == '__main__':


	HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US'})


    l=[]
	for i in range(1,21):
        URL = "https://www.amazon.in/s?k=bags&page="+str(i)+"crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
   
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
            res={}
            res["link"]="https://www.amazon.in" + link
            res["Product Title"]= get_title(new_soup)
            res["Product Price"]= get_price(new_soup))
            res["Product Rating"]= get_rating(new_soup))
            res["Number of Product Reviews"]= get_review_count(new_soup))
            l.append(res)
    field_names = ['link', 'Product Title', 'Product Price','Product Rating','Number of Product Reviews']
    with open('result.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(l)
