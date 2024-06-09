import os
import csv

folder_path = r'C:\Users\derek\OneDrive\Desktop\Shadbase\www.shadbase.com'
comic_name = 'comic-1'

for folder in os.listdir(folder_path):
    folder_dir = os.path.join(folder_path, folder)
    if os.path.isdir(folder_dir):
        index_path = os.path.join(folder_dir, 'index.html')
        if os.path.isfile(index_path):
            with open(index_path, 'r', encoding='utf-8') as file:
                content = file.read()
                try:
                    img_src = content.split(f'{comic_name}')[1].split('src="')[1].split('"')[0]
                    img_src = img_src.replace('../comic_folder/', '')
                    #print(f'Image source for {comic_name} in {folder}: {img_src}')
                    entry_start = '<div class="entry">'
                    entry_end = '<div class="clear"></div>'

                    entry_start_index = content.find(entry_start)
                    entry_end_index = content.find(entry_end, entry_start_index)

                    if entry_start_index != -1 and entry_end_index != -1:
                        entry_content = content[entry_start_index + len(entry_start):entry_end_index].strip()
                        csv_path = r'C:\Users\derek\OneDrive\Desktop\Shadbase\wp_posts.csv'
                        with open(csv_path, 'r+', encoding='utf-8') as csv_file:
                            csv_reader = csv.reader(csv_file)
                            rows = list(csv_reader)
                            for row in rows:
                                if folder in row[11]:
                                    print(row[0])  # Print the row number
                                    print(row[4])
                                    row[4] = entry_content
                                    csv_writer = csv.writer(csv_file)
                                    csv_writer.writerows(rows)
                    else:
                        print(f'Entry not found for {comic_name} in {folder}')
                except IndexError as e:
                    with open('error.log', 'a') as error_file:
                        error_file.write(f'Error: {e}\n')