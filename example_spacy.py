import requests
from bs4 import BeautifulSoup

# Load spaCy's German model
import spacy
nlp = spacy.load('de_core_news_sm')

# Define the URL of the website you want to scrape
url = 'https://www.arbeitsagentur.de/familie-und-kinder/kinderzuschlag-verstehen/kinderzuschlag-anspruch-hoehe-dauer'

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the request with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract content from specific HTML elements (modify selectors as necessary)
    eligibility_conditions = []
    for p in soup.select('div.edi-text p'):
        text = p.get_text(strip=True)
        eligibility_conditions.append(text)

    # Print extracted conditions
    for condition in eligibility_conditions:
        print(condition)

    # Define SHACL shapes
    shapes_template = """
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.org/> .

ex:EligibilityShape a sh:NodeShape ;
    sh:targetClass ex:Person ;
    sh:property [
        sh:path ex:condition ;
        sh:description "{description}" ;
    ] .
"""

    # Convert conditions to SHACL format
    shacl_shapes = ""
    for i, condition in enumerate(eligibility_conditions, start=1):
        shape = shapes_template.replace("{description}", condition)
        shacl_shapes += shape

    # Save to a file
    with open('eligibility_conditions_shacl.ttl', 'w', encoding='utf-8') as file:
        file.write(shacl_shapes)

    print("SHACL shapes created successfully!")
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
