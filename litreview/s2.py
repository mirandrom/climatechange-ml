import time
from dataclasses import dataclass
from typing import List, Dict, Union

import requests as rq
from dataclasses import asdict


API_URL = "http://api.semanticscholar.org/v1/paper/"

@dataclass
class S2Topic:
    """
    Data class for Semantic Scholar topics
    """
    topic: str
    topicId: str
    url: str


@dataclass
class S2Author:
    authorId: str
    name: str
    url: str


@dataclass
class S2Reference:
    """
    Data class for Semantic Scholar reference
    """
    arxivId: str
    authors: List[str]
    doi: str
    intent: List[str]
    isInfluential: bool
    paperId: str
    title: str
    url: str
    venue: str
    year: int


@dataclass
class S2Paper:
    """
    Data class for arxiv paper object returned by Semantic Scholar API
    """
    abstract: str
    arxivId: str
    authors: List[S2Author]
    citationVelocity: int
    citations: List[S2Reference]
    doi: str
    influentialCitationCount: int
    paperId: str
    references: List[S2Reference]
    title: str
    topics: List[S2Topic]
    url: str
    venue: str
    year: int

def get_data(
        s2id: str,
        include_unknown_references: bool = False,
        to_dataclass: bool = False,
        t=300,
        max_retries=2
        ) -> Union[Dict, S2Paper]:

    url = API_URL + s2id
    if include_unknown_references:
        url += "?include_unknown_references=true"
    r = rq.get(url)

    if not r.ok:
        if max_retries == 0:
            raise Exception(f"Max retried exceed for paper {s2id}")
        if r.status_code in [429, 403]:
            print(f"Error {r.status_code}: sleeping for {t} seconds")
            time.sleep(t)
            t*=2
            return get_data(s2id, include_unknown_references, to_dataclass, t, max_retries-1)
        elif r.status_code == 404:
            print(f"\rError 404: paper {s2id} not found", end="")
            return None
        else:
            raise Exception(f"Error {r.status_code} with reason {r.reason} for paper {s2id}")
    else:
        r = r.json()
        if to_dataclass:
            return _to_dataclass(r)
        else:
            return r


def _to_dataclass(r: Dict):
    r["authors"] = [S2Author(**x) for x in r["authors"]]
    r["citations"] = [S2Reference(**x) for x in r["citations"]]
    r["references"] = [S2Reference(**x) for x in r["references"]]
    r["topics"] = [S2Topic(**x) for x in r["topics"]]
    return S2Paper(**r)


def _asdict(paper: S2Paper):
    paper.authors = [asdict(a) if isinstance(a, S2Author) else a for a in paper.authors]
    paper.references = [asdict(a) if isinstance(a, S2Reference) else a for a in paper.references]
    paper.citations = [asdict(a) if isinstance(a, S2Reference) else a for a in paper.citations]
    paper.topics = [asdict(a) if isinstance(a, S2Topic) else a for a in paper.topics]
    return asdict(paper)
