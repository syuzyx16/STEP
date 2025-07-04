# ant colony 
# with a faster2opt by Xin Gao

import time
import math
import sys
import random

from common import read_input, print_tour


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)



def two_opt_fast(tour, cities, max_iters=10, max_checks_per_iter=20000):
    N = len(tour)
    best = tour[:]

    for _ in range(max_iters):
        improved = False
        for _ in range(max_checks_per_iter):
            i = random.randint(1, N - 3)
            j = random.randint(i + 1, N - 1)
            if j - i == 1:
                continue

            before = distance(cities[best[i - 1]], cities[best[i]]) + distance(cities[best[j]], cities[best[(j + 1) % N]])
            after = distance(cities[best[i - 1]], cities[best[j]]) + distance(cities[best[i]], cities[best[(j + 1) % N]])

            if after < before:
                best[i:j + 1] = reversed(best[i:j + 1])
                improved = True
                
                break  

        if not improved:
            print("2opt fail")
            break

    return best


"""
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
"""
# beta = 1  or log (distance )
def solve(cities, alpha = 1, beta = 5, evaporation= 0.25, iterations = 30,num_ants = 120, Q =80, q0 = 0.9):
    
    start_time = time.time()
    
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
            start = random.randrange(0, N)  #任意のcityをスタート点にして、局所最適を回避
            tour = [start]
            current = start
            visited[current] = True
            
            while len(tour) < N:
                probabilities = []
                unvisited_cities = []
                # 現在currentにいる
                for city in range(N):     
                    if not visited[city]:  #訪問したことないcityへの訪問率を計算
                        #print(f"pheromone_level[{current}][{city}] = {pheromone_level[current][city]}")
                        # product of heuristic and pheromone , later will calculate p 
                        weight= (pheromone_level[current][city]**alpha) * (heuristic_info[current][city]**beta)
                        unvisited_cities.append(city)
                        probabilities.append(weight)
                sum_of_probability = sum(probabilities)
                probabilities = [ x / sum_of_probability for x in probabilities]
                q = random.random()
                if q < q0:
                    
                    next = unvisited_cities[probabilities.index(max(probabilities))] #40%で最大weightであるedgeを選ぶ
                else: next =  random.choices(unvisited_cities, weights=probabilities)[0] # 60%でランダムに選ぶ
                visited[next] = True
                tour.append(next)
                current = next
            tour.append(start)
            optimized_tour = two_opt_fast(tour, cities)  
            tours.append(optimized_tour)
            
            # 経路長さの計算
            length = 0
            for i in range(1,len(optimized_tour)):
                length += distance(cities[optimized_tour[i]],cities[optimized_tour[i-1]])
            lengths.append(length)
            # shortest or not
            if length < best_length:
                print("find a better one")
                best_length = length
                best_tour = optimized_tour[:-1]
                
            
                
            
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
    
    end_time = time.time()
    print("time：", end_time - start_time, "s")
    
    
    return best_tour
    

if __name__ == '__main__':
    
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
    
