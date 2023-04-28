---
layout: post
title: "Linear regression with group data"
description: "This post is suitable for readers who are familiar with linear regression and want to learn about a practical approach to dealing with grouped data. We hope that our discussion sheds some light on the trade-offs between computational efficiency and statistical accuracy when working with reduced data sets."
date: 2023-03-25
tags: [Statistics]
---


In this post, we discuss linear regression with grouped data and explore whether a certain reduction can be made when there are multiple responses given a covariate. The problem is formulated as follows:

Given data $$\left(y_{i j}, x_{i j}\right), 1 \leq j \leq n_i, 1 \leq i \leq m$$, and we are asked to fit the model

$$
y_{i j}=\alpha+\beta x_{i j}+\epsilon_{i j}
$$

where $$\epsilon_{i j}$$'s are i.i.d. $$N\left(0, \sigma^2\right)$$ and $$\sigma^2$$ is known. The experiment is arranged so that

$$
\qquad\qquad x_{i j}=x_i, \quad 1 \leq j \leq n_i, 1 \leq i \leq m
$$

and the consequence of the model above is that

$$
\text{E}[\bar{y}_i]=\beta_0+\beta_1 x_i, 1 \leq i \leq m,\quad \bar{y}_i=\sum_{j=1}^{n_i} y_{i j} / n_i .
$$


1. Whether some of our time can be saved by using $$m$$ pairs $$\left(\bar{y}_i, x_i\right)$$ instead of the original data points.?

    Answer: If we know $$n_i$$ of each group, we can use reduced pairs and get the same estimator as from the original data.

<!--more-->
2. What if we can use $$n_i$$ for each $$i$$ as well?

    Answer:  If we know $$n_i$$ of each group, we can use reduced pairs and get the same estimator as from the original data.

3. What if $$\sigma^2$$ is unknown?

    Answer: If $$\sigma^2$$ is unknown, we still recommend using the original data over reduced pairs as the maximum likelihood estimator of the noise variance $$\sigma^2$$ based on original data points has a smaller variance.


Quick links to the proofs: [Proof to question 1](#proof-to-question-1), [Proof to question 2](#proof-to-question-2), [Proof to question 3](#proof-to-question-3).


## Proof to question 1
**Answer:** If we know $$n_i$$ of each group, we can use reduced pairs and get the same estimator as from the original data.

**Proof:** Denote the design matrix and the response of the original data points as $$X$$ and $$Y$$

$$
    X=\begin{pmatrix}
        \mathbf{1}_{n_1} & x_1 \mathbf{1}_{n_1}\\
        \vdots & \vdots\\
        \mathbf{1}_{n_m} & x_m \mathbf{1}_{n_m}
    \end{pmatrix} \quad\text{and}\quad Y=\begin{pmatrix}
    y_{11}\\
    \vdots\\
    y_{1n_1}\\
    \vdots\\
    y_{m1}\\
    \vdots\\
    y_{mn_m}
    \end{pmatrix}.
$$

Now we define an indicator matrix $$N$$ and a weight matrix $$W$$ as

$$
    N=\begin{pmatrix}
        \mathbf{1}_{n_1} & \cdots& 0 \\
        \vdots  &  \ddots   & \vdots
        \\0 & \cdots & \mathbf{1}_{n_m}
        \end{pmatrix}, \quad \text{and} \quad
    W=N^\intercal N=\text{diag}(n_1,\dots,n_m),
$$

We can represent the reduced pairs with the weight matrix $$W$$ to be

$$
    \bar X = W^{-1} N^\intercal  X \quad\text{and}\quad \bar Y =W^{-1} N^\intercal  Y.
$$

Denote $$\hat \beta$$ as the estimator based on the original data points and $$\hat{\beta}^{\ast}$$ as the estimator based on reduced pairs. Then we can write OLS estimators as

$$
\begin{aligned}
    \hat{\beta}&=(X^\intercal X)^{-1}X^\intercal Y\\
    \hat{\beta}^{\ast}&=(\bar{X}^\intercal \bar{X})^{-1}\bar{X}^\intercal \bar{Y}=(XNW^{-2}NX)^{-1}XNW^{-2}NY.
\end{aligned}
$$

Assuming the true mean of $$Y$$ is $$\text{E}(Y) = X\beta$$, it's easy to show that both estimators are unbiased:

$$
\begin{aligned}
    \text{E} (\hat{\beta}) &= (X^\intercal X)^{-1}X^\intercal  \text{E} (Y) = \beta\\
     \text{E} (\hat{\beta}^{\ast})& = (XNW^{-2}NX)^{-1}XNW^{-2}N \text{E}(Y) = \beta.
\end{aligned}
$$

The variance of both estimators are

$$
\begin{aligned}
    \text{Var}(\hat{\beta}) &= (X^\intercal MX)^{-1} X^\intercal MMX(X^\intercal MX)^{-1} \sigma^2\\
    \text{Var}(\hat{\beta}^{\ast})& = (X^\intercal X)^{-1} \sigma^2
\end{aligned}
$$

where $$M=NW^{-2}N$$. Comparing the two variance, we can find out that

$$
\begin{aligned}
    &\text{Var}(\hat{\beta}^{\ast})-\text{Var}(\hat{\beta})\\
    =&[\sigma(MX(X'MX)^{-1}-X(X^\intercal X)^{-1})]^\intercal [\sigma(MX(X'MX)^{-1}-X(X^\intercal X)^{-1})]\geq0,
\end{aligned}
$$

Therefore, the varaince of the OLS estimator from the reduced paris are larger than that of OLS estimator from the original data points, i.e.,

$$
    \text{Var}(\hat{\beta}^{\ast})\geq \text{Var}(\hat{\beta}).
$$

So the OLS estimator from the original data points would be more efficient than the estimator from the reduced pairs.


## Proof to question 2
**Answer:**  If we know $$n_i$$ of each group, we can use reduced pairs and get the same estimator as from the original data.


**Proof:** If we know $$n_i$$ of each group, then we can use weighted least square on the reduced data set by minimizing the following objective function

$$
    \min_{\beta}(\bar{Y} - \bar{X}\beta)^\intercal W(\bar{Y}-\bar{X}\beta).
$$

The solution can be written as

$$
    \hat{\beta}^{\ast\ast}=(X^\intercal VX)^{-1}X^\intercal VY.
$$

where $$V= NW^{-1}N^\intercal $$. We claim that $$\hat{\beta}^{\ast\ast}=\hat{\beta},$$ indicating that the solution of the weighted least squares based on the reduced data set is exactly the same as the solution of the least squares on the full data set.

We prove this by showing that $$X^\intercal  VX=X^\intercal  X$$ and $$X^\intercal =X^\intercal V$$:

$$
\begin{aligned}
    X^\intercal VX &= \begin{pmatrix}
    \mathbf{1}_{n_1}' & \dots & \mathbf{1}_{n_m}'\\
    x_1\mathbf{1}_{n_1}' & \dots & x_m\mathbf{1}_{n_m}'
    \end{pmatrix}
    \begin{pmatrix}
    \frac{1}{n_1}\mathbf{1}_{n1}\mathbf{1}_{n1}'&&\\
    &\ddots&\\
    &&\frac{1}{n_m}\mathbf{1}_{nm}\mathbf{1}_{nm}'
    \end{pmatrix}\begin{pmatrix}
    \mathbf{1}_{n_1} & x_1\mathbf{1}_{n_1}\\
    \vdots & \vdots\\
    \mathbf{1}_{n_m} & x_m\mathbf{1}_{n_m}
    \end{pmatrix}\\
    &=\begin{pmatrix}
    \sum_{i=1}^m n_i & \sum_{i=1}^m n_i x_i\\
    \sum_{i=1}^m n_ix_i & \sum_{i=1}^m n_ix_i^2
    \end{pmatrix} = X^\intercal X
\end{aligned}
$$

and

$$
\begin{aligned}
    X^\intercal V&= \begin{pmatrix}
    \mathbf{1}_{n_1}' & \dots & \mathbf{1}_{n_m}'\\
    x_1\mathbf{1}_{n_1}' & \dots & x_m\mathbf{1}_{n_m}'
    \end{pmatrix}
    \begin{pmatrix}
    \frac{1}{n_1}\mathbf{1}_{n1}\mathbf{1}_{n1}'&&\\
    &\ddots&\\
    &&\frac{1}{n_m}\mathbf{1}_{nm}\mathbf{1}_{nm}'
    \end{pmatrix}\\
    &=\begin{pmatrix}
    \mathbf{1}_{n_1}' & \dots & \mathbf{1}_{n_m}'\\
    x_1\mathbf{1}_{n_1}' & \dots & x_m\mathbf{1}_{n_m}'
    \end{pmatrix} =X^\intercal .
\end{aligned}
$$

Therefore, we conclude $$\hat{\beta}^{\ast\ast}=\hat{\beta}$$.

## Proof to question 3
**Advise:** If $$\sigma^2$$ is unknown, using the original data is still preferable than using the reduced pairs.

**Proof:**
If $$\sigma^2$$ is unknown, but $$n_i$$ is known. We define the mean squared error (adjusted to degree of freedom) as

$$
    S^{2^{\ast}}=\frac{(\bar{Y}-\bar{X}\hat{\beta})^\intercal  W(\bar{Y}-\bar{X}\hat{\beta})}{m-2}
$$

Denote $$V = NW^{-1}N$$, we can calculate that

$$
\begin{aligned}
    (\bar{Y}-\bar{X}\hat{\beta})^\intercal  W(\bar{Y}-\bar{X}\hat{\beta}) &= (W^{-1}N(Y-X\hat{\beta}))^\intercal W(W^{-1}N(Y-X\hat{\beta}))\\
    &=Y^\intercal ( I - H)V(I- H)Y.
\end{aligned}
$$

Based on the relationship that $$X^\intercal V=X^\intercal $$, $$VX=X$$, and

$$
    (I - H)^\intercal V(I- H) = (V -V H -  H V + H V H) = V- H,
$$

we obtain

$$
    (\bar{Y}-\bar{X}\hat{\beta})^\intercal W(\bar{Y}-\bar{X}\hat{\beta})= Y^\intercal (V- H)Y.
$$

Note $$V- H$$ is idempotent, symmetric, $$\text{trace}(V- H)=m-2$$ and  $$Y\sim N(X\beta,\sigma^2  I)$$. Hence, using the knowledge about $$\chi^2$$ distribution, we have

$$
S^{2^\ast} \sim \sigma^2 \frac{\chi_{m-2}^2}{m-2}(\delta).
$$

where $$\delta = \beta^\intercal  X^\intercal  (V- H) X\beta =0$$.

For the regression based on original data points, by classical theory, we have the mean squared error (adjusted to degree of freedom) $$S^2$$ as :

$$
    S^2= \frac{Y^\intercal (I- H)Y}{N-2} \sim \sigma^2\frac{\chi_{N-2}^2}{N-2}.
$$

For both $$S^2$$ and $$S^{2^\ast}$$, they are unbiased estimator since

$$
    \text{E}(S^2)=\sigma^2 \quad\& \quad \text{E}(S^{2^\ast})=\sigma^2.
$$

The variance of  $$S^2$$ and $$S^{2^\ast}$$ are respectively
$$
    \text{Var}(S^2)=\frac{1}{(N-2)^2}\cdot\text{Var}(\chi^2_{N-2})=\frac{2\sigma^4}{N-2}
$$

and

$$
    \text{Var}(S^{2^{\ast}})=\frac{1}{(m-2)^2}\cdot\text{Var}(\chi^2_{m-2})=\frac{2\sigma^4}{m-2}.
$$

Since $$N=\sum_{i=1}^m n_i \geq m$$, $$S^2$$ has a smaller variance than $$S^{2^{\ast}}$$. It means the maximum likelihood estimator of the noise variance $$\sigma^2$$ based on original data points has a smaller variance.
