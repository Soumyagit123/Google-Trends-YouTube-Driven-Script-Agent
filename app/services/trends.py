import xml.etree.ElementTree as ET
import urllib.request

def fetch_trends(country: str) -> list:
    country_map = {
        "IN": "IN",
        "US": "US",
        "UK": "GB"
    }

    geo = country_map.get(country.upper(), "US")
    url = f"https://trends.google.com/trending/rss?geo={geo}"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req)
    xml_data = resp.read()
    
    root = ET.fromstring(xml_data)
    trends = []
    for item in root.findall('.//item/title')[:10]:
        if item.text:
            trends.append(item.text)
            
    return trends
