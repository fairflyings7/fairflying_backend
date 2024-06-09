import json

# Read the data from the text file
try:
    with open('./hotel_city_code.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
except:
    with open('backend/Flight_API/hotel_city_code.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

# Skip the header line and initialize the dictionary
airport_dict = []

# Process each line to extract the relevant information
for line in lines[1:]:
    # Remove parentheses and single quotes
    line = line.replace('(', '').replace(')', '').replace("'", "").strip()
    # Split the line by commas
    parts = line.split(', ')
    # Extract the needed values
    airport_code = parts[1]
    airport_name = parts[2]
    airport_city_name = parts[3]
    airport_country_name = parts[5]
    airport_country_code = parts[6][:-1]

    data = {}
    # Create the dictionary entry
    data["label"] = f"{airport_city_name}, {airport_country_name}, {airport_name}"
    data["code"] = f"{airport_code}"
    data["countryCode"] = f"{airport_country_code}"
    airport_dict.append(data)


# Write the dictionary to a JSON file
with open('hotels_output.json', 'w') as json_file:
    json.dump(airport_dict, json_file, indent=4)

print("Data has been processed and stored in script.json")
