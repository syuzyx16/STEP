# update 
Tried a faster 2-opt with limited iterations and partial edge checks per iteration 
 ([reference](https://github.com/GabryGao/google-step-6/blob/main/solver_2opt.py) )
 
 time is shortened to be 2200s in challenge6 
 
 but the shortest way it found is  46980.13... maybe should change these two parameter **max_iters=10, max_checks_per_iter=20000** to make 2opt more effective

# what is different from week5

use 2opt for each ant finish its tour, but really cost much time.
since realize in interation 21~100, rarely find better tour,  finaly choose to decrease interation from 100 to 20 and decrease number of ants to save more time

# as a result
  - when change parameter of aco for several times, didn't improve much

  - when apply 2opt to each ant, even if interation and ants' number are decreased ( and costed more time)
  at least result became better

# run time and result for challenge 5 & 6

- challenge 5:  
distance 20956     
time 819s

- challenge 6:  
distance 42548     
time ~17000s



