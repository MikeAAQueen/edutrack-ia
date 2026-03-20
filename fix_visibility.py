import os
import glob

directory = r'd:\Projects\edutrack-ia\tables'
files_to_check = glob.glob(os.path.join(directory, '*.xs'))

for current_file in files_to_check:
    try:
        with open(current_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'visibility = "private"' in content:
            updated_content = content.replace('visibility = "private"', 'sensitive = true')
            with open(current_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Fixed visibility issue in {current_file}")
    except Exception as e:
        print(f"Failed to process {current_file}: {e}")
