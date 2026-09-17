# Working answer

Proof. For every nonnegative integer k, 1/(k+1) = ∫_0^1 x^k dx. Substituting into the finite sum gives sum_{k=0}^{n} (-1)^k binom(n,k)/(k+1) = sum_{k=0}^{n} (-1)^k binom(n,k) ∫_0^1 x^k dx. Because the sum over k=0,...,n is finite, linearity of the integral justifies interchanging the finite sum and the integral: sum_{k=0}^{n} (-1)^k binom(n,k) ∫_0^1 x^k dx = ∫_0^1 sum_{k=0}^{n} (-1)^k binom(n,k) x^k dx. By the binomial theorem, sum_{k=0}^{n} (-1)^k binom(n,k) x^k = (1-x)^n. Combining the previous steps yields sum_{k=0}^{n} (-1)^k binom(n,k)/(k+1) = ∫_0^1 (1-x)^n dx. The integral evaluates as ∫_0^1 (1-x)^n dx = ∫_0^1 u^n du = 1/(n+1). Therefore, for every nonnegative integer n, sum_{k=0}^{n} (-1)^k binom(n,k)/(k+1) = 1/(n+1).

Stop reason: `complete`.
