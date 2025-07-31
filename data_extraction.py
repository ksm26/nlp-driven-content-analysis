import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Set up Selenium WebDriver with headless Chrome."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def clean_text(text):
    """Format text to preserve paragraph breaks."""
    return '\n\n'.join([para.strip() for para in text.split('\n') if para.strip()])

def extract_article_text(driver, url):
    """Fetch and extract article title and main text from a given URL using Selenium."""
    try:
        driver.get(url)
        time.sleep(3)  # Allow time for JavaScript to load content
        
        # Extract title (modify selector based on actual website structure)
        title_element = driver.find_element(By.TAG_NAME, 'h1')
        title_text = title_element.text.strip() if title_element else "No Title Found"
        
        # Extract main article content while avoiding ads, side links, and repeated titles
        try:
            article_body_element = driver.find_element(By.CLASS_NAME, 'td-post-content')  # Main article container
        except:
            return "No Content Found"
        
        # Remove unwanted elements like ads, side links, navigation, etc.
        for unwanted in article_body_element.find_elements(By.CLASS_NAME, 'td-a-rec'):
            driver.execute_script("arguments[0].remove();", unwanted)
        for unwanted in article_body_element.find_elements(By.CLASS_NAME, 'td_block_wrap'):
            driver.execute_script("arguments[0].remove();", unwanted)
        for unwanted in article_body_element.find_elements(By.CLASS_NAME, 'td-post-sharing'):
            driver.execute_script("arguments[0].remove();", unwanted)
        for unwanted in article_body_element.find_elements(By.CLASS_NAME, 'td-post-next-prev'):
            driver.execute_script("arguments[0].remove();", unwanted)
        
        # Extract main content including headings, paragraphs, lists, and links
        content_elements = article_body_element.find_elements(By.XPATH, "./*[(self::h1 or self::h2 or self::h3 or self::p or self::ul/li or self::ol/li or self::a)]")
        
        extracted_content = []
        last_heading = None
        for elem in content_elements:
            if elem.tag_name in ['h1', 'h2', 'h3']:
                if last_heading:
                    extracted_content.append("\n\n")  # Ensure spacing before new section
                last_heading = f"**{elem.text.strip()}**"
                extracted_content.append(f"\n\n{last_heading}\n")  # Bold section title with extra spacing
            elif elem.tag_name == 'a':
                extracted_content.append(f"[Link: {elem.get_attribute('href')}]")  # Capture hyperlinks
            elif elem.tag_name in ['ul', 'ol', 'li']:
                extracted_content.append(f"- {elem.text.strip()}")  # Capture ordered and unordered lists
            else:
                extracted_content.append(elem.text.strip())
        
        # Special handling for Solution Architecture links
        solution_architecture_link = driver.find_elements(By.XPATH, "//h1[contains(text(), 'Solution Architecture')]/following-sibling::figure//div[contains(@class, 'wp-block-embed__wrapper')]")
        if solution_architecture_link:
            extracted_content.append(f"\n\n**Solution Architecture Link:** {solution_architecture_link[0].text.strip()}\n")
        
        article_text = clean_text('\n\n'.join(extracted_content)) if extracted_content else "No Content Found"
        
        return f"{title_text}\n\n{article_text}"
    except Exception as e:
        return f"Error extracting article: {str(e)}"

def save_article(url_id, text):
    """Save extracted text to a properly formatted .txt file inside 'extracted_articles' folder."""
    output_folder = "extracted_articles"
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it does not exist
    filename = os.path.join(output_folder, f"{url_id}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("\n" + text + "\n")  # Ensure proper formatting with newlines
    print(f"Saved: {filename}")

def main():
    """Main function to read input, extract text, and save it."""
    input_file = 'Input.xlsx'  # Ensure the file exists
    if not os.path.exists(input_file):
        print("Error: input.xlsx not found!")
        return
    
    df = pd.read_excel(input_file)
    driver = setup_driver()
    
    for _, row in df.iterrows():
        url_id, url = row['URL_ID'], row['URL']
        print(f"Processing: {url_id} -> {url}")
        article_text = extract_article_text(driver, url)
        save_article(url_id, article_text)
    
    driver.quit()

if __name__ == "__main__":
    main()
