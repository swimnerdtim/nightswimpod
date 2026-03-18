#!/usr/bin/env python3
"""
Google Search Console API Manager
Uses existing Google OAuth credentials to manage Search Console
"""

import json
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime

# Search Console API scope
SCOPES = ['https://www.googleapis.com/auth/webmasters']

CRED_FILE = '/Users/tim/.openclaw/credentials/youtube-tokens-nightswim.json'
SEARCH_CONSOLE_CRED_FILE = '/Users/tim/.openclaw/credentials/search-console-tokens.json'

def get_credentials():
    """Get or create Search Console API credentials"""
    creds = None
    
    # Check if we already have Search Console credentials
    if os.path.exists(SEARCH_CONSOLE_CRED_FILE):
        with open(SEARCH_CONSOLE_CRED_FILE, 'r') as f:
            creds_data = json.load(f)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
    
    # If no valid credentials, try to use YouTube credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Load YouTube credentials and create new flow
            with open(CRED_FILE, 'r') as f:
                youtube_creds = json.load(f)
            
            client_config = {
                "installed": {
                    "client_id": youtube_creds["client_id"],
                    "client_secret": youtube_creds["client_secret"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            }
            
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Save the credentials for future use
        with open(SEARCH_CONSOLE_CRED_FILE, 'w') as f:
            f.write(creds.to_json())
    
    return creds

def get_service():
    """Get Search Console API service"""
    creds = get_credentials()
    return build('searchconsole', 'v1', credentials=creds)

def list_sites():
    """List all sites in Search Console"""
    service = get_service()
    sites = service.sites().list().execute()
    return sites.get('siteEntry', [])

def get_sitemaps(site_url):
    """Get all sitemaps for a site"""
    service = get_service()
    sitemaps = service.sitemaps().list(siteUrl=site_url).execute()
    return sitemaps.get('sitemap', [])

def submit_sitemap(site_url, sitemap_url):
    """Submit a sitemap"""
    service = get_service()
    service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
    print(f"✅ Submitted sitemap: {sitemap_url}")

def delete_sitemap(site_url, sitemap_url):
    """Delete a sitemap"""
    service = get_service()
    service.sitemaps().delete(siteUrl=site_url, feedpath=sitemap_url).execute()
    print(f"🗑️ Deleted sitemap: {sitemap_url}")

def inspect_url(site_url, inspect_url):
    """Inspect a URL (check indexing status)"""
    service = get_service()
    result = service.urlInspection().index().inspect(
        body={
            'inspectionUrl': inspect_url,
            'siteUrl': site_url
        }
    ).execute()
    return result

def request_indexing(site_url, url):
    """Request indexing for a URL"""
    service = get_service()
    # Note: This uses URL Inspection API to check, then requests indexing if needed
    result = inspect_url(site_url, url)
    print(f"📊 Indexing status for {url}:")
    print(json.dumps(result, indent=2))
    return result

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 search_console_manager.py list-sites")
        print("  python3 search_console_manager.py list-sitemaps <site_url>")
        print("  python3 search_console_manager.py submit-sitemap <site_url> <sitemap_url>")
        print("  python3 search_console_manager.py delete-sitemap <site_url> <sitemap_url>")
        print("  python3 search_console_manager.py inspect <site_url> <url>")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == 'list-sites':
        sites = list_sites()
        print("🌐 Sites in Search Console:")
        for site in sites:
            print(f"  - {site['siteUrl']} ({site.get('permissionLevel', 'unknown')})")
    
    elif action == 'list-sitemaps':
        site_url = sys.argv[2]
        sitemaps = get_sitemaps(site_url)
        print(f"📄 Sitemaps for {site_url}:")
        for sitemap in sitemaps:
            print(f"  - {sitemap['path']}")
            print(f"    Last submitted: {sitemap.get('lastSubmitted', 'Never')}")
            print(f"    Status: {sitemap.get('warnings', 0)} warnings, {sitemap.get('errors', 0)} errors")
    
    elif action == 'submit-sitemap':
        site_url = sys.argv[2]
        sitemap_url = sys.argv[3]
        submit_sitemap(site_url, sitemap_url)
    
    elif action == 'delete-sitemap':
        site_url = sys.argv[2]
        sitemap_url = sys.argv[3]
        delete_sitemap(site_url, sitemap_url)
    
    elif action == 'inspect':
        site_url = sys.argv[2]
        url = sys.argv[3]
        request_indexing(site_url, url)
