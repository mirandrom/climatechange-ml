from collections import deque
from pathlib import Path
from litreview.utils import pickle_load, pickle_save
from litreview import s2
import json

# paper id for tackling climate change with ml paper
CCML_ID = '998039a4876edc440e0cabb0bc42239b0eb29644'

# how far back/forward from original papers do we scrape
MIN_CITLEN = -3
MAX_CITLEN = 3

# where to save scraped papers and associated data (to continue if it crashes)
PATH = Path(".")
DB_PATH = PATH / "papers_db.pkl" # map of paper ids to their content
S2IDS_PATH = Path("papers_buffer.pkl") # references/citations still to scrape
NOT_FOUND_PATH = Path("papers_not_found.pkl") # paper ids not found
UNKOWN_PATH = Path("papers_unknown.pkl") # papers not on semantic scholar


if __name__ == '__main__':
    if DB_PATH.exists():
        s2ids = pickle_load(S2IDS_PATH)
        db = pickle_load(DB_PATH)
        not_found = pickle_load(NOT_FOUND_PATH)
        unknown = pickle_load(UNKOWN_PATH)
    else:
        s2ids = deque([(r['paperId'],0) for r in s2.get_data(CCML_ID)['references']])
        db = {}
        not_found = set()
        unknown = set()

    i = 0
    while True:
        try:
            (s2id, citlen) = s2ids[0]
            if s2id not in db and (MIN_CITLEN <= citlen <= MAX_CITLEN):
                paper = s2.get_data(s2id, include_unknown_references=True, t=300)
                if paper:
                    for c in paper['citations']:
                        if not c['paperId']:
                            c['source'] = s2id
                            unknown.add(json.dumps(c))
                        elif c['paperId'] not in db:
                            s2ids += [(c['paperId'], citlen+1)]
                    for r in paper['references']:
                        if not r['paperId']:
                            r['source'] = s2id
                            unknown.add(json.dumps(r))
                        elif r['paperId'] not in db:
                            s2ids += [(r['paperId'], citlen -1)]
                    i += 1
                    print(f"\rPapers added: {i} ({len(s2ids)} in buffer, {len(db)} in db)", end="")
                    db[s2id] = paper
                else:
                    print(f"\rPaper not found: {s2id}", end="")
                    not_found.add(s2id)
            s2ids.popleft()
        except KeyboardInterrupt:
            print("Saving db and s2ids buffer")
            pickle_save(db, DB_PATH, overwrite=True)
            pickle_save(s2ids, S2IDS_PATH, overwrite=True)
            pickle_save(unknown, UNKOWN_PATH, overwrite=True)
            pickle_save(not_found, NOT_FOUND_PATH, overwrite=True)
            print(f"Interrupt on paper: {s2id}")
            quit()
        except Exception as e:
            print("Saving db and s2ids buffer")
            pickle_save(db, DB_PATH, overwrite=True)
            pickle_save(s2ids, S2IDS_PATH, overwrite=True)
            pickle_save(unknown, UNKOWN_PATH, overwrite=True)
            pickle_save(not_found, NOT_FOUND_PATH, overwrite=True)
            print(f"Exception on paper: {s2id}")
            raise e
