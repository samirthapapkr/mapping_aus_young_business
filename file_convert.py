import os
import xml.etree.ElementTree as ET
import csv
import logging

# Create the CSVData directory if it doesn't exist
if not os.path.exists("CSVData"):
    os.makedirs("CSVData")

# Create the Mapping_Aus_log directory if it doesn't exist
if not os.path.exists("Mapping_Aus_log"):
    os.makedirs("Mapping_Aus_log")

# Configure logging settings
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.FileHandler(os.path.join("Mapping_Aus_log", "conversion.log")),
                        logging.StreamHandler()
                    ])

# Get a list of all XML files in the Aus_YB_Map_XMLData directory
xml_files = [f for f in os.listdir("Aus_YB_Map_XMLData") if f.endswith(".xml")]

# Process each XML file and convert to CSV
for xml_filename in xml_files:
    try:
        # Read the XML data from the current XML file
        with open(os.path.join("Aus_YB_Map_XMLData", xml_filename), "r") as xml_file:
            xml_data = xml_file.read()

        # Parse the XML data
        root = ET.fromstring(xml_data)

        # Create the CSV file for the current XML file
        csv_filename = os.path.join("CSVData", os.path.splitext(xml_filename)[0] + ".csv")
        with open(csv_filename, mode="w", newline="") as csv_file:
            fieldnames = ["ABN", "Status", "StatusFromDate", "EntityTypeInd", "EntityTypeText",
                          "NonIndividualNameText", "State", "Postcode", "GSTStatus", "GSTStatusFromDate"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            # Extract data from each ABR record and write to CSV
            for abr_record in root.findall('.//ABR'):
                writer.writerow({
                    "ABN": abr_record.findtext("ABN"),
                    "Status": abr_record.find("ABN").attrib.get("status", ""),
                    "StatusFromDate": abr_record.find("ABN").attrib.get("ABNStatusFromDate", ""),
                    "EntityTypeInd": abr_record.findtext("EntityType/EntityTypeInd"),
                    "EntityTypeText": abr_record.findtext("EntityType/EntityTypeText"),
                    "NonIndividualNameText": abr_record.find("LegalEntity/IndividualName/FamilyName").text if abr_record.find("LegalEntity/IndividualName/FamilyName") is not None else "",
                    "State": abr_record.findtext("LegalEntity/BusinessAddress/AddressDetails/State"),
                    "Postcode": abr_record.findtext("LegalEntity/BusinessAddress/AddressDetails/Postcode"),
                    "GSTStatus": abr_record.find("GST").attrib.get("status", ""),
                    "GSTStatusFromDate": abr_record.find("GST").attrib.get("GSTStatusFromDate", ""),
                })

        logging.info(f"CSV file '{csv_filename}' has been created.")
    except Exception as e:
        logging.error(f"Error while processing '{xml_filename}': {e}")

