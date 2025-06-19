# medium  result for most popular
# {3377: '英語', 4145: 'ISBN', 793034: '2006年', 
# 332554: '2005年', 1069779: '2007年', 774362: '東京都', 1789: '昭和', 
# 935867: '2004年', 1491: '2003年', 1547: '2000年', 813: '2001年'}


# large result of most popular
#{1864744: '日本', 3377: '英語', 4176906: 'VIAF_(識別子)', 2503159: 'バーチャル国際典拠ファイル', 
# 1698838: 'アメリカ合衆国', 4145: 'ISBN', 4176899: 'ISNI_(識別子)'
# , 3148466: '国際標準名称識別子', 2115245: '地理座標系', 4176904: 'SUDOC_(識別子)'}


import sys
import collections

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = None
        goal_id = None
        for id, title in self.titles.items():
            if start == title:
                start_id = id
            if goal == title:
                goal_id = id
        if start_id == None:  
            print("start does not exist")
            return None
        if goal_id == None: 
            print("goal does not exist")
            return None
        
                
        if start_id == goal_id:
            return  [start]
    
        queue = collections.deque()
        visited = {}
        visited[start_id] = True
        queue.append(start_id)
        parent ={}
        parent[start_id] = None
        path_id =[goal_id]
        path = []
        while queue:
            #print(queue)
            node = queue.popleft()
            if node == goal_id:
                print("Found")
                current = goal_id
                while parent[current]:
                    path_id.append(parent[current])
                    current = parent[current]
                path_id.reverse()
                for id in path_id:
                    path.append(self.titles[id])
                return path
            for child in self.links[node]:
                if not child in visited:
                    visited[child] = True
                    parent[child] = node
                    queue.append(child)
        print ("Not found")
        return None


    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        pagerank = {}
        new_pagerank = {}
        node_num = len(self.titles)
        for id in self.titles.keys():
            pagerank[id] = 1
            new_pagerank[id] = 0.15
        is_converge= False
        
        while not is_converge:
            ended_node = 0
            for id in self.links.keys(): 
                if self.links[id]: # 隣接nodeあり
                    for dst in self.links[id]:
                        new_pagerank[dst] += 0.85 * pagerank[id] / len(self.links[id])
                else: # 隣接nodeがない
                    ended_node += pagerank[id] *0.15
            for id in new_pagerank.keys():
                new_pagerank[id] += ended_node/node_num
            
            diff = sum ((new_pagerank[id]- pagerank[id])**2 for id in pagerank.keys())/node_num
            if diff <0.0001:  is_converge = True
            print(diff)
            for id in new_pagerank.keys():
                pagerank[id] = new_pagerank[id]
                new_pagerank[id] = 0.15
            
        sorted_pagerank = dict(sorted(pagerank.items(), key = lambda x : x[1], reverse= True ) )
        top_10 = {}
        #print(sorted_pagerank)
        for i,id in enumerate(sorted_pagerank.keys()):
            if i >9: break
            top_10[id] = self.titles[id]
            
        return top_10


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    wikipedia.find_longest_titles()
    # Example
    wikipedia.find_most_linked_pages()
    # Homework #1
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")