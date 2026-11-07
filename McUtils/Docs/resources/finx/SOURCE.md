# Vendored finx assets

Verbatim copies of files from the finx Jekyll theme (https://github.com/McCoyGroup/finx), used by
`McUtils.Docs.static_doc` / `static_markdown` so single-file pages get the finx styles without a network fetch.

- Commit: `d8837eb946bffe544e5c4f41932bb4f1bbd05b82` (identical to `master` on 2026-11-05)
- Files: `assets/css/style.css`, `assets/css/docs.css`, `assets/css/pygment_trac.css`, `assets/js/init.js`

To update: copy the same files from a finx checkout and change `FINX_VENDORED_REF` in `McUtils/Docs/HTMLDocs.py`
(the commit the `"link"` mode points the browser at) to the new commit.
