# extract sections and references from source tex
from pathlib import Path
import re
import json
from collections import defaultdict

section_tex_dir = Path("tacling_climate_change_source/sections")
bbl_file = Path("tacling_climate_change_source/main.bbl")
sections_out = Path("section_information.json")
citations_out = Path("section_citations.json")
authors_out = Path("bib_authors.json")
titles_out = Path("bib_titles.json")

sections = {}
citations = defaultdict(list)
citations_lookup = set()
bib_titles = {}
bib_authors = {}

for bibitem in bbl_file.read_text().split("\n\n")[1:-1]:
    bibitem = bibitem.strip().replace("\n", " ")
    bib_id = re.match(r"\\bibitem\{(.*?)\}", bibitem).group(1)
    bib_author = re.match(r"\\bibitem\{.*?\}(.*?)\\newblock", bibitem).group(1)
    bib_title = re.match(r".*\\newblock(.*?)\\newblock", bibitem)
    if bib_title:
        bib_title = bib_title.group(1)
    else:
        bib_title = bib_author
        bib_author = None
    # TODO: normalize tex strings (e.g. remove curly brackets and \em)
    bib_titles[bib_id] = bib_title
    bib_authors[bib_id] = bib_author

authors_out.write_text(json.dumps(bib_authors, indent=4))
titles_out.write_text(json.dumps(bib_titles, indent=4))


for section_tex in section_tex_dir.glob("*.tex"):
    s = None
    ss = None
    sss = None
    p = None
    section_raw = section_tex.read_text()
    for i, line in enumerate(section_raw.split("\n")):
        if line.startswith("\\section{"):
            s = re.search(r"\\section{(.*?)\\texorpdfstring", line).group(1)
            s = s.strip()
            s = "s: " + s
            sections[s] = {}
            ss = None
            sss = None
            p = None
        if line.startswith("\\subsection{"):
            ss = re.search(r"\\subsection\*?\{(.*?)(\}|\\Gap)", line).group(1)
            ss = ss.strip()
            ss = "ss: " + ss
            sections[s][ss] = {}
            sss = None
            p = None
        if line.startswith("\\subsubsection{"):
            sss = re.search(r"\\subsubsection\*?\{(.*?)(\}|\\Gap)", line).group(1)
            sss = sss.strip()
            sss = "sss: " + sss
            sections[s][ss][sss] = {}
            p = None
        if line.startswith("\\paragraph"):
            p = re.search(r"\\paragraph\*?\{(.*?)\}", line).group(1)
            p = p.strip()
            p = "p: " + p
            if sss:
                sections[s][ss][sss][p] = {}
            elif ss:
                sections[s][ss][p] = {}
            elif s:
                sections[s][p] = {}
        # add references
        refs = re.findall(r"\\cite\{(.*?)\}", line)
        refs = ",".join(refs)
        refs = [r.strip() for r in refs.split(",") if r]
        citations_lookup.update(refs)

        # create section path as key
        if refs:
            k = section_tex.stem
            if s:
                k += ' | '+s
            if ss:
                k += ' | '+ss
            if sss:
                k += ' | '+sss
            if p:
                k += ' | '+p
            citations[k] += refs

sections_out.write_text(json.dumps(sections, indent=4))
citations_out.write_text(json.dumps(citations, indent=4))
print(f"Found {len(citations_lookup)} unique citations")