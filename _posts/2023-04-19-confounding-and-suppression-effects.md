---
layout: post
title: "Exploring the intricacies of confounding and suppression effects in linear regression: A deeper look"
description: "In this post, we dive deep into the interpretation of regression coefficients and their t-tests, highlighting the importance of understanding the full model view and submodel view. Uncover the subtle points in interpreting the significance of t-tests and learn why a significant t-test result does not necessarily indicate a good predictor. Join us as we explore these fundamental issues and enhance your understanding of linear regression."
date: 2023-04-19
tags: [Statistics]
---

In this post, I want to write something that is often overlooked about confounding effects and suppression effects. I was prompted to investigate this topic by the following question:

| When we run a regression of $$y\in \mathbb{R}^n$$ on both $$x_1, x_2\in\mathbb{R}^n$$, the $$t$$-tests for both predictors are significant. However, when we run a regression on each predictor individually, the $$t$$-test is insignificant. What could be the reason for this?

While the answer to this is suppression effects which are visually explained in the StackExchange answers by [Jake Westfall](https://stats.stackexchange.com/a/74353/114120) and [ttnphns](\href{https://stats.stackexchange.com/a/73876/114120}), and in Friedman and Wall (2005), I realize some fundamental issues need to emphasize beyond the technical consideration.

This question raises fundamental issues in understanding linear regression. In a typical linear regression book, when introducing linear regression and the related results, it only considers one model at hand with fixed predictor variables. Therefore, the interpretation of regression coefficients and their $$t$$-tests are crystal clear, and there is no ambiguity. However, when considering different linear models with different predictors simultaneously, the interpretation of regression coefficients and their $$t$$-tests becomes ambiguous and subtle.


In this post, I aim to illustrate the three points:
* The meaning of linear regression coefficients changes when considering different models.
* The change in the significance of $$t$$-tests is not purely related to the change in the explanation of the variability in $$Y$$ after including the confounder/suppressor. It is more likely due to the change in the inference target.
* The significance of the $$t$$-test should be carefully considered and not hastily regarded as an indicator of a good predictor.

<!--more-->


To begin, I will discuss the two different views of linear regression coefficients: the full model view and the submodel view.
## Full model view and submodel view
### background
The distinction between the two interpretations of linear regression coefficients was introduced by Berk (2013). Let us consider a three-variable setting where we have a random response variable $$Y$$ and random predictor variables $$X_1$$ and $$X_2$$, all assumed to be centered and standardized for simplicity.

* Full model view: The full model view assumes that the equation describes a "data-generating" mechanism for the response, hence having a causal interpretation. In this specific setting, the linear regression postulates a data-generating process with true parameters $$(\beta_1^\ast, \beta_2^\ast)$$ depicted by the equation:

$$
   (F_0)\quad  Y = X_1 \beta_1^\ast + X_2 \beta_2^\ast + \varepsilon
$$

where $$\varepsilon\sim N(0,\sigma^2)$$. The two degenerated equations

$$
\begin{aligned}
   (F_1)\quad   Y = X_1 \beta_1^\ast + \varepsilon, \\
 (F_2)\quad     Y = X_2 \beta_2^\ast + \varepsilon,
\end{aligned}
$$

imply that the true coefficient of the deselected predictor is 0, i.e., $$\beta_2^\ast$$ is 0 or $$\beta_1^\ast$$ is 0 for the $$F_1$$ and $$F_2$$ equations, respectively.


* Submodel view: The submodel view assumes that any equation merely describes the association between predictor and response variables, with no data-generating or causal claims implied. Therefore, the following three equations are equivalent candidate working models for approximation purposes:

$$
\begin{aligned}
 (M_0)\quad Y &= X_1 \beta_{1\cdot M_0} + X_2 \beta_{2\cdot M_0} + \varepsilon_0\\
 (M_1)\quad Y &= X_1 \beta_{1\cdot M_1} + \varepsilon_1 \\
 (M_2)\quad Y &= X_2 \beta_{2\cdot M_2} + \varepsilon_2
\end{aligned}
$$

where $$\varepsilon_i$$'s absorb both approximation errors and random noises. As the notation suggests, under the submodel view, the meaning of a predictor's coefficient depends on which predictors are included in the model. For example, $$\beta_{1\cdot M_0}$$ does not have the same meaning as $$\beta_{1\cdot M_1}$$. It is also worth noting that the coefficients of excluded predictors in $$M_1$$ and $$M_2$$ are not 0; they are not defined and therefore do not exist.

Within the submodel view, it is improper to assume first-order correctness anymore, as the expectation $$E[Y\rvert X_{M_i}]=\mu(X_{M_i})$$ is not necessarily a linear function in $$X_{M_i}$$. The $$M_0$$ model is only regarded as the repository of all available predictors. The true parameters for model $$M_i$$ in the submodel view are defined as the minimizer of the $$L_2$$ loss in the population space:

$$
    \beta_{M_i}^\ast = \arg\min_{\beta} (Y - X_{M_i} \beta_{M_i} )^2
$$

where we use $$X_{M_i}$$ and $$\beta_{M_i}$$ to indicate all predictors and corresponding coefficients associated with model $$M_i$$.  Therefore, assuming solvability, the true parameter can be obtained as

$$
    \beta_{M_i}^\ast = (E[X_{M_i}^\intercal X_{M_i}])^{-1}E[X_{M_i}^\intercal Y]
$$


## Problem in full model view
The reason we detour first to discuss the full model view and the submodel view of model parameters is that the estimation and inference only make sense under the submodel view when discussing the confounding effect and suppression effect. Otherwise, under the full model view, one can show that when assuming the $$F_0$$ as the correct model but regressing $$Y$$ only on $$X_1$$, the OLS estimator is biased unless $$X_1$$ and $$X_2$$ is uncorrelated or $$\beta_2^\ast=0$$

$$
 E(\hat{\beta}_1) = \beta_1^\ast + (E X_1^2)^{-1} E[X_1X_2]\beta_2^\ast.
$$

This means, in general, when you believe $$F_0$$ is the true data-generating process, there is no reason to think about $$F_1$$ or $$F_2$$ model. The corresponding $$t$$-tests in $$F_1$$ or $$F_2$$ models are meaningless because they are not valid tests about the null hypotheses $$H_0:\beta_1^\ast=0$$ or $$H_0:\beta_2^\ast=0$$. (Or at least the actual distribution of the $$t$$-statistics follows a non-central $$t$$-distribution, thus it no longer can be inpterated based on standard $$t$$ value).

## Estimation and inference under submodel view
In the most general case, when nonlinearity is allowed in $$\mu(X)$$, the estimation and inference are even more subtle due to the ancillarity of the regressor $$X$$ would fail, and $$X$$ can not be treated as fixed. We refer to Buja et al. (2020) for further information.

Below, we consider relatively restrictive assumptions which allow the simultaneous consideration of different linear models and suffices to serve our main purpose. Specifically, we assume $$(Y,X_1,X_2)$$ jointly follows a multivariate normal distribution such that $$E[Y\rvert  X_{M_i}]=\mu(X_{M_i})$$ is always linear for $$i=0,1,2$$. Assume the real data obtained are $$y, x_1, x_2 \in \mathbb{R}^n$$, then the OLS estimator

$$
    \hat{\beta}_{M_i} = (x_{M_i}^\intercal x_{M_i})^{-1} x_{M_i}^\intercal y
$$

is an unbiased estimator for $$\beta_{M_i}^\ast$$. The parameters have the usual interpretations when people teach regression, that is, "the average difference in the response for a unit difference in the predictor, at fixed levels of all other predictors in the model." Furthermore, we have the $$t$$-test valid

$$
    t_{j\cdot M_i}  = \frac{\hat{\beta}_{j\cdot M_i}}{\sqrt{\hat{\sigma}_{M_i}^2/\|x_{j\cdot M_i}\|_2^2 }}
$$

for the hypothesis $$H_0:  \beta^\ast_{j\cdot M_i} = 0$$ when a predictor $$j$$ is included in the model $$M_i$$. We emphasize that, under the submodel view, the estimation and inference target depends on the model being considered.




## Confounding effect and suppression effect
### Definitions
There are different definitions of the confounding effect and the suppression effect. A precise definition is not the main interest of this post. Below, I provide a definition only to serve the purpose of this post.

* Confounding effect: The inclusion of both predictors in a linear model decreased the magnitude of the linear coefficient.

* Suppression effect: Tnclusion of both predictors in a linear model increased the magnitude of the linear coefficient.


In the remaining section, we illustrate the related impact on estimation and inference, assuming that $$Y$$, $$X_1$$, and $$X_2$$ jointly follow a normal distribution:

$$
    \begin{pmatrix}
        Y\\
        X_1\\
        X_2
    \end{pmatrix} \sim N\left(  \begin{pmatrix}
        0\\
        0\\
        0
    \end{pmatrix},   \begin{pmatrix}
        1 &\rho_{y1} &\rho_{y2} \\
        \rho_{y1} & 1 &\rho_{12} \\
        \rho_{y2} &\rho_{12} &1 \\
    \end{pmatrix} \right).
$$

We assume $$\rho_{y1} = \rho_{y2} = \alpha$$ in the following discussion, while the readers may derive other cases if interested or refer to Friedman and Wall (2005). Now, one can calculate the estimation targets for the three models:

$$
\begin{aligned}
    (M_0)\quad &
    \begin{pmatrix}
        \beta_{1\cdot M_0}^\ast\\
        \beta_{2\cdot M_0}^\ast\\
    \end{pmatrix}=
    \begin{pmatrix}
        \frac{\alpha}{1+\rho_{12}}\\
       \frac{\alpha}{1+\rho_{12}}\\
    \end{pmatrix}\\
    (M_1)\quad &\beta_{1\cdot M_1}^\ast = \alpha \\
    (M_2)\quad &\beta_{2\cdot M_2}^\ast = \alpha    
\end{aligned}
$$



Therefore, when $$1>\rho_{12} > 0$$, the confounding effect appears, and the coefficient of $$X_1$$ becomes smaller after considering $$X_1$$ and $$X_2$$ together, i.e.,

$$\beta_{1\cdot M_0}^\ast = \frac{\alpha}{1+\rho_{12}} < \alpha =  \beta_{1\cdot M_1}^\ast$$

On the contrary, when $$0>\rho_{12} > -1$$, the suppression effect appears, and the coefficient of $$X_1$$ becomes smaller after considering $$X_1$$ and $$X_2$$ together, i.e.,

$$\beta_{1\cdot M_0}^\ast = \frac{\alpha}{1+\rho_{12}} > \alpha =  \beta_{1\cdot M_1}^\ast$$

However, the change of the magnitude of the coefficient does not mean it is a better or worser predictor because the meaning of the coefficient has changed. Furthermore, as one may realize, multicollinearity also interferes with the confounding and suppression effects. One may further derive the formula for $$t$$-statistics as a function of $$\rho_{12}$$ to see how the change for the collineartiy in different region. We save this for the future writing.


### Subtle point in interpreting the significance of $$t$$-test
In the context of linear regression, people often make the mistake of thinking that a significant t-test result for a regression coefficient indicates a statistically significant relationship between the independent variable associated with that coefficient and the dependent variable, implying that the independent variable is a good predictor of the dependent variable. However, this is an overly optimistic interpretation of the power of a t-test. In reality, the t-test only provides information about the confidence of $$\hat{\beta}_{j\cdot M_i}\neq 0$$, and the non-zeroness of $$\hat{\beta}_{j\cdot M_i}$$ does not necessarily imply that it is a good predictor.

We illustrate the problem and revisit the original issue that we introduced at the beginning of the post. To demonstrate the impact of multicollinearity on the significance of the $$t$$-test, we consider an extreme case where $$\alpha = 0.01$$ and $$\rho=-0.999$$. In this case, the true coefficient for $$X_1$$ in the model $$M_0$$ is

$$\beta_{1\cdot M_0}^\ast = 10.$$

Then the $$t$$-test is likely to produce significant results, despite the influence of multicollinearity on the estimation of variance, as we can seen from the following  simulation based on $$50$$ observations:

```r
set.seed(123)

mat <- rbind(c(1,.01,.01),
             c(.01,1,-.999),
             c(.01,-.999,1))
dat <- data.frame(mvrnorm(n=50, mu=numeric(3), empirical=T, Sigma=mat))
names(dat) <- c("y","x1","x2")
```

The model $$M_0$$ summary shows:

```
Coefficients:
   Estimate   Std. Error t value Pr(>|t|)   
x1   10.000      2.887   3.463  0.00113 **
x2   10.000      2.887   3.463  0.00113 **
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 0.9037 on 48 degrees of freedom
Multiple R-squared:    0.2,	Adjusted R-squared:  0.1667
F-statistic:     6 on 2 and 48 DF,  p-value: 0.004722
```
As shown, the $$t$$-test is significant in the model $$M_0$$. However, the $$R^2$$ value is only 0.2, and we already know that $$X_1$$ is not a good predictor of $$Y$$ due to the low correlation.

On the other hand, the summary of models $$M_1$$ and $$M_2$$ shows insignificant $$t$$-test results:
```
M1
Coefficients:
   Estimate   Std. Error t value Pr(>|t|)
x1   0.0100     0.1429    0.07    0.944

M2:
Coefficients:
   Estimate   Std. Error t value Pr(>|t|)
x2   0.0100     0.1429    0.07    0.944

```

This simulation serves as an example of the phenomenon presented in the original problem, and sheds light on the overlooked side in my exploration of the available answers.


## Reference
Berk, R., Brown, L., Buja, A., Zhang, K., & Zhao, L. (2013). Valid post-selection inference. The Annals of Statistics, 802-837.

Friedman, L., & Wall, M. (2005). Graphical views of suppression and multicollinearity in multiple linear regression. The American Statistician, 59(2), 127-136.
