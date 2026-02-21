#!/usr/bin/env python3
"""Research skill helper functions for archive.org and Open Library APIs."""

import json
import urllib.request
import urllib.parse
from typing import Optional, List, Dict, Any


USER_AGENT = "OpenClaw-Research/1.0 (+https://github.com/fantasticsquirrel/OpenClaw)"


def search_books(
    query: Optional[str] = None,
    title: Optional[str] = None,
    author: Optional[str] = None,
    isbn: Optional[str] = None,
    subject: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> Dict[str, Any]:
    """Search Open Library for books.
    
    Args:
        query: General search query
        title: Search by title
        author: Search by author
        isbn: Search by ISBN
        subject: Search by subject
        limit: Max results (default 10, max 100)
        offset: Pagination offset
        
    Returns:
        Dict with 'numFound' and 'docs' (list of book objects)
    """
    params = {}
    
    if query:
        params["q"] = query
    if title:
        params["title"] = title
    if author:
        params["author"] = author
    if isbn:
        params["isbn"] = isbn
    if subject:
        params["subject"] = subject
        
    params["limit"] = min(limit, 100)
    params["offset"] = offset
    params["fields"] = "key,title,author_name,first_publish_year,isbn,edition_count,has_fulltext,ia,cover_i,publisher,subject"
    
    url = f"https://openlibrary.org/search.json?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read())


def get_book_details(identifier: str, id_type: str = "ISBN") -> Dict[str, Any]:
    """Get detailed book information from Open Library.
    
    Args:
        identifier: Book identifier (ISBN, OLID, etc.)
        id_type: Type of identifier (ISBN, OCLC, LCCN, OLID, OL)
        
    Returns:
        Dict with book details
    """
    bibkey = f"{id_type}:{identifier}"
    params = {
        "bibkeys": bibkey,
        "format": "json",
        "jscmd": "data"
    }
    
    url = f"https://openlibrary.org/api/books?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read())
        return data.get(bibkey, {})


def get_archive_metadata(ia_identifier: str) -> Dict[str, Any]:
    """Get Internet Archive metadata for an item.
    
    Args:
        ia_identifier: Internet Archive identifier
        
    Returns:
        Dict with full metadata including download links
    """
    url = f"https://archive.org/metadata/{ia_identifier}"
    
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read())


def get_download_links(ia_identifier: str) -> List[Dict[str, str]]:
    """Get available download links for an Archive.org item.
    
    Args:
        ia_identifier: Internet Archive identifier
        
    Returns:
        List of dicts with 'format', 'size', and 'url' keys
    """
    metadata = get_archive_metadata(ia_identifier)
    files = metadata.get("files", [])
    
    # Filter for common readable formats
    readable_formats = {".pdf", ".epub", ".mobi", ".txt", "_djvu.txt"}
    
    links = []
    for file in files:
        name = file.get("name", "")
        if any(name.endswith(fmt) for fmt in readable_formats):
            links.append({
                "format": file.get("format", "unknown"),
                "filename": name,
                "size": file.get("size", "unknown"),
                "url": f"https://archive.org/download/{ia_identifier}/{name}"
            })
    
    return links


def format_book_result(book: Dict[str, Any], include_downloads: bool = True) -> str:
    """Format a book search result as markdown.
    
    Args:
        book: Book dict from Open Library search
        include_downloads: If True and book has Archive.org ID, fetch download links
        
    Returns:
        Formatted markdown string
    """
    title = book.get("title", "Unknown Title")
    authors = book.get("author_name", [])
    author_str = ", ".join(authors) if authors else "Unknown Author"
    year = book.get("first_publish_year", "Unknown")
    
    ol_key = book.get("key", "")
    isbn = book.get("isbn", [None])[0]
    editions = book.get("edition_count", 0)
    has_fulltext = book.get("has_fulltext", False)
    ia_ids = book.get("ia", [])
    
    md = f"### {title} by {author_str} ({year})\n\n"
    md += f"- **Open Library ID:** {ol_key}\n"
    
    if isbn:
        md += f"- **ISBN:** {isbn}\n"
    
    md += f"- **Editions:** {editions}\n"
    md += f"- **Online Access:** {'Yes' if has_fulltext else 'No'}\n"
    
    if ia_ids and include_downloads:
        ia_id = ia_ids[0]
        md += f"  - Archive.org ID: {ia_id}\n"
        md += f"  - Reader: https://archive.org/details/{ia_id}\n"
        
        try:
            downloads = get_download_links(ia_id)
            if downloads:
                md += "  - Downloads:\n"
                for dl in downloads:
                    md += f"    - [{dl['format']}]({dl['url']}) ({dl['size']} bytes)\n"
        except Exception as e:
            md += f"  - Download links unavailable ({e})\n"
    
    return md


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python skill.py <search query>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    
    print(f"Searching for: {query}\n")
    results = search_books(query=query, limit=3)
    
    print(f"Found {results['numFound']} results. Showing top 3:\n")
    
    for book in results.get("docs", [])[:3]:
        print(format_book_result(book))
        print()
