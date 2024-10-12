import requests
import whois
import json
from datetime import datetime
import dns.resolver

def log_redirects(url):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
    }
    response = session.get(url, headers=headers, allow_redirects=True)
    redirects = response.history
    print(f"Redirects for {url}:")
    for i, redirect in enumerate(redirects):
        print(f"{i + 1}. {redirect.url} - {redirect.status_code}")
    print(f"Final URL: {response.url} - {response.status_code}")

    # Add the final URL to the redirects list
    redirects.append(response)

    return redirects

def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        provider = w.registrar or w.org or w.name or "Unknown"
        dig_result = dns.resolver.resolve(domain, 'A')
        dig_info = [str(ip) for ip in dig_result]
        whois_dig_info = [whois.whois(ip) for ip in dig_info]
        return {
            'provider': provider,
            'dig_result': dig_info,
            'whois_dig_result': [str(info) for info in whois_dig_info]
        }
    except Exception as e:
        return str(e)

def build_json_map(redirects):
    relations = []
    for response in redirects:
        domain = response.url.split('/')[2]
        whois_info = whois_lookup(domain)
        relations.append({
            'url': response.url,
            'status_code': response.status_code,
            'whois': convert_to_serializable(whois_info)
        })
    return relations

def convert_to_serializable(data):
    if isinstance(data, dict):
        return {k: convert_to_serializable(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_serializable(i) for i in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data

def main():
    url = input("Enter the URL to check for redirects: ")
    redirects = log_redirects(url)
    json_map = build_json_map(redirects)
    with open('redirects_map.json', 'w') as f:
        json.dump(json_map, f, indent=4)
    print("Redirects map saved to redirects_map.json")

if __name__ == "__main__":
    main()