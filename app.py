# IMport all the required libraries and methods
from flask import Flask, render_template, request, redirect, flash, url_for
from .forms import *
import urllib.request 
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup,SoupStrainer
import requests
import validators
import json
import re
import itertools
from .index import *
from scholarly import scholarly
from urllib.request import urlopen
from flask_apscheduler import APScheduler
from .pages import pages
from scholarly import ProxyGenerator

# Iniatalise the flask app and the scheduler
app = Flask(__name__)
app.secret_key = '67eadccda3bc198f2b9712c77912bd55'
scheduler = APScheduler()
#Proxy from scholary

# pg = ProxyGenerator()
# pg.FreeProxies()
# scholarly.use_proxy(pg)

@app.route("/profiles",methods=("GET", "POST"), strict_slashes=False)
def index():
    try:
        #A list to store all the author data
        authorpack = list()
        #Start a loop through each of the three pages,for each page perform a crawl and append data
        #to the authorpack list
        for page in pages:
            #Assign a url to a variable requested url
            requested_url = page
            # Print each page url for demo purposes
            print(requested_url)
            #Convert urls to text for beautful soup to parse
            source = requests.get(requested_url).text
            # Convert all the contents of each url to lxml format
            soup = BeautifulSoup(source, 'lxml')
            #From the page contents,extract only divs with a class gsc_1usr,
            #At this point we have several divs that match the given class name
            authors = soup.findAll('div', attrs={'class':'gsc_1usr'})
            #Url segment to embedd to all relative image paths
            imgUrl = 'https://scholar.googleusercontent.com'
            #Url segment to embedd to all relative profile paths
            profileUrl = 'https://scholar.google.com'
            #Loop through each author package and for each extract all the information avaialable info
            for author in authors:
                author_image = author.find('img')
                author_image = author_image["src"]
                #Validate image path using validators
                valid_imgpath = validators.url(author_image)
                #If it's valid,assign it to the image variable,else join to the imgUrl to form a complete path
                if valid_imgpath == True:
                    author_image = author_image
                else:
                    full_path = urljoin(imgUrl, author_image)
                    author_image =full_path

                author_name = author.find('h3').text
                print(author_name)
                profile_link = author.select('.gs_ai_name a')
                profile_link = profileUrl + profile_link[0]['href']
                author_affiliation = author.find("div", {"class": "gs_ai_aff"}).text
                author_email = author.find("div", {"class": "gs_ai_eml"}).text
                author_citations = author.find("div", {"class": "gs_ai_cby"}).text
                author_tags = author.find("div", {"class": "gs_ai_int"}).text
                
                #To fetch all the papers from each author ,we again parse the authors profile links
                r = requests.get(profile_link).text
                aProfile = BeautifulSoup(r,"html.parser")
                #Find all paper links using the 'a' tag
                papers = aProfile.find_all('a', class_='gsc_a_at')
                #A list to store all the papers
                paperpack = []
                #Loop through each paper and then convert to text
                for paper in papers:
                    paperpack.append(paper.text)
                #Assign all the paper details to a single variable for proper and organised storage
                x = (author_image,author_name,profile_link,author_affiliation,author_email,author_citations,author_tags,papers,index)
                #Now add them to the list in line 33
                authorpack.append(x)
        #After the loop return a template and populate it with the results
        return render_template("index.html",authorpack=authorpack,title="GS-Crawler | Profiles")

        
    #Catch errors from blocked connections    
    except requests.exceptions.ConnectionError:
        flash(f"Connection Refused !", "danger")
    #Default route template
    return render_template("index.html",title="GS-Crawler | Profiles")

@app.route("/",methods=("GET", "POST"), strict_slashes=False)
def search():
    #Flask form to render the text field
    form = Url()
    #Get the value a user types in the search bar
    query = request.form.get('text')
    try:
        #If the query is not empty,proceed
        if query:
            #A list of the urls to be crawled,we only use one for demo purposes
            q_pages = ['http://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q='+query,
            # 'https://scholar.google.com/scholar?start=20&q=' +query +'&hl=en&as_sdt=0,5',
            # 'https://scholar.google.com/scholar?start=30&q=' +query +'&hl=en&as_sdt=0,5',
            # 'https://scholar.google.com/scholar?start=40&q=' +query +'&hl=en&as_sdt=0,5',
            ]
            #Loop through all the available pages 
            for r_page in q_pages:
                ##Assign each page a a loop level to the url variable
                requested_url = r_page
                #Show on the terminal the url being crawled
                print('Crawling page ....',requested_url)
                #G.scholar base url
                baseUrl = 'https://scholar.google.com'
                #Bs4 default url parsing method
                #Convert url to text
                source = requests.get(requested_url).text
                #Convert page contents to lxml format
                soup = BeautifulSoup(source, 'lxml')
                #Fetch all divs with a class name gs_ri
                articles = soup.findAll('div', attrs={'class':'gs_ri'})
                #Author ids list,used to filter only required authos
                author_ids = list()
                #A list to store all the articles and their data
                articlepack = list()
                #Loop through each article,fetch all relevant info
                for article in articles:
                    title = article.find('h3').text
                    paper_link = article.select('.gs_rt a')
                    paper_link = paper_link[0]['href']
                    author = article.find("div", {"class": "gs_a"}).text
                    abstract =article.find("div",{"class" : "gs_rs"}).text
                    extra = article.find("div",{"class" : "gs_fl"}).text
                    citations = article.select('.gs_fl a:nth-of-type(3)')
                    citations = baseUrl + citations[0]['href']
                    related = article.select('.gs_fl a:nth-of-type(4)')
                    related = baseUrl + related[0]['href']
                    # Show only results with atleast one author from CU
                    # Search publication by title,Then fetch the author ID
                    p_title = scholarly.search_pubs(title)
                    p_title = next(p_title)
                    # Process Author ID
                    a_id = p_title['author_id']
                    author_ids.append(a_id)

                    for id in a_id:
                        if id:
                            individual_id = id
                            # Author id extracted,check if author/coauthor is from CU
                            f_author = scholarly.search_author_id(individual_id)
                            #Extract email domain from author container
                            f_author_email = f_author['email_domain']
                            print(f_author_email)
                            if f_author_email == '@coventry.ac.uk':
                                # flash(f"At least one Coauthor is from CU !", "info")
                                pack = (title,paper_link,author,abstract,extra,citations,related)
                                articlepack.append(pack)
                            # else:
                            #     flash(f"No Coauthor is not from CU !", "danger")
                # print(author_ids)
            return render_template("results.html",form=form,articlepack=articlepack,title="GS-Crawler | Search")
    except requests.exceptions.ConnectionError:
        flash(f"Connection Refused !", "danger")


    return render_template("search.html",form=form,title="GS-Crawler | Search")

    if __name__ == "__main__":
        #Schedule the crwler to run with the flask app,automate to crawl after every 3 days
        scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval", days=3)
        scheduler.start()
        app.run(debug=True)
