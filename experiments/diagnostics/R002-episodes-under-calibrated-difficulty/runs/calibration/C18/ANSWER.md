# Working answer

Derivation:
1. At t=0, admit A and dispatch A. A runs from [0,1), leaving 3 work.
2. At t=1, A has 3 left; admit B. B has priority 2 vs A priority 3, so B preempts A and runs [1,2), leaving 2.
3. At t=2, B has 2 left and continues [2,3), leaving 1.
4. At t=3, B has 1 left; admit C. C priority 1 is best, so C preempts B and runs [3,4), leaving 1.
5. At t=4, C has 1 left; admit D. C and D both priority 1, but C arrived earlier, so C continues [4,5) and completes at t=5.
6. At t=5, after C completes, admit E. Available D priority 1 beats B/E priority 2 and A priority 3, so D runs [5,6) and completes at t=6.
7. At t=6, B priority 2 beats E priority 2 by earlier arrival and A priority 3, so B runs [6,7) and completes at t=7.
8. At t=7, after B completes, admit F. F priority 1 runs [7,8) and [8,9), completing at t=9.
9. At t=8, F continues because priority 1 beats E priority 2, A priority 3, and G priority 3.
10. At t=9, after F completes, E priority 2 beats A and G priority 3, so E runs [9,10), [10,11), [11,12), [12,13), completing at t=13.
11. At t=13, A and G both priority 3; A arrived earlier, so A runs [13,14), [14,15), [15,16), completing at t=16.
12. At t=16, G runs [16,17), [17,18), [18,19), completing at t=19.
13. Turnarounds: A=16-0=16, B=7-1=6, C=5-3=2, D=6-4=2, E=13-5=8, F=9-7=2, G=19-8=11. Sum=16+6+2+2+8+2+11=47.

The completion sequence is C at 5, D at 6, B at 7, F at 9, E at 13, A at 16, and G at 19. The sum of turnaround times is 47.

Stop reason: `complete`.
