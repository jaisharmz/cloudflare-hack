from crawl_google_scholar import *
from generate_graph import *

def pipeline(name):
    ID = process(name)
    get_graph_html(name, ID)
    
if __name__ == '__main__':
    pipeline('Ian Goodfellow')