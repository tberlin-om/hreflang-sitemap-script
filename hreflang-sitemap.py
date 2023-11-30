import os
import csv
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from xml.dom import minidom

def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def split_large_sitemaps(root, threshold):
    count = len(root.findall('url'))
    sitemaps = []

    if count > threshold:
        while len(root):
            new_root = Element('urlset', {
                'xmlns': 'https://www.sitemaps.org/schemas/sitemap/0.9',
                'xmlns:xhtml': 'https://www.w3.org/1999/xhtml'
            })

            for _ in range(threshold):
                if len(root):
                    url_element = root[0]
                    root.remove(url_element)
                    new_root.append(url_element)

            sitemaps.append(new_root)

        return sitemaps
    else:
        return [root]

def generate_sitemap_from_csv(csv_file, threshold=20000):
    urlset = Element('urlset', {
        'xmlns': 'https://www.sitemaps.org/schemas/sitemap/0.9',
        'xmlns:xhtml': 'https://www.w3.org/1999/xhtml'
    })

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)

        for row in reader:
            for idx, url in enumerate(row):
                if url:
                    url_element = SubElement(urlset, 'url')
                    loc_element = SubElement(url_element, 'loc')
                    loc_element.text = url

                    alternate_count = 0

                    for sub_idx, alternate_url in enumerate(row):
                        if alternate_url and idx != sub_idx:
                            xhtml_element = SubElement(url_element, 'xhtml:link', {
                                'rel': 'alternate',
                                'hreflang': headers[sub_idx],
                                'href': alternate_url
                            })
                            alternate_count += 1

                    if alternate_count:
                        xhtml_element = SubElement(url_element, 'xhtml:link', {
                            'rel': 'alternate',
                            'hreflang': headers[idx],
                            'href': url
                        })
                    else:
                        urlset.remove(url_element)

    sitemaps = split_large_sitemaps(urlset, threshold)

    return sitemaps

output_dir = 'output/'
os.makedirs(output_dir, exist_ok=True)

sitemaps = generate_sitemap_from_csv('hreflang-data.csv')

for idx, sitemap in enumerate(sitemaps):
    sitemap_xml = prettify(sitemap)
    with open(f'output/hreflang_sitemap_{idx + 1}.xml', 'w', encoding='utf-8') as file:
        file.write(sitemap_xml)

print(f"{len(sitemaps)} Sitemaps wurden generiert!")
