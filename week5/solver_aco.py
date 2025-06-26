import math
import sys
import random
from common import read_input, print_tour


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def two_opt(tour, cities):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour) - 1):
                if j - i == 1:  
                    continue
                before = distance(cities[tour[i - 1]], cities[tour[i]]) + distance(cities[tour[j]], cities[tour[j + 1]])
                after = distance(cities[tour[i - 1]], cities[tour[j]]) + distance(cities[tour[i]], cities[tour[j + 1]])
                if after < before:
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True
    return tour

def solve(cities, alpha = 0.5, beta = 3, evaporation= 0.8, iterations = 50,num_ants = 50, Q =100, q0 = 0.4):
    N = len(cities)
    dist = [[0]*N for i in range (N)]
    for i in range (N):
        for j in range(i,N):
            if i != j:
                dist[i][j] = dist[j][i] = distance(cities[i],cities[j])
            else:
                dist[i][i] = 1e-10 #  dist[i][i]分母になると、逆数で無限大を返す
                                   # -> heuristic_info
    
    # 距離の逆数　betaが大きいほど、greedyに近似
    heuristic_info = [[1.0/dist[i][j] for j in range(N)] for i in range(N)]
    # フェロモン alphaが大きいほと、前の情報を信頼
    pheromone_level =  [[1.0 for j in range(N)] for i in range(N)]
            
    best_length = float('inf')
    best_tour = None
    
    for i in range(iterations):
        print("iteration =", i)
        print(' ')
        print(' ')
        tours = []
        lengths = []
        for k in range(num_ants):
            #print (" now ant index is", k)
            visited = [False] * N
            start = random.randrange(0, N)
            tour = [start]
            current = start
            visited[current] = True
            
            while len(tour) < N:
                probabilities = []
                candidate_cities = []
                # 現在currentにいる
                for city in range(N):     #現地から訪問したcityへの訪問率は0？
                    if not visited[city]: #訪問したことないcityへの訪問率を計算？
                        #print(f"pheromone_level[{current}][{city}] = {pheromone_level[current][city]}")
                        # product of heuristic and pheromone , later will calculate p 
                        weight= (pheromone_level[current][city]**alpha) * (heuristic_info[current][city]**beta)
                        candidate_cities.append(city)
                        probabilities.append(weight)
                sum_of_probability = sum(probabilities)
                probabilities = [ x / sum_of_probability for x in probabilities]
                q = random.random()
                if q < q0:
                    
                    next = candidate_cities[probabilities.index(max(probabilities))]
                else: next =  random.choices(candidate_cities, weights=probabilities)[0]
                visited[next] = True
                tour.append(next)
                current = next
            tour.append(start)
            tours.append(tour)
            # 経路長さの計算
            length = 0
            for i in range(1,N):
                length += distance(cities[tour[i]],cities[tour[i-1]])
            lengths.append(length)
            # shortest or not
            if length < best_length:
                print("find a better one")
                best_length = length
                best_tour = tour[:-1]
                best_tour = two_opt(best_tour, cities)
            
                
            
        # pheromone更新
        # 蒸発
        for i in range(N):
            for j in range(i,N):
                if j !=i :
                    pheromone_level[i][j] *= (1-evaporation) 
                    pheromone_level[j][i] = pheromone_level[i][j]
                    
        # 増加
        for k,tour in enumerate(tours):
            increase = Q/lengths[k] # tourの長さはn+1  e.g. 0->1->4->2->3->0 
            for i in range(1, N+1):                 #index 0- 1- 2- 3- 4- 5
                cityA = tour[i]
                cityB = tour[i-1] 
                pheromone_level[cityA][cityB] += increase
                pheromone_level[cityB][cityA] += increase
        
    print(best_tour)
    start= best_tour.index(0)
    best_tour = best_tour[start:] +best_tour[:start]
    
    return best_tour
    

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    
