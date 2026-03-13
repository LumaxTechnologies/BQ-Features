# Release notes

## What it is

**Release notes** in BigQuery list product updates and announcements: new features, changes, and deprecations. You open them from the console (e.g. Release notes in the menu or from Overview).

## Demo doc

Use release notes to keep the demo and docs up to date. When a feature you use in the demo (e.g. saved queries, Dataform, Gemini, data canvas) changes, update the relevant feature doc in `doc/<first-level>/<second-level>.md` and note the change in a short “Demo changelog” or in this file.

## Demo material

1. **Open Release notes**  
   In BigQuery → **Release notes** (from the left menu or Overview). Or open the release notes URL from the BigQuery docs.

2. **Skim recent updates**  
   Read the latest 2–3 releases. Note any that affect:
   - **Studio**: Explorer, Queries, Notebooks, Data canvas, Data preparations, Pipelines.  
   - **Pipelines and integration**: Data Transfers, Dataform, Scheduled queries.  
   - **Governance**: Policy tags, exchanges, clean rooms.  
   - **Administration**: Jobs, monitoring, reservations.  
   - **Agents, Search, Settings** (Preview).

3. **Relate to demo**  
   If a release adds or changes a feature you demo (e.g. “Saved queries now support X”), add a one-line note in the corresponding doc file (e.g. `1-studio/queries.md`): “As of [date], [feature].” No need to change the demo data; just keep the steps and screens accurate.

4. **Changelog (optional)**  
   In this file or in a `doc/CHANGELOG.md`, keep a short list: “YYYY-MM: Updated agents.md for new agent UI.” “YYYY-MM: Added dataform.md for Dataform operations demo.” This helps maintainers know what was touched when.

5. **Subscribe**  
   Subscribe to Google Cloud release notes (RSS, email, or blog) so you hear about BigQuery changes. Document the link for your team.

## Demo data used

- No direct use of the demo dataset in release notes.  
- Release notes inform **updates** to the demo docs and runbooks.

## References

- [BigQuery release notes](https://cloud.google.com/bigquery/docs/release-notes)  
- [Google Cloud Blog – BigQuery](https://cloud.google.com/blog/products/data-analytics)
