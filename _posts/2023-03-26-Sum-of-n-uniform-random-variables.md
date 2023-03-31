---
layout: post
title: "Finding the expected mumber of uniform random variables to exceed 1"
description: "In this post, we explore the problem of finding the expected value of minimum number of uniform random variables needed for their sum to exceed 1. We provide two different solutions to this problem and explain the underlying concepts of probability and geometric intuition. This problem is a classic example in probability theory. Join us as we delve into the world of probability and explore this fascinating problem!"
date: 2023-03-26
tags: [Probability]
---

## Problem

Given $$X_1,...,X_n$$ are iid random variables following a uniform distribution on the interval $$[0,1]$$, what is the expected value of the minimum number of these variables needed for their sum to exceed 1?

### Solution 1
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


### Solution 2

We can solve this problem using an approach similar to the coupon collector problem. Define the random variable $$N(t) = \inf_n \{ \sum_{i=1}^n X_i > t\}$$ and its expectation as $$M(t) = E[N(t)]$$.

Our goal is to find $$M(1)$$. We can compute $$M(1)$$ by conditioning on the first value $$X_1$$:

$$
    M(1) = E[N(1)] =  E_{X_1}[ E[N(1) | X_1 = t ] ]= \int_{0}^1 E[N(1) | X_1 = t ]\cdot 1 d t
$$

By the definition of $$N(t)$$, if $$X_1$$ equals to a value $$t$$, then it remains to find:

$$
E[N(1) | X_1 = t ] = E[N(1-t)] + 1
$$

This equation represents the idea that, given the first variable $$X_1$$ taking the value $$t$$, we now need to find the expected number of additional uniform random variables required for their sum to exceed $$1-t$$, while accounting for the contribution of the first variable $$X_1$$ we have already considered.

Therefore, we have:

$$
    M(1) = \int_{0}^1E[N(1-t)] + 1 d t = 1 + \int_{0}^1M(1-t)d t.
$$

Now we want to derive a general formula for $$M(t)$$ for $$0\leq t \leq 1$$. Similar calculations give:

$$
    M(t) =  1 + \int_{0}^t M(t-s)d s.
$$

In the equation, we want to simplify the expression in the second term. To do this, we can do change of variable. We introduce a new variable, $$u$$, and set $$u=t-s$$. This helps us rewrite the expression inside the integral in a simpler form:

$$
M(t) = 1 + \int_{0}^t M(u) du
$$

This change of variable makes the equation easier to work with and allows us to proceed with finding the expected value. Now we can take the derivative with respect to $$t$$ on both sides, and with Leibniz rule, we get:

$$
  M'(t) = M(t),
$$

which is a differential equation with the initial condition $$M(0) = 1$$. Solving the differential equation gives:

$$
  M(t) = e^{t}.
$$

Plugging in $$t=1$$ gives the final answer: $$M(1) = e^1 = e$$.

### Extension
Now suppose we want to generalize the question to find the expected value of the minimum number of these variables needed for their sum to exceed an **arbitrary** $$t$$ where $$t \in [0, \infty]$$.

The first solution becomes challenging to work with due to the complexity of the probability $$P(S_n\geq t)$$, which involved [Irwin–Hall distribution](https://en.wikipedia.org/wiki/Irwin%E2%80%93Hall_distribution).

This difficulty highlights the advantages of directly working with expectations, as demonstrated in the second solution. We will still make use of the idea of conditioning on $$X_1$$. For $$t>1$$, we have  

$$
M(t) = 1 + \int_{0}^1 E[N(t-s)] d s = 1 + \int_{t-1}^t E[N(u)] d u = 1 + \int_{t-1}^t M(u) d u.
$$

Taking derivative w.r.t to $$t$$ yields a delayed differential equaiton

$$
M'(t) = M(t) - M(t-1)
$$

on $$t > 1$$. Combining this with the previously obtained differential equation for $$0\leq t\leq 1$$, we have the following system:

$$
\begin{aligned}
\begin{cases}
M'(t) = M(t), & 0 \leq t \leq 1,\\
M'(t) = M(t) - M(t-1), & t > 1.
\end{cases}
\end{aligned}
$$

with initial condition $$M(0)=1$$. While a general formula for the delayed equation is not obtainable, we can recursively find the solution on the intervals $$[1, 2], [2, 3], \dots$$. For example, consider $$t \in [1, 2]$$, the delayed differential equaiton now can be written as

$$
M'(t) = M(t) - e^{t-1}.
$$

This is an inhomogeneous first-order differential equation. We can find the integrating factor as:

$$
\mu(t) = \exp(\int_1^t -1 dt) = \exp(1-t).
$$

Uisng the integrating factor, we can determine the solution:

$$
m(t) = e^{t-1}( e - \int_{1}^t e^{1-t} e^{t-1} )d t = e^{t-1}( e - (t-1)) .
$$

In particular, we can find that $$m(2) = e^2 -e $$. By following this approach, we can continue obtaining formulas for other intervals.
