from lxml import etree
import sys

def find_duplicates(xml_file, content_value=None):
    # Parse the XML file
    tree = etree.parse(xml_file)
    root = tree.getroot()
    print('running find duplicates')
    # Dictionary to track seen entries and their line numbers
    seen_entries = {}
    duplicates = []

    # Find all profileActionOverrides nodes using findall
    entries = root.findall(".//profileActionOverrides")

    for entry in entries:
        # Extract the values of formFactor, recordType, profile, and content
        form_factor = entry.find('formFactor').text
        record_type = entry.find('recordType').text
        profile = entry.find('profile').text
        content = entry.find('content').text

        # If content_value is specified, filter by content
        if content_value and content != content_value:
            continue  # Skip this entry if content doesn't match

        # Create a tuple key based on formFactor, recordType, profile
        entry_key = (form_factor, record_type, profile)

        # Get the line number for this entry
        line_number = entry.sourceline

        # Check if this entry has been seen before
        if entry_key in seen_entries:
            # If duplicate, store both the current and previous entries
            duplicates.append((entry, seen_entries[entry_key]['line_number']))
        else:
            seen_entries[entry_key] = {'entry': entry, 'line_number': line_number}

    # If duplicates were found, print the results
    if duplicates:
        print(f"Found {len(duplicates)} duplicate entries with content '{content_value}':")
        for duplicate, original_line in duplicates:
            # Print the line numbers and the duplicate XML entries
            print(f"Duplicate found at line {duplicate.sourceline}, original entry at line {original_line}")
            print(etree.tostring(duplicate, pretty_print=True, encoding='unicode'))
            print("-" * 50)  # Separator for readability
    else:
        print(f"No duplicates found with content '{content_value}'.")

if __name__ == "__main__":
    # Replace 'input_file.xml' with the path to your XML file
    #  if sys.argv[1:]:
    #     if sys.argv[1] == "-f" and sys.argv[2]:
    #         xml_file = sys.argv[2]  # Update this to the correct file path
    #         if sys.argv[3] == "--content":
    #             content_value = sys.argv[4]  # Set the value you want to filter for
    #             find_duplicates(xml_file, content_value)
    #  else:
    xml_file = 'test.xml'
    content_value = 'CTP_MVP_Lead_Page'
    find_duplicates(xml_file, content_value)