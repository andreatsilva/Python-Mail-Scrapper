import requests
from bs4 import BeautifulSoup
import re
import argparse


def scrape_emails(url):
    # Send a GET request to the website
    response = requests.get(url, verify=False)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all text that matches an email pattern
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        emails = set(re.findall(email_pattern, soup.get_text()))
        
        return emails
    else:
        print(f"Failed to retrieve the content from {url}")
        return None

def scrape_emails_from_file(input_file):
    with open(input_file, 'r') as file:
        urls = file.readlines()

    extracted_emails = set()
    for url in urls:
        url = url.strip()
        scraped_emails = scrape_emails(url)
        if scraped_emails:
            extracted_emails.update(scraped_emails)

    return extracted_emails

def save_emails_to_file(emails, output_file):
    with open(output_file, 'w') as file:
        for email in emails:
            file.write(email + '\n')

def main():
    input_file = input("Enter the path to the input file containing a list of URLs: ")
    output_file = input("Enter the path for the output file to save the extracted emails: ")

    extracted_emails = scrape_emails_from_file(input_file)

    if extracted_emails:
        save_emails_to_file(extracted_emails, output_file)
        print(f"Scraped emails saved to {output_file}")
    else:
        print("No emails were scraped.")

if __name__ == "__main__":
    main()