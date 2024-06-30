import requests
from bs4 import BeautifulSoup
import csv


url = 'https://results.eci.gov.in/'  
response = requests.get(url)
if response.status_code == 200:
    page_content = response.text
else:
    print("Failed to retrieve the web page")
    exit()


soup = BeautifulSoup(page_content, 'html.parser')


title = soup.title.text.strip()
print(f"Title: {title}")


main_heading = soup.find('div', class_='page-title').h1.text.strip()
print(f"Main Heading: {main_heading}")


disclaimer = soup.find('div', class_='dis-info').p.text.strip()
print(f"Disclaimer: {disclaimer}")


sections = soup.find_all('div', class_='state-item')
links = []
for section in sections:
    state_name = section.h2.text.strip()
    num_constituencies = section.h1.text.strip()
    link = section.find('a')['href']
    if not link.startswith('http'):
        link = 'https://results.eci.gov.in/' + link  
    links.append({'Type': 'State', 'Name': state_name, 'Details': num_constituencies, 'Link': link})


additional_states = soup.find_all('a', class_='btn btn-big btn-primary')
for state in additional_states:
    state_name = state.text.strip()
    link = state['href']
    links.append({'Type': 'Additional State', 'Name': state_name, 'Details': '', 'Link': link})


footer = soup.find('footer')
app_links = footer.find_all('a', target='_blank')
for app_link in app_links:
    platform = app_link.img['alt'].split(' ')[0]  
    link = app_link['href']
    links.append({'Type': 'Mobile App', 'Name': platform, 'Details': '', 'Link': link})


csv_file = 'election_info.csv'


with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(['Title', title])
    writer.writerow(['Main Heading', main_heading])
    writer.writerow(['Disclaimer', disclaimer])
    writer.writerow([])
    writer.writerow(['Type', 'Name', 'Details', 'Link'])
    
    for link_info in links:
        writer.writerow([link_info['Type'], link_info['Name'], link_info['Details'], link_info['Link']])

print(f"Information successfully written to {csv_file}")
