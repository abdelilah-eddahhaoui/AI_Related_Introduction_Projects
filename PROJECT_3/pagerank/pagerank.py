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
    print(sys.argv[1])
    
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print("PageRank Results from Iteration")
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
    
    ## We set the transition dict as a copy of corpus ##
    transition_proba = corpus.copy()
    pages_to_grade = transition_proba[page]
    
    ## We ennumrate the number of items in the pages to rank and in the total pages ##
    n_pages_grade = len(pages_to_grade)
    n_pages_total = len(transition_proba)
    
    if n_pages_grade != 0:
        ## Loop for the keys inside the transition model to calculate the main probabilities ##
        for key in transition_proba:
            if key in pages_to_grade:
                transition_proba[key] = damping_factor/n_pages_grade + \
                    (1 - damping_factor)/n_pages_total
            else:
                transition_proba[key] = (1 - damping_factor)/n_pages_total
        
        ## Verify if it all sums to 1 ##
        summit = 0
        for values in transition_proba.values():
            summit += values
        return transition_proba
    else:
        ## Loop for the keys inside the transition model to calculate the main probabilities ##
        for key in transition_proba:
            transition_proba[key] = 1/n_pages_total
            
        ## Verify if it all sums to 1 ##
        summit = 0
        for values in transition_proba.values():
            summit += values
        return transition_proba

    
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    ## We set the probabilities dict as a copy of corpus ##
    PR = corpus.copy()
    
    PR_final_proba = corpus.copy() 
    for key, value in PR_final_proba.items():
        PR_final_proba[key] = 0
        
    for sample in range(n):
        
        if sample == 0:
            ## Pick a random page from the corpus copy ##
            starting_page = random.choice(list(PR))
            
            ## Computes the initial probabilities ##
            PR = transition_model(corpus, starting_page, damping_factor)
            
            ## Weights and chooses the next page ##
            population = []
            weights = []
            for key, value in PR.items():
                population.append(key)
                weights.append(value)
                    
            page = random.choices(
                population, 
                weights,
                k=1
            )[0]
            
            PR_final_proba[page] = 1
        else:
            ## Computes the following probabilities ##
            PR = transition_model(corpus, str(page), damping_factor)
            population = []
            weights = []
            for key, value in PR.items():
                population.append(key)
                weights.append(value)
                
            ## Weights and chooses the next page ##        
            page = random.choices(
                population, 
                weights,
                k=1
            )[0]
            
            ## Increments the value if a key corresponds, leaving us with a number of appearances in the end ##
            for key, value in PR_final_proba.items():
                if key in page:
                    value += 1
                    PR_final_proba[key] = value

    ## Final probability on how many elements were counted in the loop diveded by the total samples ##       
    for key, value in PR_final_proba.items():
        value = value / n
        PR_final_proba[key] = value
        
    return PR_final_proba

    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iterativelyraise NotImplementedError updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    ## Sigma determing how precise we want the result ##
    sigma = 0.001
    PR_final_proba = corpus.copy() 
    N = len(PR_final_proba)
    
    ## Initial probability equal everywhere ##
    for key, value in PR_final_proba.items():
        value = 1 / N
        PR_final_proba[key] = value

    ## We loop until convergence, meaning that the absolute difference found will be < sigma ##
    ## Direct application of the PR(p) formula ##
    converg = False
    while not converg:
        PR = dict()
        for page in corpus:
            summation = 0
            for inner_page in corpus:
                if page in corpus[inner_page]:
                    summation += PR_final_proba[inner_page] / len(corpus[inner_page])
                elif len(corpus[inner_page]) == 0:
                    summation += PR_final_proba[inner_page] / N

            PR[page] = (1-damping_factor)/N + damping_factor*summation
        
        ## Difference computed and breaking the loop if the equation is satisfied ##
        for page in corpus:
            diff = abs(PR[page] - PR_final_proba[page])

        if diff < sigma:
            converg = True
        
        # Update for next iteration ##
        PR_final_proba = PR
    
    return PR_final_proba


if __name__ == "__main__":
    main()