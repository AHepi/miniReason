# Working answer

Let DeltaP(x)=P(x+1)-P(x). This finite difference is not differentiation: Delta uses the exact change over step 1, while P'(x) is a limit of divided differences as the step tends to 0. Expanding gives (x+1)^4-x^4=4x^3+6x^2+4x+1, so P0(x)=x^4 satisfies the finite-difference equation and P0(0)=0. If Q is another rational polynomial solution with Q(0)=0, then D=Q-P0 has D(0)=0 and D(x+1)-D(x)=0 for every rational x. A nonconstant rational polynomial cannot have period 1: if D has degree n>=1 and leading coefficient a_n, then D(x+1)-D(x) has degree n-1 and leading coefficient n a_n, which is nonzero. Hence D is constant, and D(0)=0 forces D=0. Therefore P(x)=x^4 is the unique rational polynomial satisfying P(0)=0 and the finite-difference equation.

Stop reason: `complete`.
