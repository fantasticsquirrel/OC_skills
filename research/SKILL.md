# Research Skill

Provides tools for web research including archive.org book search, academic resources, and source verification.

## Archive.org Book Search

### Open Library Search API

**Endpoint:** `https://openlibrary.org/search.json`

**Parameters:**
- `q` - Query string (title, author, ISBN, etc.)
- `title` - Search by title
- `author` - Search by author name  
- `isbn` - Search by ISBN
- `subject` - Search by subject/topic
- `limit` - Max results (default 100, max 100)
- `offset` - Pagination offset
- `fields` - Comma-separated list of fields to return (default: all)

**Example:**
```bash
curl "https://openlibrary.org/search.json?q=dune&author=herbert&limit=5"
```

**Response fields:**
- `numFound` - Total number of results
- `docs` - Array of book objects
  - `key` - Open Library work ID (e.g., "/works/OL45804W")
  - `title` - Book title
  - `author_name` - Array of author names
  - `first_publish_year` - Year first published
  - `isbn` - Array of ISBNs
  - `publisher` - Array of publishers
  - `edition_count` - Number of editions
  - `has_fulltext` - Boolean, true if readable online
  - `ia` - Array of Internet Archive identifiers
  - `cover_i` - Cover image ID

### Book Details API

**Endpoint:** `https://openlibrary.org/api/books`

**Parameters:**
- `bibkeys` - Comma-separated list of identifiers (ISBN:, OCLC:, LCCN:, OLID:, OL:)
- `format` - Response format (`json`)
- `jscmd` - Data level (`data` for full details, `details` for MARC)

**Example:**
```bash
curl "https://openlibrary.org/api/books?bibkeys=ISBN:0451524934&format=json&jscmd=data"
```

### Internet Archive Metadata

**Endpoint:** `https://archive.org/metadata/{identifier}`

Returns full metadata for an Internet Archive item including:
- Download links (PDF, EPUB, etc.)
- File formats available
- OCR text
- Reviews and ratings

**Example:**
```bash
curl "https://archive.org/metadata/dune00herb"
```

### Cover Images

**Small cover:** `https://covers.openlibrary.org/b/id/{cover_i}-S.jpg`  
**Medium cover:** `https://covers.openlibrary.org/b/id/{cover_i}-M.jpg`  
**Large cover:** `https://covers.openlibrary.org/b/id/{cover_i}-L.jpg`

Or by ISBN: `https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg`

### Reading Online

For books with `has_fulltext: true` and `ia` identifiers:

**Reader URL:** `https://archive.org/details/{ia_identifier}`  
**Borrow URL:** `https://openlibrary.org/borrow/ia/{ia_identifier}`

### Download Links

If Internet Archive metadata shows files available:

**Direct download:** `https://archive.org/download/{identifier}/{filename}`

Common formats:
- `{identifier}.pdf`
- `{identifier}_djvu.txt` (OCR text)
- `{identifier}_jp2.zip` (images)

## Workflow: Finding a Book

1. **Search by title/author:**
   ```bash
   curl "https://openlibrary.org/search.json?title=neuromancer&author=gibson&limit=5&fields=key,title,author_name,first_publish_year,isbn,has_fulltext,ia"
   ```

2. **Check if readable online** (look for `has_fulltext: true` and `ia` array)

3. **Get full metadata from Internet Archive:**
   ```bash
   curl "https://archive.org/metadata/{ia_identifier}"
   ```

4. **Extract download links** from `files` array in metadata response

5. **For borrowable books** (not always downloadable), use:
   ```
   https://openlibrary.org/borrow/ia/{ia_identifier}
   ```

## Output Format

When researching books, structure output as:

```markdown
### {Title} by {Author} ({Year})

- **Open Library ID:** {key}
- **ISBN:** {first available ISBN}
- **Editions:** {edition_count}
- **Online Access:** {Yes/No}
  - Archive.org ID: {ia_identifier}
  - Reader: https://archive.org/details/{ia_identifier}
  - Download: {list available formats with links}

**Summary/Notes:** {any additional context}
```

## Rate Limits

- Open Library: No official limit, but be respectful (~1 req/sec recommended)
- Archive.org: No strict limit for metadata, but use reasonable delays for downloads

## User Agent

Always use a descriptive User-Agent:
```
User-Agent: OpenClaw-Research/1.0 (+https://github.com/fantasticsquirrel/OpenClaw)
```

## Notes

- Not all books are downloadable (copyright restrictions)
- `has_fulltext: true` means readable in browser, but may require "borrowing" (1-hour loan)
- Archive.org identifiers from Open Library may be outdated; always verify via metadata API
- For recent/copyrighted books, check `lending_edition` in Open Library API for borrow-only access
