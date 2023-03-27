---
layout: post
title: "Finding the Expected Number of Uniform Random Variables to Exceed 1"
description: "In this post, we explore the problem of finding the expected number of uniform random variables needed for their sum to exceed 1. We provide two different solutions to this problem and explain the underlying concepts of probability and geometric intuition. This problem is a classic example in probability theory and has practical applications in fields such as finance and statistics. Join us as we delve into the world of probability and explore this fascinating problem!"
date: 2023-03-26
tags: [probability]
---

## Problem

Given $$X_1,...,X_n$$ are iid random variables following a uniform distribution on the interval $$[0,1]$$, what is the expected value of the minimum number of these variables needed for their sum to exceed 1?

## Solution 1
Let $$N$$ be the random variable representing the minimum number of uniform random variables needed for their sum to exceed 1, i.e.,

$$N = \inf_n \{ \sum_{i=1}^n X_i > 1\}.$$

In the first solution, we calculate the expectation by the definition: $$E[N] = \sum_{n=1}^\infty n P(N=n).$$

To determine $$P(N=n)$$, we first calculate the probability of the sum $$S_n = \sum_{i=1}^n X_i$$ being less than or equal to 1, denoted by $$P(S_n \leq 1)$$. Geometrically, we can consider the $$(n-1)$$-dimensional simplex $$T_n = \{x_i\geq 0:x_1+\cdots+x_n\leq 1\}$$, which represents the set of all points in the $$n$$-dimensional space where the sum $$S_n$$ is less than or equal to 1. Since the joint distribution of $$X_1, \ldots, X_n$$ is uniform over the unit hypercube $$[0, 1]^n$$, the probability of a point in the $$n$$-dimensional space falling into a specific region is proportional to the volume of that region. Therefore, the probability of $$S_n$$ being less than or equal to 1 is equal to the ratio of the volume of $$T_n$$ to the volume of the unit hypercube, which is 1.

The volumes of $$T_2$$ and $$T_3$$ are $$1/{2!}$$ and $$1/{3!}$$, respectively, as known from geometry. In general, $$T_n$$ is has a volume of $$1/n!$$, yielding the probability $$P(S_n \leq 1) = \vert T_n  \vert = 1/n!$$. Then, for $$n\geq 2$$, the probability is

$$
\begin{aligned}
    P(N=n) &= P(S_{n-1} \leq 1 \text{ and } S_n > 1) \\
            &= P(S_{n-1} \leq 1) - P(S_n \leq 1)\\
            & =  \frac{1}{(n-1)!} - \frac{1}{n!}\\
            & = \frac{n-1}{n!}.
\end{aligned}
$$

where the second equality holds because $$\{S_{n} \leq 1\} \subseteq \{S_{n-1}\leq 1\}$$. Moreover, we have $$P(N=1) = P(X_1 > 1) = 0$$.
Now we can calculate the expected number of uniform random variables for their sum to exceed 1:

$$
\begin{aligned}
E[N] &= \sum_{n=1}^\infty n P(N=n)= \sum_{n=2}^\infty \frac{1}{(n-2)!}= \sum_{t=0}^\infty \frac{1}{t!} = e.
\end{aligned}
$$

Therefore, the expected value of the minimum number of these variables needed for their sum to exceed $$1$$ is $$e$$.
