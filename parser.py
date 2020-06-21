import requests
from bs4 import BeautifulSoup
import re
import time

def make_soup(url):
    # Make a request to the URL
    r = requests.get(url)
    # Use BeautifulSoup to read teh text and lxml
    soup = BeautifulSoup(r.text, 'lxml')
    # Obey the 30 second crawl delay in the MIT robots.txt file
    time.sleep(30)
    # Return the soup
    return soup

def get_xml_urls(soup):
    urls = [loc.string for loc in soup.find_all('loc')]
    return urls

def get_src_contain_str(soup, string):
    srcs = soup.find_all('meta', content=re.compile(string))
    return srcs

# Start the program
if __name__ == '__main__':
    # define the URL to the MIT sitemap
    xml = 'https://dspace.mit.edu/sitemap?map=1'
    # Make soup using BeautifulSoup out of the URLs
    soup = make_soup(xml)
    # Get the XML URLs soup
    urls = get_xml_urls(soup)
    # Create a string for the end of the XML URL
    end_xml = '?show=full'
    # Creat a subsrting for the PDF
    substring = "application/pdf"
    # Open a file to write the URLs to PDF's
    with open("urlsmit.txt", "a") as urls_file:
        # Open a file to write the URLs to XML's metadata
        with open("xmlsmit.txt", "a") as xmls_file:
            # For each URL in the list of URL's in a sitemap
            for url in urls:
                # Get the PDF File
                # Create a PDF file url list
                url_soup = make_soup(url)
                # print (url)
                # Get the string with PDF at the end of it.
                srcs = get_src_contain_str(url_soup, ".pdf")
                # Make a string out of srcs i.e. sources
                soup_string = str(srcs)
                # Remove the first 16 and last 28 characters from the soup_string
                soup_string = soup_string[16:-28]
                # If the substring defined above, exists in the soup_string then
                if substring in soup_string:
                    # Remove the first 104 characters
                    soup_string = soup_string[104:]
                # print (soup_string)
                # Write the PDF to URL in the file
                urls_file.write(soup_string+ '\n')

                # Get the XML file
                # Concatenate the static end of the XML file URL to the URL
                xmlFile = url + end_xml
                # Write the PDF to XML in the file
                xmls_file.write(xmlFile+ '\n')
