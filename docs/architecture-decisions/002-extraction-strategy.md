# 002 - Extraction Strategy

## Status
Accepted (partially revisited - see "Known limitations" below)

## Context
The pipeline pulls skill-demand signals from multiple, very different
sources: some offer clean public APIs (RemoteOK, GitHub, StackOverflow),
others don't offer any official free API at all (Google Trends, Google
Search). Each source needed its own extraction approach, but they all
had to plug into the same pipeline in a consistent way.

## Decision
Every extractor inherits from a shared `BaseExtractor` class that defines
one required method - `extract()` - which returns a list of raw records.
The base class handles the common part (saving results into
`raw_staging.db`), so each concrete extractor only needs to worry about
fetching data from its specific source.

Per-source approach:
- **RemoteOK**: public JSON API, no auth needed. Simplest case.
- **GitHub**: official REST API via `PyGithub`, authenticated with a
  personal access token for a higher rate limit.
- **StackOverflow**: official Stack Exchange API, works without a key
  (lower rate limit) or with one (higher rate limit).
- **Google Trends**: no official API exists. Used the `pytrends` library
  (unofficial wrapper around Google's internal endpoints) with a fixed
  seed list of skill keywords to query interest scores for.
- **Google Search**: no free official API for result counts at scale.
  Used direct scraping with `requests` + `beautifulsoup4` as a best-effort
  approach, reading the approximate result count Google shows on the
  results page.

## Known limitations
- **`pytrends` is unmaintained.** The GitHub repository was archived by
  its maintainers in April 2025, and Google has since changed backend
  behavior in ways that can break requests (e.g. `400 Bad Request`
  errors). This extractor is not guaranteed to work reliably long-term,
  and the pipeline currently runs without it enabled by default.
- **Google Search scraping is fragile.** Google actively blocks
  automated scraping (429 errors, CAPTCHAs) and this extractor is
  best-effort only, not something to depend on for reliable data.
- Both of the above are consequences of relying on sources that don't
  provide an official, stable API. A future revision could replace them
  with a paid third-party API (e.g. SerpApi) if reliability becomes a
  priority, or drop them in favor of sources with official support.

## Consequences
- The four API-backed extractors (RemoteOK, GitHub, StackOverflow) are
  stable and form the reliable core of the pipeline's data.
- Trends and Google Search are treated as optional, best-effort signals
  rather than core dependencies - the pipeline is designed to still
  produce a useful ROI report without them.