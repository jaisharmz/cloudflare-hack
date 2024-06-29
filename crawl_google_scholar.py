from scholarly import scholarly
from collections import deque
import json

MAX_DEG = 5
search_query = scholarly.search_author('Steven A Cholewiak')

ID_adj_list = {}
ID_to_info = {
    
    'EXAMPLE_ID' : {'name': 'Steven A Cholewiak', 'pic_link': 'https://scholar.google.com/citations?view_op=medium_photo&user=4bahYMkAAAAJ',
     
     'affiliation': "Applied Vision Scientist at Google LLC",
     
     }
    
}

author = next(search_query)
dictionary = scholarly.fill(author, sections=['coauthors'])
ID = author['scholar_id']

print('Starting ID', ID)

visited = set()
Q = []

Q.append(ID)
visited.add(ID)

queue = deque(Q)

while queue and len(visited) < 10:
    cur = queue.popleft()
    print(cur)
    
    if cur in ID_adj_list:
        continue
    
    search_query = scholarly.search_author_id(cur)
    
    print(search_query)
    
    # author = next(search_query)
    dictionary = scholarly.fill(search_query, sections=['coauthors'])
    
    # scholarly.fill
    
    print(dictionary)
    
    ID_adj_list[cur] = []
    ID_to_info[cur] = {
        
        'name': author['name'],
        # 'url_picture': author['pic_link'],
        'affiliation': author['affiliation'],
        # 'citations': author['citedby']
        
    }
    
    nxt_authors = search_query['coauthors']
    
    for i in range(min(MAX_DEG, len(nxt_authors))):
        nxt_author = nxt_authors[i]
        nxt_ID = nxt_author['scholar_id']
        ID_adj_list[cur].append(nxt_ID)
        
        if nxt_ID not in visited:
            visited.add(nxt_ID)
            queue.append(nxt_ID)


#Make graph bidirectional

for ID in ID_adj_list:
    for nxt_ID in ID_adj_list[ID]:
        if ID not in ID_adj_list[nxt_ID]:
            ID_adj_list[nxt_ID].append(ID)


with open(ID + '_id_data.json', 'w') as f:
    json.dump(ID_to_info, f)
    
    

with open(ID + '_graph_data.json', 'w') as f:
    json.dump(ID_adj_list, f)


