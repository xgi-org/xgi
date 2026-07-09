from collections import defaultdict
from pathlib import Path

import yaml

DATA_DIR = Path("citations")
OUTPUT = Path("docs/source/using_xgi.rst")


# ---------- Loaders ----------


def load_yaml(name):
    with open(DATA_DIR / name, "r") as f:
        return yaml.safe_load(f)


# ---------- Formatting ----------


def format_authors(authors):
    if len(authors) <= 2:
        return " and ".join(authors)
    if len(authors) > 2:
        return ", ".join(authors[:-1]) + ", and " + authors[-1]
    elif len(authors) == 1:
        return authors[0]
    elif len(authors) == 2:
        return " and ".join(authors)
    else:
        return ""  # no authors provided


def format_tags(tags):
    return "[" + ", ".join(tags) + "]"


def format_links(links):
    lines = []
    for key, url in links.items():
        label = key.capitalize()
        lines.append(f":bdg-link-primary-line:`{label} <{url}>`")
    return "\n".join(lines)


def group_by_year(entries):
    grouped = defaultdict(list)
    for e in entries:
        grouped[e["year"]].append(e)
    return dict(sorted(grouped.items(), reverse=True))


# ---------- Renderers ----------


def render_entries(entries_dict, kind="published"):
    entries = list(entries_dict.values())

    grouped = group_by_year(entries)
    lines = []

    counter = len(entries)

    for year, items in grouped.items():
        lines.append(str(year))
        lines.append("-" * len(str(year)))
        lines.append("")

        # sort by first author last name (approx: last token)
        items = sorted(items, key=lambda x: x["authors"][0].split()[-1])

        for e in items:
            authors = format_authors(e["authors"])
            tags = format_tags(e.get("tags", []))
            title = f"\"{e['title']}\""

            # --- Different formatting per type ---
            if kind == "theses":
                venue = e.get("university", "")
            else:
                venue = e.get("reference", "")

            venue_str = f"{venue}" if venue else ""

            # main line
            line = f"{counter}. {tags} {authors}, {title}"
            if venue_str:
                line += f", {venue_str}"
            line += f" ({e['year']})."

            lines.append(line)
            lines.append("")

            # links
            if "links" in e:
                lines.append(format_links(e["links"]))
                lines.append("")

            counter -= 1

    return "\n".join(lines)


def render_software(software_dict):
    lines = []

    items = list(software_dict.items())
    items = sorted(items, key=lambda x: x[0], reverse=False)

    counter = len(items)

    for name, meta in items:
        url = meta["url"]
        lines.append(f"{counter}. `{name} <{url}>`_")
        counter -= 1

    return "\n\n".join(lines)


# ---------- Main ----------


def main():
    published = load_yaml("published.yaml")
    preprints = load_yaml("preprints.yaml")
    theses = load_yaml("theses.yaml")
    software = load_yaml("software.yaml")

    out = []

    # Header
    out.append("******************")
    out.append("Projects using XGI")
    out.append("******************\n")

    out.append(
        "XGI has been used in a variety of published work and other software. "
        "This is a list of projects that use XGI in substantive ways or use XGI-DATA. "
        "These are marked with [XGI] and [XGI-DATA], respectively.\n"
    )

    out.append(
        "Articles are listed by year and then alphabetically by the last name "
        "of the first author (and title if necessary).\n"
    )

    # Software
    software_header = f"Software Packages ({len(software)} total)"
    length = len(software_header)
    out.append(software_header)
    out.append("=" * length)
    out.append("")
    out.append(render_software(software))
    out.append("\n")

    # Published
    published_header = f"Published Work ({len(published)} total)"
    length = len(published_header)
    out.append(f"Published Work ({len(published)} total)")
    out.append("=" * length)
    out.append("")
    out.append(render_entries(published, kind="published"))
    out.append("")

    # Preprints
    preprints_header = f"Preprints ({len(preprints)} total)"
    length = len(preprints_header)
    out.append(preprints_header)
    out.append("=" * length)
    out.append("")
    out.append(render_entries(preprints, kind="preprint"))
    out.append("")

    # Theses
    theses_header = f"Theses ({len(theses)} total)"
    length = len(theses_header)
    out.append(theses_header)
    out.append("=" * length)
    out.append("")
    out.append(render_entries(theses, kind="theses"))

    OUTPUT.write_text("\n".join(out))
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
