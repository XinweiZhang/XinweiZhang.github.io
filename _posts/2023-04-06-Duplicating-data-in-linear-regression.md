---
layout: post
title: "Exploring the effects of data replication in linear regression"
description: "This classic problem tests the fundamentals of linear regression by examining the impact of data replication on least squares estimates, noise variance estimates, and t-statistics. Join us as we dive into this intriguing problem!"
date: 2023-04-03
tags: [Statistics]
keywords: statistic, linear regression, data replication
---


In this post, we explore the effects of data replication in linear regression, specifically examining how the least squares estimates, noise variance estimates, and $$t$$-statistics change after duplicating data. We consider two variations of this problem and provide solutions to both cases:
* [Case 1](#case-1): We duplicate both $$x$$ and $$y$$.
* [Case 2](#case-2): We only duplicate $$x$$ but append $$y$$ with 0.

I want to clarify that the solutions presented here follow a principled statistical analysis and may **differ** from the standard interview solutions that will also be provided for comparison purposes.  This difference is due to the fact that the interview setting often involves incomplete or unclear assumptions, such as whether the iid assumption still holds after duplicating data. It is important to keep these differences in mind when considering the solutions presented here.

<!--more-->
## Recap of simple linear regression
Before we dive into the specific cases, let's first recap the basics of simple linear regression, which suffices to show the main idea (you may easily generalize it). Given the centered covariate vector $$x$$ and response vector $$y$$, the standard simple linear regression models postulates an underlying **true model**

$$
  y = x \beta + \varepsilon
$$

where $$\varepsilon \sim N(0, \sigma^2 I)$$. The LSE estimated coefficient is $$\hat{\beta} = (x^\intercal x)^{-1} x^\intercal y$$, and the variance of the estimated coefficient is

$$
  \text{Var}(\hat{\beta}) = \text{Var}((x^{\intercal}x)^{-1} x^{\intercal}y) = (x^{\intercal} x)^{-1} \sigma^2.
$$

The $$t$$-statistics for $$\beta$$ is defined as

$$
    t =\frac{\hat{\beta}}{\sqrt{\widehat{\text{Var}}(\hat\beta)}} =  \frac{\hat{\beta}}{\sqrt{(x^\intercal x)^{-1}\hat{\sigma}^2}}.
$$

where the estimator $$\hat{\sigma}^2$$ is obtained by dividing residual sum squares (RSS) by the (n-1) degree freedom
$$
    \hat{\sigma}^2 = [y^{\intercal}(I - x(x^{\intercal} x)^{-1}x^{\intercal}) y]/(n-1).
$$
One can show that under the assumption of the true model, the estimator $$\hat{\sigma}^2$$ is unbiased, i.e. $$E \hat{\sigma}^2 = \sigma^2.$$

### Case 1: Duplicated $$x$$ and $$y$$
#### Principled analysis
Let's consider the first case, where we duplicate both the covariate vector $$x$$ and the response vector $$y$$.  For convenience, we define the duplicated covariate vector $$x_d$$ and response vector $$y_d$$ as

$$
 x_d = \begin{pmatrix}
 x\\
 x
 \end{pmatrix} \quad \text{ and } \quad y_d= \begin{pmatrix}
 y\\
 y
 \end{pmatrix}.
$$

Using the subscript $$_d$$ to indicate results after duplication, we have the following:

* The coefficient estimate after duplicating the data remains the same:

  $$
      \hat{\beta}_d = (x_d^{\intercal} x_d)^{-1} x_d^{\intercal}y_d =  (2x^{\intercal} x)^{-1} (2x^{\intercal}y) = \hat{\beta}.
  $$
* The variance of $$\hat{\beta}_d$$ remains the same. We can reason directly that, since $$\hat{\beta}_d = \hat{\beta}$$, thus the variance of the coefficient estimate must also be the same.  Alternatively, we can calculate the variance as follows:

  $$
  \begin{aligned}
 \text{Var}(\hat{\beta}_d ) =  \text{Var}((x_d^{\intercal}x_d)^{-1} x_d^{\intercal}y_d)& =(x_d^{\intercal}x_d)^{-1} x_d^{\intercal} \text{Var}(y_d) x_d (x_d^{\intercal}x_d)^{-1} \\
  & = (x_d^{\intercal}x_d)^{-1}  x_d^{\intercal} \begin{pmatrix}
          I\sigma^2 & I\sigma^2\\
          I\sigma^2 & I\sigma^2\\
      \end{pmatrix}
   x_d (x_d^{\intercal}x_d)^{-1} \\
   &=(2x^{\intercal}x)^{-1} (4 x^{\intercal} x \sigma^2) (2x^{\intercal}x)^{-1} = (x^{\intercal}x)^{-1} \sigma^2.
  \end{aligned}
  $$

  The reason for providing the direct calculation here explicitly to emphasize an important point. The variance $$\text{Var}(y_d)$$ is not $$2n$$-dimensional identity matrix $$I_{2n}$$, because the duplicated data is not independent with the original data!

* The estimator of $$\sigma^2$$ and $$t$$-statistics: We can still use the RSS to estimate $$\sigma^2$$ by taking the degree of freedom now as $$2n-1$$, which gives the estimator based on duplicated data as:

  $$
  \hat{\sigma}_d^2 = \frac{y_d^{\intercal}(I_{2n} - x_d(x_d^{\intercal} x_d)^{-1}x_d^{\intercal}) y_d}{2n-1}=\frac{y^{\intercal}(1 - x(x^{\intercal} x)^{-1}x^{\intercal}) y}{n- \frac{1}{2}} = \frac{2n-2}{2n- 1}\hat{\sigma}^2.$$

  However, we will find that this estimator is biased, with a slightly larger value than $$\hat{\sigma}^2$$) and its expcetation, given by $$E[ \hat{\sigma}_d^2] = \frac{2n-2}{2n- 1}\sigma^2$$, shows it underestimate the true value. As a result, the $$t$$-statistics become larger as:

  $$
     t_d = \frac{\hat{\beta}_d}{\widehat{\text{Var}}(\hat{\beta}_d )} = \frac{\hat{\beta}_d}{\sqrt{(x^\intercal x)^{-1}\hat{\sigma}_d^2}} = \sqrt{\frac{2n-1}{2n-2}}\frac{\hat{\beta}}{\sqrt{(x^\intercal x)^{-1}\hat{\sigma}^2}} = \sqrt{\frac{2n-1}{2n-2}} t.
  $$

  This shows that underestimating the variance increases the likelihood of test statistics being significant. However, we can adjust it by applying a correction factor to $$\hat{\sigma}_d$$ for unbiasedness, which makes the $$t$$-statistics remain the same.


#### Interview analysis
In some interview settings, the importance of rederiving the $$\text{Var}(\hat{\beta}_d)$$ may not be recognized or intentionally disregarded to solely test the candidate's ability to applying formulas. In this scenario, the true underlying model is implicitly assumed to be
$$
y_d = x_d + \varepsilon
$$
where $$\varepsilon \sim N(0, I_{2n})$$ after duplicating the data, and the components of $$y_d$$ are independent. We can use the formula in our first section to obtain the following results:


* The coefficient estimate after duplicating the data remains the same:

  $$
      \hat{\beta}_d = (x_d^{\intercal} x_d)^{-1} x_d^{\intercal}y_d =  (2x^{\intercal} x)^{-1} (2x^{\intercal}y) = \hat{\beta}.
  $$


* The estimator of $$\sigma^2$$ and $$t$$-statistics: The estimator of $$\sigma^2$$ based on 2n-1 degree freedom is still $$\hat{\sigma}_d^2 = \frac{2n-2}{2n- 1}\hat{\sigma}^2$$. The $$t$$-statistics becomes

  $$
     t_d = \frac{\hat{\beta}_d}{\sqrt{(x_d^\intercal x_d)^{-1}\hat{\sigma}_d^2}} =  \sqrt{2\cdot\frac{2n-1}{2n-2}}\frac{\hat{\beta}}{\sqrt{(x^\intercal x)^{-1}\hat{\sigma}^2}} \approx \sqrt{2} t
  $$

  Therfore, the $$t$$-statistics becomes approximately $$\sqrt{2}$$ times larger than before.



### Case 2: Duplicated $$x$$ and appended zeros to $$y$$
#### Principled analysis
Let's now consider the second case,  where we duplicate the covariate vector $$x$$ but append the response vector $$y$$ with 0. We similarly define the extended vectors

$$
 x_d = \begin{pmatrix}
 x\\
 x
 \end{pmatrix} \quad \text{ and } \quad y_d= \begin{pmatrix}
 y\\
 0
 \end{pmatrix}.
$$

In the following, we will repeatively use $$x_d^{\intercal} x_d = 2 x^{\intercal} x$$ and $$x_d^{\intercal} y_d = x^{\intercal} y $$.

* The coefficient estimate becomes half of the original LSE estimate:

$$
  \hat{\beta}_d = (x_d^{\intercal} x_d)^{-1} x_d^{\intercal}y_d = (2x^{\intercal} x)^{-1} x^{\intercal}y= \frac{1}{2} \hat{\beta}
$$

* The variance of $$\hat{\beta}_d$$ becomes one-fourth of the original variance: You may either directly reason that $$\text{Var}(\hat{\beta}_d) = \text{Var}(1/2\hat{\beta}) = 1/4\text{Var}(\hat{\beta})$$ or calculate it as follows:

  $$
  \begin{aligned}
 \text{Var}(\hat{\beta}_d ) =  \text{Var}((x_d^{\intercal}x_d)^{-1} x_d^{\intercal}y_d)& =(x_d^{\intercal}x_d)^{-1} x_d^{\intercal} \text{Var}(y_d) x_d (x_d^{\intercal}x_d)^{-1} \\
  & = (x_d^{\intercal}x_d)^{-1}  x_d^{\intercal} \begin{pmatrix}
          I\sigma^2 & 0\\
          0 & 0\\
      \end{pmatrix}
   x_d (x_d^{\intercal}x_d)^{-1} \\
   &=(2x^{\intercal}x)^{-1} (x^{\intercal} x \sigma^2) (2x^{\intercal}x)^{-1} = \frac{1}{4} (x^{\intercal}x)^{-1} \sigma^2.
  \end{aligned}
  $$

  The reason for providing the direct calculation is to emphasize that the variance of the duplicated data is different from $$I_{2n}$$, which is a consequence of appending 0 to the response vector.

* The estimator of $$\sigma^2$$ and $$t$$-statistics: Assuming the use of the $$2n-1$$ degree of freedom. we can calculate the estimator of $$\sigma^2$$ for this case as follows

  $$
  \begin{aligned}
  \hat{\sigma}_d^2 = \frac{y_d^{\intercal}(I_n - x_d(x_d^{\intercal} x_d)^{-1}x_d^{\intercal}) y_d}{2n-1} &= \frac{y^{\intercal}(I_n - \frac{1}{2}x(x^{\intercal} x)^{-1}x^{\intercal}) y}{2n-1} \\
    %               &=  \frac{y^{\intercal}(I_n - x(x^{\intercal} x)^{-1}x^{\intercal}) y}{2n-1} + \frac{1}{2} \frac{y^{\intercal}x(x^{\intercal}x)^{-1}x^{\intercal}y}{2n-1} \\
                   & = \frac{1}{2}\cdot \frac{2n-2}{2n-1}\cdot \hat{\sigma}^2 +  \frac{1}{2} \cdot\frac{1}{2n-1}\cdot \frac{(x^{\intercal} y)^2}{\|x\|_2^2},
  \end{aligned}
  $$

  where the estimator is in the form of a weighted combination of $$\hat{\sigma}^2$$ and $${(x^{\intercal} y)^2}/{\|x\|_2^2}$$. The expectation of the estimator is:

  $$
  \begin{aligned}
    E[\hat{\sigma}_d^2 ] & = \frac{1}{2n-1} E[\text{tr}(y^{\intercal}(I_n -\frac{1}{2} x(x^{\intercal} x)^{-1}x^{\intercal}) y)]\\
                        & =\frac{1}{2n-1} \text{tr}((I_n - \frac{1}{2}x(x^{\intercal} x)^{-1}x^{\intercal})E[yy^{\intercal}])\\
                        & =  \frac{1}{2}  \sigma^2 +  \frac{1}{2} \frac{\|x\beta\|_2^2}{2n-1} \\
  \end{aligned}
  $$

  where the calculation uses the linearity of the trace and expectation operators, $$\text{tr}(ab) = \text{tr}(ba)$$ and $$E[yy^{\intercal}] = \text{Var}(y) + E[y] E[y]^{\intercal} = \sigma^2 I_n +  x \beta\beta^{\intercal} x^{\intercal}$$.

  Therefore, depending on the signal-to-noise ratio (SNR) $$\text{SNR}=\|x\beta\|_2^2/\sigma^2$$, the estimator $$\hat{\sigma}_d^2$$ will overestimate the variance of noise $$\sigma^2$$ if $$\text{SNR} > 2n- 1$$ and underestimate $$\sigma^2$$ if $$\text{SNR} < 2n -1$$. It is unbiased only if $$\text{SNR} = 2n- 1$$.

  Empirically, the $$t$$-statistics is

  $$
    t_d = \frac{\hat{\beta}_d}{\sqrt{(x_d^\intercal x_d)^{-1}\hat{\sigma}_d^2}} = \frac{\frac{1}{2}\hat{\beta}}{\sqrt{\frac{1}{4}(x^\intercal x)^{-1}\hat{\sigma}_d^2}} = \frac{\hat{\beta}}{\sqrt{(x^\intercal x)^{-1}\hat{\sigma}_d^2}}
  $$

  and thus the value is influenced by $$\hat{\sigma}_d^2$$ which depends on the ratio between $${(x^{\intercal} y)^2}/{\|x\|_2^2}$$ and $$\hat{\sigma}^2$$. It is interesting to note that if we determine the threshold ratio at which $$\hat{\sigma}_d^2$$ becomes larger than $$\hat{\sigma}%2$$ after duplication, we obtain the inequality

  $$
  \frac{(x^\intercal y)^2}{\|x\|^2_2\|y\|_2^2} = R^2 > \frac{2n}{3n-1}.
  $$

  This means that if the coefficient of determination $$R^2$$ is greater than approximately 2/3, $$\hat{\sigma}_d^2$$ becomes larger, and the $$t$$-statistic becomes smaller, making it less likely to be significant.

  The results show that when you duplicate the $$x$$ values and append $$y$$ with 0s, you are essentially adding new data points with no relationship between $$x$$ and $$y$$ (since all the new $$y$$ values are 0). Consequently, the overall strength of the relationship between $$x$$ and $$y$$ in the entire dataset will be diluted if the original relationship is relatively strong. However, if the relationship is relatively weak ($$R^2<2/3$$), this modification might better highlight the true relationship between $$x$$ and $$y$$.




#### Interview analysis
Similarly, we have
* The coefficient estimate after duplicating the data becomes half of the original:

  $$
      \hat{\beta}_d = (x_d^{\intercal} x_d)^{-1} x_d^{\intercal}y_d =  (2x^{\intercal} x)^{-1} (x^{\intercal}y) = \frac{1}{2}\hat{\beta}.
  $$


* The estimator of $$\sigma^2$$ and $$t$$-statistics: The estimator of $$\sigma^2$$ based on $$2n-1$$ degree freedom is the same in the above. The $$t$$-statistics becomes

$$
   t_d = \frac{\hat{\beta}_d}{\sqrt{(x_d^\intercal x_d)^{-1}\hat{\sigma}_d^2}} =  \frac{\sqrt{2}}{2}\frac{\hat{\beta}}{\sqrt{(x^\intercal x)^{-1}\hat{\sigma}_d^2}}
$$

  Therfore, the $$t$$-statistics becomes approximately $$\sqrt{2}/{2}$$ times smaller, even if $$\hat{\sigma}_d^2 = \hat{\sigma}^2$$.
