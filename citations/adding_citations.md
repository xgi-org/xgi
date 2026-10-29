# Updating the "Projects using XGI" Page

This page is automatically generated from structured YAML files. **Do not edit the `.rst` file directly** because any changes will be overwritten the next time the generator is run. Note that you'll need the `docs` dependencies to run the `generate_using_xgi.py` script.


## File Structure

```
citations/
  published.yaml
  preprints.yaml
  theses.yaml
  software.yaml

tools/
  generate_using_xgi.py

docs/
  source/
    using_xgi.rst (Auto-generated)
```


## How to Add or Edit Entries

All content is stored in YAML files under the `citations/` directory. Each file corresponds to a section of the page.


### 1. Published Papers (`published.yaml`)

Each entry is a dictionary keyed by a unique identifier:

```yaml
tong_hic3_2025:
  tags:
    - XGI
  authors:
    - Yuyan Tong
    - Renhao Hong
  title: "Hi-C3: a statistical inference-based model..."
  year: 2025
  reference: "Briefings in Bioinformatics, Volume 26, Issue 5, bbaf568"
  links:
    paper: https://doi.org/...
    code: https://github.com/...
```

**Notes:**

* `tags` should include `XGI` and/or `XGI-DATA`
* `authors` must be in order
* `reference` is free-form (journal, conference, etc.)
* `links` is optional but highly recommended


### 2. Preprints (`preprints.yaml`)

```yaml
akcakir_exploring_2024:
  tags:
    - XGI
  authors:
    - Gülşah Akçakır
  title: Exploring the interplay...
  year: 2024
  reference: "arXiv:2407.12728"
  links:
    paper: https://arxiv.org/abs/2407.12728
```


### 3. Theses (`theses.yaml`)

```yaml
sampson_complex_2025:
  tags:
    - XGI
  authors:
    - Corbit Sampson
  title: "Complex Social Systems..."
  year: 2025
  university: "The University of Colorado at Boulder"
  links:
    thesis: https://...
```

**Note:** Use `university` instead of `reference`.


### 4. Software (`software.yaml`)

```yaml
hoi:
  url: https://brainets.github.io/hoi/

hypercontagion:
  url: https://hypercontagion.readthedocs.io/en/latest
```


## Generating the `.rst` Page

After updating any YAML file, regenerate the page:

```bash
python tools/generate_using_xgi.py
```

This will overwrite:

```
docs/source/using_xgi.rst
```


## Sorting and Formatting Rules

The script automatically:

* Groups entries by **year (descending)**
* Sorts within each year by **first author’s last name**
* Numbers entries automatically
* Formats links and citations for Sphinx


## Important Guidelines

* **Do not manually edit** `using_xgi.rst`
* Always run the generator after making changes
* Ensure YAML is valid (spacing matters!)
* Keep keys (e.g., `tong_hic3_2025`) unique


## Workflow Summary

1. Edit the appropriate YAML file
2. Save changes
3. Run:

   ```bash
   python tools/generate_using_xgi.py
   ```
4. Commit both the YAML and generated `.rst`


## Tips

* Copy an existing entry as a template when adding new ones
* Keep formatting consistent (quotes for long titles help)
* Add links to the paper and code whenever possible (DOIs prefered)
