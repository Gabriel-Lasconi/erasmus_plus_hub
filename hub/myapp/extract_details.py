import spacy
import requests

nlp = spacy.load("en_core_web_lg")

# List of European countries
european_countries = [
    "Greece", "Bulgaria", "Czech Republic", "Latvia", "Spain", "Netherlands",
    "Austria", "France", "Italy", "Germany", "Hungary", "Poland", "Portugal",
    "Slovakia", "Sweden", "Finland", "Estonia", "Lithuania", "Belgium",
    "Ireland", "Denmark", "Cyprus", "Malta", "Luxembourg", "Slovenia",
    "Romania", "Croatia", "Georgia", "Turkey", "Armenia"
]

# Function to validate city names using OpenStreetMap Nominatim API
def is_valid_city(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return True  # City found
    return False

# Function to extract the most likely location (city and country) from text
def extract_location(text):
    """Extracts city and country from the given text."""
    doc = nlp(text)
    city = None
    country = None

    # Extract geopolitical entities (GPEs) using spaCy
    gpes_and_locs = [ent.text for ent in doc.ents if ent.label_ in {"GPE", "LOC"}]


    # Process GPEs to identify city and country
    for gpe in gpes_and_locs:
        if gpe in european_countries:
            country = gpe  # Match a valid country

    for gpe in gpes_and_locs:
        print(gpe)
        if(gpe != country):
            city = gpe  # Match a valid city

    return city, country

# Function to extract general project information
def extract_general_information(message):
    # Extract location
    city, country = extract_location(message)

    # Extract project type
    type_keywords = ["training course", "youth exchange"]
    type_match = next(
        (keyword.title() for keyword in type_keywords if keyword in message.lower()),
        None
    )

    # Generate project name dynamically
    if type_match and city and country:
        name = f"{type_match} in {city}, {country}"
    elif type_match and country:
        name = f"{type_match} in {country}"
    else:
        name = "Unknown Project"

    # Extract dates using spaCy
    entities = extract_entities(message)
    dates = entities["dates"]

    return {
        "Name": name,
        "Country": country or "Unknown",
        "City": city or "Unknown",
        "Type": type_match or "Unknown",
        "Dates": dates if dates else ["Unknown"]
    }

# Function to extract entities like dates
def extract_entities(text):
    """Use spaCy to extract entities like dates."""
    doc = nlp(text)
    entities = {"dates": []}

    for ent in doc.ents:
        if ent.label_ == "DATE":
            entities["dates"].append(ent.text)

    return entities

# Test with sample messages
message1 = """
🚀 Open Call for the training course Erasmus+ Explorer Training and Synergies
📅 Dates: January 17 - 27, 2025 (including travel days)
📍 Location: Bordeaux, France
🇪🇺 Accommodation & food are fully covered by Erasmus budget! ✈ Travel cost is covered by up to 417 EUROS for a round trip)
"""

message2 = """
This one also i am helping to find participants
——————————
🌍 URGENT CALL FOR PARTICIPANTS: Fully Funded Erasmus+ Training Course in Austria! 🌍
📅 Dates: November 17-25, 2024 
🌍 Location: Drienica, Austria 
"""

message3 = """
Open call for participants from Greece 🇬🇷 Bulgaria 🇧🇬 Czech Republic 🇨🇿 Latvia 🇱🇻 Spain 🇪🇸 Netherlands 🇳🇱

Training course Water to the moon
Open to Youth workers 18+

📅 9-17 Jan 2025 (arrival & departure incl)
📍 Habri, Czech Republic
"""
message4 = """ 

http://Linktr.ee/ywb_nl

🇬🇪Youth Exchange
Green Generation
22 November - 1 December 
Kobuleti 
Georgia 🇬🇪
https://forms.gle/eE9K7gZZ8prKxcAb7

"""

# Results
result1 = extract_general_information(message1)
result2 = extract_general_information(message2)
result3 = extract_general_information(message3)
result4 = extract_general_information(message4)

print("Result 1:", result1)
print("Result 2:", result2)
print("Result 3:", result3)
print("Result 4:", result4)
