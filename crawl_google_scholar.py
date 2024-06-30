from scholarly import scholarly
from collections import deque
import json
from tqdm import tqdm

TOT_NODES = 50
MAX_DEG = 7

def process(author_name='Ilya Sutskever'):
    search_query = scholarly.search_author(author_name)
    ID_adj_list = {}
    ID_to_info = {
        
        'EXAMPLE_ID' : {'name': 'Steven A Cholewiak', 'pic_link': 'https://scholar.google.com/citations?view_op=medium_photo&user=4bahYMkAAAAJ',
        
        'affiliation': "Applied Vision Scientist at Google LLC",
        
        }
        
    }

    ID_to_info = {}

    author = next(search_query)
    dictionary = scholarly.fill(author, sections=['coauthors'])
    ID = author['scholar_id']
    
    starting_ID = ID

    print('Starting ID', ID)

    visited = set()
    Q = []

    Q.append(ID)
    visited.add(ID)

    # ID_to_info[ID] = {
            
    #     'name': author['name'],
    #     'affiliation': author['affiliation'],
        
    # }
    
    pbar = tqdm(total=TOT_NODES, desc='Processing nodes')

    queue = deque(Q)

    while queue and len(visited) < TOT_NODES:
        cur = queue.popleft()
        # print(cur)
        
        if cur in ID_adj_list:
            continue
            
        print(cur)
            
        search_query = scholarly.search_author_id(cur)
        
        # print(search_query)
        
        # author = next(search_query)
        dictionary = scholarly.fill(search_query, sections=['coauthors'])
        
        # scholarly.fill
        
        print(dictionary)
        
        ID_adj_list[cur] = []
        
        nxt_authors = search_query['coauthors']
        
        # print(nxt_authors)
        
        for i in range(min(MAX_DEG, len(nxt_authors))):
            nxt_author = nxt_authors[i]
            nxt_ID = nxt_author['scholar_id']
            ID_adj_list[cur].append(nxt_ID)
            ID_to_info[nxt_ID] = {
                
                'name': nxt_author['name'],
                'affiliation': nxt_author['affiliation'],
                
            }
            
            if nxt_ID not in visited:
                visited.add(nxt_ID)
                queue.append(nxt_ID)
                pbar.update(1)
    
    pbar.close()  # Close the progress bar when done

    #Make graph bidirectional

    all_news = []

    for ID in ID_adj_list:
        for nxt_ID in ID_adj_list[ID]:
            if nxt_ID not in ID_adj_list:
                all_news.append(nxt_ID)

    for i in all_news:
        ID_adj_list[i] = []
        
    for ID in ID_adj_list:
        for nxt_ID in ID_adj_list[ID]:
            if ID not in ID_adj_list[nxt_ID]:
                ID_adj_list[nxt_ID].append(ID)
        

    with open(author_name + '_id_data.json', 'w') as f:
        json.dump(ID_to_info, f)
        
    with open(author_name + '_graph_data.json', 'w') as f:
        json.dump(ID_adj_list, f)
        
    return starting_ID


if __name__ == '__main__':
    process('Andrew Ng')