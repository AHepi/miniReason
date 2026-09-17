# Working answer

Solution. The valid index domain is n a nonnegative integer and k an integer with 1 <= k <= n; when n=0 the sum is empty and equals 0. For n>=1, each denominator k(k+1)(k+2) is positive because k, k+1, and k+2 are positive integers; for all n>=0, 4(n+1)(n+2) is positive because n+1 and n+2 are positive; and 2 is nonzero. Thus every division is valid. For every integer k>=1, 1/[k(k+1)(k+2)] = (1/2)(1/[k(k+1)] - 1/[(k+1)(k+2)]). Summing k=1..n gives sum(k=1..n) 1/[k(k+1)(k+2)] = (1/2) sum(k=1..n)(1/[k(k+1)] - 1/[(k+1)(k+2)]). The sum telescopes to (1/2)(1/(1*2) - 1/[(n+1)(n+2)]) = 1/4 - 1/[2(n+1)(n+2)] = [(n+1)(n+2)-2]/[4(n+1)(n+2)] = n(n+3)/[4(n+1)(n+2)]. For every nonnegative integer n, sum(k=1..n) 1/[k(k+1)(k+2)] = n(n+3)/[4(n+1)(n+2)], with the empty sum equal to zero when n=0. In particular, for n=0 both sides are 0.

Stop reason: `complete`.
