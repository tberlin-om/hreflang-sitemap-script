import csv
import xml.etree.ElementTree as ET

csv_file_path = 'hreflang_data.csv'

output_base_name = 'hreflang_sitemap'
output_counter = 1

max_urls_per_sitemap = 20000

urlset = ET.Element('urlset', xmlns='https://www.sitemaps.org/schemas/sitemap/0.9')

url_count = 0

with open(csv_file_path, 'r', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    languages = next(csv_reader)
    
    for row in csv_reader:
        url = row[0]
        
        url_element = ET.SubElement(urlset, 'url')
        loc_element = ET.SubElement(url_element, 'loc')
        loc_element.text = url
        
        for i, lang_code in enumerate(languages[1:]):
            hreflang_url = row[i + 1]
            if hreflang_url and hreflang_url.strip():
                hreflang_element = ET.SubElement(url_element, 'xhtml:link', hreflang=lang_code, rel='alternate')
                hreflang_element.set('href', hreflang_url)
        
        url_count += 1
        
        if url_count >= max_urls_per_sitemap:
            output_file = f'{output_base_name}_{output_counter}.xml'
            tree = ET.ElementTree(urlset)
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            
            output_counter += 1
            
            urlset = ET.Element('urlset', xmlns='https://www.sitemaps.org/schemas/sitemap/0.9')
            
            url_count = 0

if url_count > 0:
    output_file = f'{output_base_name}_{output_counter}.xml'
    tree = ET.ElementTree(urlset)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f'Die hreflang-Sitemaps wurden erstellt.')
