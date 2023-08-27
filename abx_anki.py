import csv

# Open the original CSV file
input_csv_path = "original_table.csv"  # Update with your file path
output_csv_path = "anki_import.csv"    # Path for the Anki import CSV

def replace_effectiveness(value):
    replacements = {
        "8:": "May be active:",
        "9:": "Likely active:",
        "0:": "Likely not active:",
        "8": "May be active",
        "9": "Likely active",
        "0": "Likely not active"
    }
    
    for key, replacement in replacements.items():
        if value.startswith(key):
            return replacement + value[len(key):]
    
    return value

try:
    with open(input_csv_path, 'r') as input_file:
        csv_reader = csv.reader(input_file)
        
        # Read the first row to get bact names
        bacts = next(csv_reader)[1:]
        
        # Create or open the output CSV file
        with open(output_csv_path, 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            
            # Iterate through the remaining rows
            for abx, *effectiveness in csv_reader:
                for bact, effectiveness_value in zip(bacts, effectiveness):
                    updated_effectiveness = replace_effectiveness(effectiveness_value)
                    
                    # Format the front and back values
                    front_value = f"Is {abx} active against {bact}?"
                    
                    # Applying color based on effectiveness
                    color = ""
                    if updated_effectiveness.startswith("Likely active"):
                        color = "green"
                    elif updated_effectiveness.startswith("Likely not active"):
                        color = "red"
                    elif updated_effectiveness.startswith("May be active"):
                        color = "darkgoldenrod"  # Dark yellow color
                        
                    back_value = f'<font color="{color}">{updated_effectiveness}</font>'
                    
                    csv_writer.writerow([front_value, back_value])
                    
except FileNotFoundError:
    print("Input file not found:", input_csv_path)
