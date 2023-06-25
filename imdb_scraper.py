import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as ChromeOptions
#from selenium.webdriver.edge.options import Options as EdgeOptions #Use whichever one works best for you.
import requests #To load page for BS4
from bs4 import BeautifulSoup
import pandas as pd
#from pathlib import Path #Use if your script or notebook isn't already within your working folder.
import time

options = ChromeOptions()
options.add_argument("--remote-allow-origins=*")
options.add_argument("user-agent=Mozilla/5.0")
driver = webdriver.Chrome(options=options)

#Path("imdb_reviews").mkdir(parents=True, exist_ok=True)
#Use if your script or notebook isn't already within your working folder.

urls = ["https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250",
       "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=251&ref_=adv_nxt",
       "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=501&ref_=adv_nxt",
       "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=751&ref_=adv_nxt"]
#IMDb Top 1000 list, 4 pages, 250 links per page.

def get_imdb_reviews(urls):
    title = []
    link = []
    genre = []

    for url in urls:
        driver.get(url)
        driver.implicitly_wait(1)
        block = driver.find_elements(By.CLASS_NAME, 'lister-item')
    
        for i in range(0, 250):
            try:
                ftitle = block[i].find_element(By.CLASS_NAME, 'lister-item-header').text
                forder = block[i].find_element(By.CLASS_NAME, 'lister-item-index').text
                ftitle = ftitle.replace(forder+' ', '')[:-7]
                flink = block[i].find_element(By.LINK_TEXT, ftitle).get_attribute('href')
                fgenre = block[i].find_element(By.CLASS_NAME, 'genre').text
        
                title.append(ftitle)
                link.append(flink)
                genre.append(fgenre)
        
                time.sleep(1)
            except:
                continue
        #Get initial materials for DataFrame and text files.
        
        user_review_links = []
        for url in link:
            url = url
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            review_link = 'https://www.imdb.com'+soup.find('a', text="User reviews").get('href')
            user_review_links.append(review_link)
        #Get user review needed to scrape review text.
        
        top_1000_data = {'movie_name': title,
                         'link': link,
                         'genre': genre,
                         'review_links': user_review_links}
        top_1000 = pd.DataFrame(data=top_1000_data)
        #Create DataFrame from which review links and materials for text files will be drawn.

        for i in range(len(top_1000["review_links"][i])):
            driver.get(top_1000["review_links"][i])
            driver.implicitly_wait(1)
            
            review = driver.find_elements(By.CLASS_NAME, 'review-container')
            content = []
            for n in range(0, 10):
                try:
                    fcontent = review[n].find_element(By.CLASS_NAME, 'content').get_attribute('textContent').strip()
                    content.append(fcontent)
                    
                    time.sleep(1) 
                except:
                    continue
            #Scrapes 10 reviews for every film on the list/within the DataFrame.
            #Note: If this section of the script stops before iterating through all links within the DataFrame,
            #Rerun this section of the script from the index position after the one it stopped on.
                
            movie = top_1000['movie_name'][i]
            genre = top_1000['genre'][i]
            for i in range(len(content)):
                try:
                    f = open(f'{movie}-{i+1}.txt', "x", encoding="utf-8")
                    f.write(f'{movie}\n')
                    f.write(f'genre: {genre}\n')
                    f.write(f'review: {content[i]}')
                    f.close()
                except:
                    continue
            #Takes the review text, along with the titles and genres of the movies,
            #and writes them into text files.

            top_1000.to_csv("top_1000.csv")

driver.quit()