import json

def read_json(file_path):
    """Reads a JSON file and returns the parsed content."""
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_json(json1, json2):
    """Compares two JSON objects and returns the differences in a human-readable format."""
    diff = []
    
    # Compare all keys in both JSON objects
    all_keys = set(json1.keys()).union(set(json2.keys()))
    
    for key in all_keys:
        value1 = json1.get(key, None)
        value2 = json2.get(key, None)
        
        if value1 != value2:
            diff.append(f"{key}: {value1} >> {value2}")
    
    return diff

def write_markdown(diff, output_file):
    """Writes the differences into a markdown file."""
    with open(output_file, 'w') as file:
        file.write(f"## JSON File Comparison\n\n")
        for line in diff:
            file.write(f"{line}\n")
    
    print(f"Markdown file with differences saved to {output_file}")

def compare_json_files(file1, file2, output_file):
    """Reads two JSON files, compares them, and outputs the difference to a markdown file."""
    json1 = read_json(file1)
    json2 = read_json(file2)
    
    diff = compare_json(json1, json2)
    write_markdown(diff, output_file)

# Example Usage
file1 = 'path_to_first_json_file.json'
file2 = 'path_to_second_json_file.json'
output_file = 'comparison_output.md'

compare_json_files(file1, file2, output_file)
