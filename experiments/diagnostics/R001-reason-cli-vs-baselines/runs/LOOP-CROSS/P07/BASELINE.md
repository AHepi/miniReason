# Baseline readings

Same problem and conjecturer; one logical call per mode, with recorded attempts. No computed comparison.

## bare

Outcome: `COMPLETE`.

Thinking: off; completion ceiling: 8192; declared reasoning effort: medium.

Work modulo 19, with residues 0,...,18.

1) Is f(x)=x^3+8x one-to-one on {0,...,18}? No.

A quick way to see this is to factor the difference. For inputs a,b,

f(a)-f(b) = (a^3-b^3)+8(a-b)
= (a-b)(a^2+ab+b^2+8),

with all arithmetic modulo 19. Thus f(a)=f(b) exactly when a=b or
a^2+ab+b^2+8 ≡ 0 (mod 19). A counterexample is enough:

f(1)=1^3+8·1=9 mod 19.
f(7)=7^3+8·7 = 343+56 = 399. Since 19·21=399, f(7) ≡ 0 mod 19? Wait, that gives 0, not 9. Let me recompute directly: 7^3=343, 343 mod 19: 19·18=342, so 343≡1. 8·7=56, 56 mod 19: 19·2=38, 56-38=18≡-1. So f(7)=1+18=19≡0. So 1 is not a collision with 7.

A valid collision: check x=2 and x=17? Use the factorization. Need a^2+ab+b^2+8≡0.
Try a=1, solve b^2+b+9≡0 mod 19. Discriminant 1-36=-35≡3 mod 19. Is 3 a square mod 19? Squares mod 19 are 0,1,4,9,16,6,17,11,7,5 (for 0 through 9), and then symmetric. 3 is not there, so no b for a=1.
Try a=2: b^2+2b+12≡0, discriminant 4-48=-44≡? -44+57=13 mod 19. Squares list has no 13? List: 0,1,4,9,16,6,17,11,7,5. 13 no.
a=3: b^2+3b+17≡0, disc 9-68=-59≡? +76=17. 17 is square (7^2=49≡11? wait 7^2=49, 49-38=11; 8^2=64, 64-57=7; let me list properly: 0^2=0,1^2=1,2^2=4,3^2=9,4^2=16,5^2=25≡6,6^2=36≡17,7^2=49≡11,8^2=64≡7,9^2=81≡5. Yes 17 is square.) So b ≡ (-3 ± 6)/2. Now 2 inverse mod 19 is 10. -3+6=3, 3·10=30≡11; -3-6=-9≡10, 10·10=100≡5. So b=11 or 5. Check f(3)=27+24=51≡51-38=13. f(11)=1331+88=1419. 19·74=1406, rem 13. Yes! f(3)=f(11)=13. So not one-to-one.

Also list inputs mapping to 13: solve x^3+8x≡13. We found x=3 and x=11. Cubic can have up to 3 roots mod prime. Factor using root 3: divide x^3+8x-13 by x-3 over mod 19. Synthetic gives x^2+3x+17 (since 3·3=9, 8+9=17; 17+3·3=26≡7? need exact). Direct: (x-3)(x^2+3x+17)=x^3+3x^2+17x-3x^2-9x-51=x^3+8x-51≡x^3+8x-51+57=x^3+8x+6. Not right because constant target: x^3+8x-13; constant -13≡6. Yes -51≡-51+57=6≡-13. Correct. So quotient x^2+3x+17. Its roots: discriminant 9-68=-59≡-59+76=17; sqrt 17 is ±6 (since 6^2=36≡17). Roots (-3±6)/2 = 3/2=3·10=30≡11 and -9/2=10·10=100≡5. Check f(5)=125+40=165, 165-152=13. So roots are 3,11,5. Thus inputs giving 13 are x=3,5,11.

Never-output residues: image of f. Compute values f(0)=0. f(1)=9. f(2)=8+16=24≡5. f(3)=13. f(4)=64+32=96≡96-95=1. f(5)=13. f(6)=216+48=264, 264-247=17. f(7)=0. f(8)=512+64=576, 19·30=570 rem6. f(9)=729+72=801, 19·42=798 rem3. f(10)=1000+80=1080, 19·56=1064 rem16. f(11)=13. f(12)=1728+96=1824, 19·96=1824 rem0. f(13)=2197+104=2301, 19·121=2299 rem2. f(14)=2744+112=2856, 19·150=2850 rem6. f(15)=3375+120=3495, 19·183=3477 rem18. f(16)=4096+128=4224, 19·222=4218 rem6. f(17)=4913? 17^3=4913, +136=5049, 19·265=5035 rem14. f(18)=5832+144=5976, 19·314=5966 rem10.
Image set: {0,1,2,3,5,6,9,10,13,14,16,17,18}. Missing from 0..18: {4,7,8,11,12,15}.

2) d(x)=3x^2+8 nonzero at every allowed x? No. d(x)=0 when 3x^2≡-8≡11 mod 19. Inverse of 3 mod 19 is 13 since 3·13=39≡1. So x^2≡11·13=143≡143-133=10 mod 19. Squares mod 19 are {0,1,4,5,6,7,9,11,16,17}. 10 is not a square mod 19. Therefore d(x) is nonzero for every x in {0,...,18}. Explicit check: d(0)=8, d(1)=11, d(2)=20≡1, etc., none zero.

So final facts: f is not one-to-one; d(x) is nonzero everywhere on the allowed set; preimages of 13 are {3,5,11}; never-output residues are {4,7,8,11,12,15}.

Assumption: residues chosen in {0,...,18}, all arithmetic mod 19.

## native

Outcome: `COMPLETE`.

Thinking: native; completion ceiling: 32768; declared reasoning effort: medium.

Assumption: x is in F_19 represented by {0,1,...,18}. (1) f is not one-to-one: f(3)=3^3+8*3=27+24=51≡13 (mod19), while f(5)=5^3+8*5=125+40=165, and 19*8=152, so 165≡13 (mod19). Distinct inputs 3 and 5 give the same output 13. Thus f is not one-to-one on {0,...,18}. (2) d(x)=3x^2+8 is nonzero for every allowed x. If d(x)=0, then 3x^2≡-8≡11 (mod19). Since 3^{-1}=13 (mod19), this gives x^2≡13*11=143≡10 (mod19). The quadratic residues modulo 19 are {0,1,4,5,6,7,9,11,16,17}; 10 is not among them. Hence x^2≡10 has no solution, so d(x)≠0 for all x in {0,...,18}. (3) The full value table is x: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; f(x): 0 9 5 13 1 13 17 0 6 3 16 13 0 2 6 18 6 14 10. Therefore the input residues mapping to 13 are exactly {3,5,11}; exhaustiveness also follows because f(x)-13 is a cubic over F_19 and has at most 3 roots. The outputs actually attained are {0,1,2,3,5,6,9,10,13,14,16,17,18}. Hence the residues the device can never output are {4,7,8,11,12,15}. Uncertainty: none; the modular arithmetic and table above determine these facts. Note that d(x) being nonzero everywhere does not force f to be one-to-one here, as the explicit collision shows.

