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
        
        hreflang_entries = 0
        for i, lang_code in enumerate(languages[1:]):
            hreflang_url = row[i + 1]
            if hreflang_url and hreflang_url.strip():
                hreflang_element = ET.SubElement(url_element, 'xhtml:link', hreflang=lang_code, rel='alternate')
                hreflang_element.set('href', hreflang_url)
                hreflang_entries += 1
                
        if hreflang_entries > 0:
            pretty_print(urlset)
            
            output_file = f'{output_folder}/{output_base_name}_{output_counter}.xml'
            tree = ET.ElementTree(urlset)
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            
            sitemap_file = open(output_file, 'r', encoding='utf-8')
            sitemap_contents = sitemap_file.read()
            sitemap_file.close()
            
            sitemap_contents = '<?xml version="1.0" encoding="UTF-8"?>\n' + sitemap_contents
            sitemap_contents = '<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9" ' \
                               'xmlns:xhtml="https://www.w3.org/1999/xhtml">\n' + sitemap_contents
            sitemap_contents += '</urlset>\n'
            
            sitemap_file = open(output_file, 'w', encoding='utf-8')
            sitemap_file.write(sitemap_contents)
            sitemap_file.close()
            
            url_count += 1
            if url_count >= max_urls_per_sitemap:
                url_count = 0
                output_counter += 1
                urlset.clear()

if url_count > 0:
    pretty_print(urlset)
    
    output_file = f'{output_folder}/{output_base_name}_{output_counter}.xml'
    tree = ET.ElementTree(urlset)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f'Die hreflang-Sitemaps wurden im Ordner "{output_folder}" erstellt.')
