from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def get_user_input():
    username = input("Enter Instagram username: ")
    print("Search for:")
    print("1. Comments only")
    print("2. Likes only")
    print("3. Both comments and likes")
    choice = int(input("Enter your choice (1-3): "))
    return username, choice

def scrape_reels(username, search_choice):
    url = f"https://www.instagram.com/{username}/reels/"
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")
    reel_links = [a['href'] for a in soup.find_all('a', href=True) if "/reel/" in a['href']]
    
    for reel_link in reel_links:
        full_link = f"https://www.instagram.com{reel_link}"
        driver.get(full_link)
        time.sleep(3)
        reel_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        if search_choice == 1:
            comments = reel_soup.find_all('span', class_='comment-item')
            for comment in comments:
                if username in comment.text:
                    store_link(full_link)
                    
        elif search_choice == 2:
            likes = reel_soup.find_all('div', class_='like-indicator-class')
            if likes:
                store_link(full_link)
                
        elif search_choice == 3:
            comments = reel_soup.find_all('span', class_='comment-item')
            liked = False
            for comment in comments:
                if username in comment.text:
                    store_link(full_link)
                    break
            if not liked and 'like-indicator-class' in reel_soup.text:
                store_link(full_link)

    driver.quit()

def store_link(link):
    with open("liked_commented_reels.txt", "a") as f:
        f.write(link + "\n")

def main():
    username, search_choice = get_user_input()
    try:
        scrape_reels(username, search_choice)
        print("Reel links with your interaction stored successfully!")
    except Exception as e:
        print(f"Error encountered: {e}")

if __name__ == "__main__":
    main()
