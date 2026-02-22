# Research Skill

Provides tools for web research including archive.org book search, academic resources, and source verification.

## Research Guidelines

When conducting research and producing output, follow these principles:

### Output Style
- **Tone:** Factual and neutral. No editorializing or subjective language.
- **Speculation:** Label explicitly when presenting credible speculation. Distinguish clearly between confirmed facts and informed inference.
- **Structure:** Present information clearly with appropriate headings and organization.

### Source Standards
- **Primary sources preferred:** Government sites (.gov, .mil), academic institutions (.edu), official documents, direct interviews, original publications.
- **First-hand accounts:** Newspaper interviews, social media posts, direct statements, and original content from individuals are acceptable sources. **When an article references someone's post or statement, prefer to find and cite the original post directly** rather than the article about it.
- **Secondary sources:** Use reputable news organizations, established research institutions, and verified experts.
- **Wikipedia:** Acceptable as a discovery starting point to find leads, but **do not cite Wikipedia directly in final output**. Instead, follow Wikipedia's citations to the primary sources and cite those.
- **Archive sources:** When live sites are blocked or inaccessible, use Wayback Machine (archive.org) or archive.ph. Include both the original URL and the archive URL with timestamp.

### Citations
- **Always cite sources** with clear, clickable links.
- **Format:** `[Source Name](URL)` or include full URL in text.
- **Archive all sources:** For every page you cite, archive it to both archive.org (Wayback Machine) and archive.is, then provide all three links:
  - Original: `https://example.com/article`
  - Archive.org: `https://web.archive.org/web/TIMESTAMP/https://example.com/article`
  - Archive.is: `https://archive.is/SHORTCODE` (or `https://archive.ph/SHORTCODE`)
- **Attribution:** Clearly attribute quotes, data, and claims to their sources.

### Research Workflow
1. Start with primary sources when available (.gov, .mil, .edu, official docs)
2. **When an article references a post or statement, locate the original source** (e.g., if an article talks about a tweet, find and cite the actual tweet)
3. Use Wikipedia to discover source trails, then cite the original sources
4. **Archive every source you cite** to both archive.org and archive.is immediately after finding it
5. When blocked by paywalls or geo-restrictions, try Wayback Machine or archive.ph
6. Cross-reference claims across multiple independent sources when possible
7. Note the date of source material when relevant (especially for current events)
8. Distinguish between what is known, what is reported, and what is speculated
9. **Save all research output to the Obsidian vault** at `/var/lib/openclaw/vault/Research/` using the topic-based structure (see "Storing Research Output" section below)

### Example Citation Formats

**Primary source with archives:**
> According to the [2025 FBI Crime Report](https://www.fbi.gov/crime-stats/2025) ([archive.org](https://web.archive.org/web/20260222/https://www.fbi.gov/crime-stats/2025), [archive.is](https://archive.is/AbCdE)), violent crime decreased by 3.2%.

**First-hand social media post:**
> In a [Twitter post](https://twitter.com/user/status/123456) ([archive.org](https://web.archive.org/web/20260222/https://twitter.com/user/status/123456), [archive.is](https://archive.is/XyZ12)), the CEO stated "We are committed to transparency."

**News article referencing a post (cite the original):**
> ❌ **Avoid:** News article says "CEO tweeted about transparency"  
> ✅ **Prefer:** Locate and cite the [original tweet](https://twitter.com/ceo/status/789) ([archive.org](https://web.archive.org/web/20260222/...), [archive.is](https://archive.is/...)) directly

**Multiple sources:**
> This claim is reported by [Reuters](https://example.com/reuters) ([archive.org](https://web.archive.org/web/20260222/...), [archive.is](https://archive.is/...)), [AP](https://example.com/ap) ([archive.org](https://web.archive.org/web/20260222/...), [archive.is](https://archive.is/...)), and confirmed in [official documents](https://example.gov/doc.pdf) ([archive.org](https://web.archive.org/web/20260222/...), [archive.is](https://archive.is/...)).

### How to Archive Pages

For every source you cite, create archives on both platforms:

#### Archive.org (Wayback Machine)

**Save a page:**
```bash
# Submit URL for archiving
curl -X POST "https://web.archive.org/save/https://example.com/article"
```

**Check if archived:**
```bash
# Get most recent snapshot
curl "https://archive.org/wayback/available?url=https://example.com/article"
```

**Direct archive link format:**
```
https://web.archive.org/web/YYYYMMDDHHMMSS/https://example.com/article
```

#### Archive.is (archive.ph)

**Save a page:**
```bash
# Submit URL for archiving
curl -X POST "https://archive.ph/submit/" -d "url=https://example.com/article"
```

**Or visit directly in browser:**
```
https://archive.is/?run=1&url=https://example.com/article
```

**Result:** You'll receive a short URL like `https://archive.is/AbCdE` or `https://archive.ph/XyZ12`

#### Archiving Workflow

1. **Find the source** (original article, post, document)
2. **Archive to archive.org:** `curl -X POST "https://web.archive.org/save/URL"`
3. **Archive to archive.is:** Submit via curl or visit `https://archive.is/?run=1&url=URL`
4. **Retrieve archive links:**
   - Wayback: Check `https://archive.org/wayback/available?url=URL` for timestamp
   - Archive.is: Copy the short URL from the result page
5. **Cite all three** in your output (original + both archives)

**Note:** Some sites may block archiving or require manual CAPTCHA completion on archive.is. If automated archiving fails, use browser-based submission.

---

## Storing Research Output

All research findings should be saved to the Obsidian vault for long-term storage and accessibility via the Hub.

### Vault Location

**Server path:** `/var/lib/openclaw/vault/Research/`  
**Hub access:** https://95.111.254.161/vault  
**Obsidian access:** https://95.111.254.161/obsidian-launch

### Research Folder Structure

Research notes are organized by **topic** with a standardized structure:

```
Research/
  topic-name/
    _topic.md          # Topic metadata and summary
    YYYYMMDDTHHMMSS_[hex].md  # Individual research notes (timestamped)
    YYYYMMDDTHHMMSS_[hex].md
    ...
```

### Creating a New Research Topic

1. **Choose a topic name:** Use kebab-case (e.g., `rhone-group-epstein`, `project-mockingbird`, `ufos-1947-roswell`)

2. **Create topic folder:**
   ```bash
   mkdir -p /var/lib/openclaw/vault/Research/topic-name
   ```

3. **Create `_topic.md`** with frontmatter:
   ```markdown
   ---
   title: Topic Name
   type: research-topic
   created: 2026-02-22
   updated: 2026-02-22
   status: active
   tags:
     - research
     - domain/topic-area
   ---
   
   # Topic Name
   
   Brief description of what this research covers.
   
   ## Key Questions
   
   - What are we investigating?
   - What connections are we mapping?
   
   ## Related Topics
   
   - [[other-topic]]
   - [[another-related-topic]]
   ```

4. **Add research notes** using timestamped filenames:
   ```bash
   # Generate timestamp + random hex
   TIMESTAMP=$(date +%Y%m%dT%H%M%S)
   HEX=$(openssl rand -hex 2)
   NOTE_PATH="/var/lib/openclaw/vault/Research/topic-name/${TIMESTAMP}_${HEX}.md"
   ```

5. **Note frontmatter template:**
   ```markdown
   ---
   title: Finding Title
   type: research-note
   topic: topic-name
   created: 2026-02-22T13:45:00
   sources:
     - https://example.com/article
   tags:
     - finding
     - evidence
   ---
   
   # Finding Title
   
   ## Summary
   
   Key finding in 1-2 sentences.
   
   ## Details
   
   Full investigation details with citations.
   
   ## Sources
   
   - [Article Title](https://example.com/article) ([archive.org](https://web.archive.org/...), [archive.is](https://archive.is/...))
   - [Another Source](https://example.org/doc) ([archive.org](https://web.archive.org/...), [archive.is](https://archive.is/...))
   ```

### After Completing Research

1. **Update `_topic.md`** with summary of findings
2. **Set permissions** (vault is www-data owned):
   ```bash
   chown -R www-data:www-data /var/lib/openclaw/vault/Research/topic-name
   chmod -R 755 /var/lib/openclaw/vault/Research/topic-name
   ```
3. **Verify on Hub:** Visit https://95.111.254.161/vault and navigate to Research folder
4. **Notify Jon** that research is stored and accessible

### Example: Rhône Group Research

Existing example at `/var/lib/openclaw/vault/Research/rhone-group-epstein/`:

- `_topic.md` — Topic overview and key questions
- `20260218T000001_a1b2.md` — Robert Agostinelli connections
- `20260218T000002_c3d4.md` — Full member search log
- `20260218T210000_b5c6.md` — FOII board details, Kafka financial ties, Aznar email

All notes include triple-link citations (original + archive.org + archive.is).

---

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
