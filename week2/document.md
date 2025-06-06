**(1)calculate_hash function**

version 1: hash = hash + ord(ch) *10^i
want to mkae it like decimal number, be like "abc" -> 123 "cba"->321
but may end up with huge hash hard for calculation

version 2: hash = hash + ord(ch) * i
be like "abc" -> 1x1+2x2+3x3 , "cba" -> 1x3+2x2+3x1 
costing too much time for performance test even with expanding hash table

version 3: use a list of primes
hash = hash* one prime from list (one by one) + ord (ch)
pass performance test 
using prime to make calculation more complicated so less conflict 

**(2)delete function**

 *step1* : find item which need to delete in buckets or not, if not return false

 *step2* : if item at the head of list (list == buckets[bucket_index]), make head be None ; if item not at the head part of list, use while loop to find the postion of item, also a variable called prev is used to save the position of previous item of item. when the right position of item is found, prev.next will be linked with item.next, the  current item is skipped, which means deleted from list in bucket.

 **(3)expand function**

 when item size is larger than bucket size, expand bucket size as two times: make a new hash table, then add items into new buckets.

 first try: add new item at head of list: bad performance, - still don't understance why

 second try: add new item at end of list, with parameter next of new itme as None  






