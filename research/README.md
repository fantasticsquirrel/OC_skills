# Research Skill

Search for books on archive.org, find academic papers, and verify sources.

## Features

- **Archive.org Book Search**: Find books via Open Library API, check online availability, get download links
- **Internet Archive Metadata**: Access full item details and file listings
- **Download Links**: Direct links to PDF, EPUB, and other formats when available

## Usage

### With OpenClaw

Just ask the agent to search for a book:

> "Search archive.org for Neuromancer by William Gibson"

> "Find The Gulag Archipelago on archive.org"

> "Look up ISBN 0451524934 in the archive.org library"

### Command Line

```bash
python3 skill.py "dune herbert"
```

### As a Library

```python
from skill import search_books, get_download_links, format_book_result

# Search for books
results = search_books(title="1984", author="orwell", limit=5)

# Format results
for book in results['docs']:
    print(format_book_result(book))

# Get download links for a specific Archive.org item
links = get_download_links("1984_202101")
for link in links:
    print(f"{link['format']}: {link['url']}")
```

## API Reference

See [SKILL.md](SKILL.md) for full API documentation including:
- Open Library Search API
- Book Details API  
- Internet Archive Metadata
- Download link construction
- Rate limits and best practices

## Examples

### Search by title and author
```python
results = search_books(title="neuromancer", author="gibson")
```

### Search by ISBN
```python
results = search_books(isbn="0441569595")
```

### Get book details
```python
details = get_book_details("0441569595", id_type="ISBN")
```

### Get download links
```python
links = get_download_links("neuromancer00gibs")
for link in links:
    print(f"{link['format']}: {link['url']} ({link['size']} bytes)")
```

## Notes

- Not all books are downloadable due to copyright restrictions
- Some books require "borrowing" (1-hour loan) rather than permanent download
- Always respect archive.org's terms of service
- Use a reasonable request rate (recommended: ~1 req/sec)

## License

Part of the OpenClaw project.
