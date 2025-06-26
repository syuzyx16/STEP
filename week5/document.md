
# Method

Ant colony optimization with 2-opt: when a shorter path is found, apply 2-opt for local exploration to further improve the solution, in order to avoid local optima.

# Result
| Challenge | Length    |
|-----------|-----------|
| 0         | 3418.10   |
| 1         | 3832.29   |
| 2         | 5223.97   |
| 3         | 8527.00   |
| 4         | 12034.26  |
| 5         | 22258.21  |
| 6         | 44570.13  |


# Problems 
**when apply ACO without 2opt**
even after adjusting parameters, the algorithm still falls into a local optimum by the third iteration.

**when apply ACO with 2opt**
run time increased. 
as first, wanted to apply 2opt for each found path but cost too much time, that is the reason for only applying it when a shorter path is found.

**when size of cities is too small**
shortest path is the same as that found by greedy.


# Reference
- [Ant Colony Optimization (ACO) algorithm](https://dilipkumar.medium.com/ant-colony-optimization-aco-algorithm-6a954b0b083e)

- [wikipedia蟻コロニー最適化](https://ja.wikipedia.org/wiki/%E8%9F%BB%E3%82%B3%E3%83%AD%E3%83%8B%E3%83%BC%E6%9C%80%E9%81%A9%E5%8C%96)