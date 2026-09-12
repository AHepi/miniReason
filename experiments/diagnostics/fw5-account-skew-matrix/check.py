"""Exact polynomial check; arithmetic evidence, no semantic verdict."""
from collections import defaultdict
from itertools import permutations
import json


def sign(p):
    return (-1) ** sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1,len(p)))


def skew_polynomial(n):
    coefficients=defaultdict(int)
    surviving=0
    positive=negative=0
    for p in permutations(range(n)):
        if any(i==j for i,j in enumerate(p)):
            continue
        surviving+=1
        c=sign(p)
        monomial=[]
        for i,j in enumerate(p):
            c*=1 if i<j else -1
            monomial.append((min(i,j),max(i,j)))
        coefficients[tuple(sorted(monomial))]+=c
        positive+=c>0
        negative+=c<0
    nonzero={str(k):v for k,v in coefficients.items() if v}
    return {"n":n,"permutations":__import__('math').factorial(n),"nonzero_before_collection":surviving,"positive_terms":positive,"negative_terms":negative,"collected_monomials":len(coefficients),"remaining_coefficients":nonzero}


def determinant(a):
    n=len(a)
    return sum(sign(p)*__import__('math').prod(a[i][p[i]] for i in range(n)) for p in permutations(range(n)))


def inverse_permutation(p):
    q=[0]*len(p)
    for i,j in enumerate(p): q[j]=i
    return tuple(q)

checks=[]
for n in (3,5):
    result=skew_polynomial(n)
    assert result['remaining_coefficients']=={}
    ps=[p for p in permutations(range(n)) if all(i!=j for i,j in enumerate(p))]
    assert all(inverse_permutation(p)!=p for p in ps)
    result['distinct_inverse_pairs']=len(ps)//2
    checks.append(result)

identity3=[[1,0,0],[0,1,0],[0,0,1]]
even_skew=[[0,1],[-1,0]]
assert determinant(identity3)==1
assert determinant(even_skew)==1
sample3=[[0,2,3],[-2,0,5],[-3,-5,0]]
assert determinant(sample3)==0
result={"scope":"Exact symbolic cancellation for arbitrary real entries at n=3 and n=5; direct integer contrast witnesses. General odd-n proof remains a separate argument.","symbolic_checks":checks,"contrasts":{"remove_skewness_odd_identity3_det":determinant(identity3),"remove_odd_dimension_even_skew_det":determinant(even_skew)},"compatible_baseline":{"matrix":sample3,"determinant":determinant(sample3)},"semantic_verdict":"Not computed; all-five-pass and absence of bearing require independent interpretation."}
print(json.dumps(result,indent=2))
