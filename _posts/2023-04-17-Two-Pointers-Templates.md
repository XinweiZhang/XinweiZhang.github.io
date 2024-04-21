---
layout: post
title: "Mastering two pointers technique in LeetCode: 'and' vs 'or' conditions"
description: "Discover the nuances of using 'and' and 'or' conditions with the two pointers technique in LeetCode problems, demonstrated through merging two sorted lists."
date: 2023-04-17
tags: [Algorithm, Leetcode]
keywords: leetcode, two pointers
---

In this post, we will explore the two pointers technique, focusing on the differences and advantages of using 'and' and 'or' conditions within while loops. Understanding the subtle differences between these two approaches can be the key to solving LeetCode problems more efficiently.

To illustrate these concepts, we will examine LeetCode problem 21, [merging two sorted lists](https://leetcode.com/problems/merge-two-sorted-lists/), a classic example for the two pointers technique.


## Problem description: Merge two sorted lists
The problem of merging two sorted lists is as follows: given two linked lists `list1` and `list2`, merge them into a single sorted linked list and return the head of the new list.

Here's an example of how the input and output should look like:
```
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
```
<!--more-->
## Template 1: Using 'and' condition
The first template uses the 'and' condition in the while loop, which means that we append a node to the new list in the while loop only when both pointers have not reached the end. Once one of the pointer reaches the end of a list, we exit the while loop. Consequently, an additional block of code is required to append the remaining elements of the other list to the resulting linked list. In this instance, the line new_list.next = p1 or p2 serves this purpose.

The advantage of this template is that it may avoid iterating over every element in both lists, potentially saving time. Especially in this problem, if, for example, point `p1` hit the end of the list, we can just append the other remaining nodes starting at `p2` to the new list. These remaining nodes will not be iterated.


```python
class Solution:
    def mergeTwoLists(self, list1, list2):

       new_list = ListNode()
       memo = new_list

       # Pointers for the two input linked lists
       p1 = list1
       p2 = list2

       # Merge the two lists by comparing the values of the nodes
       while p1 and p2:
           if p1.val < p2.val:
               new_list.next = p1
               p1 = p1.next
           else:
               new_list.next = p2
               p2 = p2.next
           new_list = new_list.next

       # Append any remaining nodes from list1 or list2 to the merged list
       new_list.next = p1 or p2

       # Return the head node of the merged list
       return memo.next
```

## Template 2: Using 'or' condition
The second template uses the 'or' condition in the while loop. In this case, we exit the while loop until both pointers have reached the ends of ther respective lists. Consequently, all appending operations must be handled within the while loop itself.

Note the condition for appending the node at `p1` to the new list, specifically the line `if p1 and (not p2 or p1.val < p2.val)`. This condition has two parts:

1. `p1`: This ensures that we check the existence of `p1` before attempting to access its value. It acts as a safeguard against null reference exceptions which could occur if `p1` were null.
2. `not p2 or p1.val < p2.val`: This part of the condition serves two purposes:
    - `not p2`: This checks if `p2` has reached the end of `list2`. If it has, and since `p1` is not null (ensured by the first part of the condition), the node at `p1` is appended to the new list.
    - `p1.val < p2.val`: This checks if the value at `p1` is less than the value at `p2`. If true, it means `p1`'s node should be appended next in order to maintain order in the merged list.

If the condition fails (i.e., `p1` is null or `p1.val` is not less than `p2.val` while `p2` is not null), the node at `p2` is appended to the new list. This structure ensures that the merging process continues seamlessly by always choosing the smaller node between `p1` and `p2` until both lists are completely traversed.

This approach is particularly effective in scenarios where one list may finish before the other, allowing the remaining elements of the non-empty list to be appended in one go, thereby completing the merge.


```python
class Solution(object):
    def mergeTwoLists(self, list1, list2):

        new_list = ListNode()
        memo = new_list

        # Pointers for the two input linked lists
        p1 = list1
        p2 = list2

        # Merge the two lists by comparing the values of the nodes
        while p1 or p2:
            if p1 and (not p2 or p1.val < p2.val):
                new_list.next = p1
                p1 = p1.next
            else:
                new_list.next = p2
                p2 = p2.next
            new_list = new_list.next

        # Return the head node of the merged list
        return memo.next

```

## Conclusion
In conclusion, understanding the subtle differences between the 'and' and 'or' conditions in the two pointers technique is crucial for tackling LeetCode problems effectively. The 'and' condition template can potentially save time by avoiding iterating over every element in both lists, but it may require extra code, which could make the solution look messier. In contrast, the 'or' condition template is more concise but requires iterating over all elements in both lists.

When solving LeetCode problems, consider both templates and evaluate which approach is better suited for the specific problem. Being able to adapt your approach based on the problem requirements will help you become a more versatile and skilled problem solver.
