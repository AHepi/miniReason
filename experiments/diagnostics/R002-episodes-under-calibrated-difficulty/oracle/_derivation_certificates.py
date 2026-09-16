from fractions import Fraction as F
from math import comb

def check(cid):
    if cid=='C19':
        ok=all(sum((F(1,k*(k+1)*(k+2)) for k in range(1,n+1)),F(0))==F(n*(n+3),4*(n+1)*(n+2)) for n in range(0,65))
        trap=sum((F(1,k*(k+1)*(k+2)) for k in range(1,6)),F(0)) != F(1,4)
        return {'certificate_passed':ok,'certificate':'exact rational instances n=0..64','trap_check':{'kind':'counterexample','passed':trap,'detail':'n=5 sum is not the faulty constant 1/4'}}
    if cid=='C20':
        # Singular 2x2 certificate: A=diag(1,0), u=(2,3), v=(5,7).
        A=((1,0),(0,0));u=(2,3);v=(5,7)
        det=lambda M:M[0][0]*M[1][1]-M[0][1]*M[1][0]
        lhs=det(tuple(tuple(A[i][j]+u[i]*v[j] for j in range(2)) for i in range(2)))
        adj=((A[1][1],-A[0][1]),(-A[1][0],A[0][0]))
        rhs=det(A)+sum(v[i]*adj[i][j]*u[j] for i in range(2) for j in range(2))
        ok=lhs==rhs and det(A)==0
        return {'certificate_passed':ok,'certificate':'exact singular 2x2 adjugate smoke instance','trap_check':{'kind':'counterexample','passed':det(A)==0,'detail':'A is singular, so an A^-1-first route is undefined although the adjugate identity holds'}}
    if cid=='C21':
        a0=[0];a1=[1]
        for n in range(0,40):
            xp1=[0]+a1; xp1 += [0]*(max(len(a1),len(a0)+1)-len(xp1));
            base=a1+[0]*(len(xp1)-len(a1)); xa0=[0]+a0+[0]*(len(xp1)-len(a0)-1)
            a2=[base[i]+xp1[i]-xa0[i] for i in range(len(xp1))]
            a0,a1=a1,a2
        ok=all(c==1 for c in a1)
        trap_x=1;trap_n=3;trap_numerator=trap_x**trap_n-1;trap_denominator=trap_x-1;trap_polynomial_sum=sum(trap_x**j for j in range(trap_n))
        trap_passed=(trap_numerator==0 and trap_denominator==0 and trap_polynomial_sum==trap_n)
        return {'certificate_passed':ok,'certificate':'coefficient recurrence instances through n=41','trap_check':{'kind':'domain-counterexample','passed':trap_passed,'x':trap_x,'n':trap_n,'quotient_numerator':trap_numerator,'quotient_denominator':trap_denominator,'polynomial_sum':trap_polynomial_sum,'detail':'at x=1,n=3 the rational presentation is 0/0 while the polynomial sum evaluates to 3'}}
    if cid=='C22':
        # Finite difference of a polynomial represented low-to-high.
        def shift(p):
            q=[F(0)]*len(p)
            for i,a in enumerate(p):
                for j in range(i+1):q[j]+=a*comb(i,j)
            return q
        def delta(p):
            q=shift(p);q += [F(0)]*(len(p)-len(q));return [q[i]-p[i] for i in range(len(p))]
        target=[F(1),F(4),F(6),F(4),F(0)]
        true=delta([F(0),F(0),F(0),F(0),F(1)])
        integrated=[F(0),F(1),F(2),F(2),F(1)]
        bad=delta(integrated)
        return {'certificate_passed':true==target,'certificate':'computed binomial finite difference of x^4','trap_check':{'kind':'counterexample','passed':bad!=target,'detail':'finite difference of the termwise antiderivative does not equal the target cubic'}}
    if cid=='C23':
        ok=all(sum((F((-1)**k*comb(n,k),k+1) for k in range(n+1)),F(0))==F(1,n+1) for n in range(0,65))
        trap=sum((F((-1)**k*comb(3,k),k+1) for k in range(4)),F(0)) != 0
        return {'certificate_passed':ok,'certificate':'exact factorial/binomial instances n=0..64','trap_check':{'kind':'counterexample','passed':trap,'detail':'at n=3 the weighted alternating sum is 1/4, not zero'}}
    if cid=='C24':
        # pair (alpha,beta) represents alpha*t+beta modulo t^2-3t+2.
        a,b=0,1
        for _ in range(17): a,b=3*a+b,-2*a
        inverse_ok=(F(-1,2)*3+F(3,2),F(-1,2)*-2)==(F(0),F(1))
        ok=(a,b)==(131071,-131070) and inverse_ok
        trap=(131072*1)!=(131071*1-131070) # A=I satisfies the premise.
        return {'certificate_passed':ok,'certificate':'quotient-ring multiplication and inverse coefficients','trap_check':{'kind':'counterexample','passed':trap,'detail':'A=I refutes the omitted-intercept formula 2^17 A'}}
    raise KeyError(cid)
