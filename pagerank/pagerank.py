import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    initial_prob = ((1 - damping_factor)/len(corpus)) if len(corpus[page]) > 0 else (1.0/len(corpus))
    result = dict()
    for key in corpus.keys():
        result[key] = initial_prob

    for p in corpus[page]:
        result[p] += damping_factor/len(corpus[page])

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    count = dict()
    for key in corpus.keys():
        count[key] = 0

    current_page = random.choice(list(corpus.keys()))
    count[current_page] += 1

    for _ in range(n - 1):
        tm = transition_model(corpus, current_page, damping_factor)
        keys, weights = zip(*tm.items())  # returns keys and weights in separate lists matching the positions
        current_page = random.choices(keys, weights)[0]
        count[current_page] += 1

    # normalize count to get the pagerank
    for key, value in count.items():
        count[key] = value/n

    return count


def links_to(corpus, page):
    """
    Returns set of pages that link to page
    """
    result = set()
    for p, links in corpus.items():
        # A page that has no links at all should be interpreted as having one link for every page in the corpus
        if page in links or len(links) == 0:
            result.add(p)
    return result

    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # store pages that link to another page
    dict_links_to = dict()
    for page in corpus.keys():
        dict_links_to[page] = links_to(corpus, page)

    N = len(corpus)
    PR = dict()

    # start by assuming the PageRank of every page is 1 / N
    for page in corpus.keys():
        PR[page] = 1.0/N

    done = False
    while not done:
        done = True
        for page in corpus.keys():
            s = 0
            for i in dict_links_to[page]:
                # A page that has no links at all should be interpreted as having one link for every page in the corpus
                if len(corpus[i]) > 0:
                    s += PR[i] / len(corpus[i])
                else:
                    s += PR[i] / len(corpus.keys())

            new_value = ((1 - damping_factor) / N) + (damping_factor * s)

            # keep going if improved more than 0.001
            if abs(PR[page] - new_value) > 0.001:
                done = False

            PR[page] = new_value
        
            # normalize
            norm = sum(PR.values())
            for key, value in PR.items():
                PR[key] = value / norm

    return PR


if __name__ == "__main__":
    main()
