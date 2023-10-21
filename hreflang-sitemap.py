import csv
import xml.etree.ElementTree as ET
import os

def pretty_print(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            pretty_print(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

csv_file_path = 'hreflang-data.csv'
output_folder = 'output'
output_base_name = 'hreflang_sitemap'
output_counter = 1
max_urls_per_sitemap = 20000
urlset = ET.Element('urlset', xmlns='https://www.sitemaps.org/schemas/sitemap/0.9', 
                    attrib={'xmlns:xhtml': 'https://www.w3.org/1999/xhtml'})

url_count = 0

with open(csv_file_path, 'r', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    languages = next(csv_reader)
    
    for row in csv_reader:
        url_element = ET.Element('url')
        primary_url = row[0]
        primary_lang = languages[0]
        
        # Check if there's at least one alternate URL
        has_alternate = any(row[1:])
        
        if not has_alternate:
            continue
        
        loc_element = ET.SubElement(url_element, 'loc')
        loc_element.text = primary_url
        
        primary_hreflang = ET.SubElement(url_element, 'xhtml:link', hreflang=primary_lang, rel='alternate', href=primary_url)
        
        for i, lang_code in enumerate(languages[1:]):
            hreflang_url = row[i + 1]
            if hreflang_url and hreflang_url.strip():
                hreflang_element = ET.SubElement(url_element, 'xhtml:link', hreflang=lang_code, rel='alternate', href=hreflang_url)

        urlset.append(url_element)
        url_count += 1
        if url_count >= max_urls_per_sitemap:
            pretty_print(urlset)
            
            output_file = f'{output_folder}/{output_base_name}_{output_counter}.xml'
            tree = ET.ElementTree(urlset)
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            
            url_count = 0
            output_counter += 1
            urlset.clear()

if url_count > 0:
    pretty_print(urlset)
    
    output_file = f'{output_folder}/{output_base_name}_{output_counter}.xml'
    tree = ET.ElementTree(urlset)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f'Die hreflang-Sitemaps wurden im Ordner "{output_folder}" erstellt.')
