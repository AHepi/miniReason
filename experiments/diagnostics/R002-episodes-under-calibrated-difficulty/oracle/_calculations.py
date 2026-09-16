from fractions import Fraction as F
from itertools import combinations, permutations, product
from functools import lru_cache
import heapq, json, math

out = {}

# C01: observed ordered colours B,R,B; then one further draw.
modes = {'A': (F(2,7),2,4), 'B': (F(3,7),4,3), 'C': (F(2,7),5,3)}
w = {}
for k,(pr,r,b) in modes.items():
    n=r+b; w[k]=pr*F(b,n)*F(r,n-1)*F(b-1,n-2)
z=sum(w.values()); post={k:v/z for k,v in w.items()}
next_r=sum(post[k]*F(r-1,r+b-3) for k,(_,r,b) in modes.items())
wb={k:pr*F(b,r+b)*F(r,r+b)*F(b,r+b) for k,(pr,r,b) in modes.items()}; zb=sum(wb.values())
out['C01']={'posterior_C':str(post['C']),'next_red':str(next_r),'weights':{k:str(v) for k,v in w.items()},'with_replacement_trap':{'posterior_C':str(wb['C']/zb),'next_red':str(sum(wb[k]/zb*F(r,r+b) for k,(_,r,b) in modes.items()))}}

# C02: balanced proper bracelets.
words=[]
for apos in combinations(range(14),5):
  arem=set(apos)
  for bpos in combinations([i for i in range(14) if i not in arem],5):
    s=['C']*14
    for i in apos:s[i]='A'
    for i in bpos:s[i]='B'
    if all(s[i]!=s[(i+1)%14] for i in range(14)): words.append(''.join(s))
def rots(s): return [s[i:]+s[:i] for i in range(len(s))]
rot_reps={min(rots(s)) for s in words}
dih_reps={min(rots(s)+rots(s[::-1])) for s in words}
out['C02']={'linear_valid':len(words),'rotation_classes':len(rot_reps),'bracelets':len(dih_reps),'reflection_fixed_rotation_classes':2*len(dih_reps)-len(rot_reps),'half_rotation_trap':F(len(rot_reps),2).__str__()}

# C03: synchronous register machine and sequential-update trap.
seq='ABACBCABBACACBBACABC'
def step(v,ch,sequential=False):
  x,y,z=v
  if not sequential:
    if ch=='A': return ((x+y)%17,(y+z)%17,(z+x)%17)
    if ch=='B': return ((2*x+z)%17,(x+3*y)%17,(y+2*z)%17)
    return ((x+2*y+1)%17,(2*x+z)%17,(y+z+3)%17)
  if ch=='A': x=(x+y)%17; y=(y+z)%17; z=(z+x)%17
  elif ch=='B': x=(2*x+z)%17; y=(x+3*y)%17; z=(y+2*z)%17
  else: x=(x+2*y+1)%17; y=(2*x+z)%17; z=(y+z+3)%17
  return x,y,z
def run3(sequential=False):
 v=(4,7,9); chk=0
 for i,ch in enumerate(seq,1):
  v=step(v,ch,sequential); chk=(chk+i*(100*v[0]+10*v[1]+v[2]))%1009
 return v,chk
out['C03']={'answer':run3(False),'sequential_trap':run3(True)}
_v=(4,7,9);_trace=[]
for _i,_ch in enumerate(seq,1):
 _v=step(_v,_ch,False);_trace.append((_i,_ch,*_v))
out['C03']['trace']=_trace

# C04 expected relational result and WHERE-trap result.
customers=[(1,'Blue'),(2,'Blue'),(3,'Gold'),(4,'Gold'),(5,'Silver')]
orders=[(101,1,10,'ok'),(102,1,6,'void'),(103,2,7,'ok'),(104,2,None,'ok'),(105,3,4,'void'),(106,4,9,'ok'),(107,4,3,'ok')]
def groups(on_filter=True):
 rows=[]
 for cid,tier in customers:
  ms=[o for o in orders if o[1]==cid and (o[3]=='ok' if on_filter else True)]
  if not ms: rows.append((tier,cid,None,None,None))
  else:
   for oid,_,amt,status in ms:
    if on_filter or status=='ok': rows.append((tier,cid,oid,amt,status))
 by={}
 for row in rows: by.setdefault(row[0],[]).append(row)
 ans=[]
 for tier,rs in by.items():
  if len(rs)>=2: ans.append((tier,len({r[1] for r in rs}),sum(r[2] is not None for r in rs),sum((r[3] or 0) for r in rs),len(rs)))
 return sorted(ans,key=lambda x:(-x[3],x[0]))
out['C04']={'answer':groups(True),'where_trap':groups(False)}

# C05 scheduling with release times and sequence-dependent setup.
jobs={'A':(0,4,2),'B':(0,3,5),'C':(2,5,3),'D':(4,2,8),'E':(7,1,12),'F':(1,4,4),'G':(9,2,9),'H':(3,3,6)}
def sched(order):
 t=0; prev=None; total=0; detail=[]
 for j in order:
  r,p,wj=jobs[j]; setup=(ord(j)-64)%3 if prev is None else abs(ord(j)-ord(prev))%3
  start=max(t,r)+setup; t=start+p; total+=wj*t; detail.append((j,start,t)) ; prev=j
 return total,detail
vals=sorted((sched(p)[0],''.join(p),sched(p)[1]) for p in permutations(jobs))
best=vals[0]
# deterministic ready-WSPT trap: never idle; among ready minimize (p+setup)/w.
rem=set(jobs); t=0; prev=None; greedy=[]
while rem:
 ready=[j for j in rem if jobs[j][0]<=t]
 if not ready: t=min(jobs[j][0] for j in rem); ready=[j for j in rem if jobs[j][0]<=t]
 j=min(ready,key=lambda q:((jobs[q][1]+((ord(q)-64)%3 if prev is None else abs(ord(q)-ord(prev))%3))/jobs[q][2],q))
 setup=(ord(j)-64)%3 if prev is None else abs(ord(j)-ord(prev))%3
 t=max(t,jobs[j][0])+setup+jobs[j][1]; greedy.append(j); rem.remove(j); prev=j
out['C05']={'minimum':best[0],'order':best[1],'timeline':best[2],'second_cost':next(v[0] for v in vals if v[0]>best[0]),'greedy_trap':{'order':''.join(greedy),'cost':sched(greedy)[0]}}

# C06 constrained monotone paths.
obs={(2,2),(4,3),(5,6),(7,5),(8,8)}; P=(3,4); Q=(6,7)
valid=[]
for rs in combinations(range(18),9):
 s=set(rs); x=y=0; path=''; seen=[]; ok=True
 for i in range(18):
  if i in s:x+=1;path+='R'
  else:y+=1;path+='D'
  if (x,y) in obs or path.endswith('RRR') or path.endswith('DDD'):ok=False;break
  if (x,y)==P:seen.append('P')
  if (x,y)==Q:seen.append('Q')
 if ok: valid.append((path,tuple(seen)))
exact=[p for p,s in valid if len(set(s))==1]
atleast=[p for p,s in valid if len(set(s))>=1]
out['C06']={'count':len(exact),'lex_D_before_R':min(exact,key=lambda p:p.translate(str.maketrans('DR','01'))),'at_least_one_trap':len(atleast)}

# C07 exact absorbing-chain equations.
trans=[[(1,F(1,2)),(2,F(1,3)),(-1,F(1,6))],[(0,F(1,4)),(3,F(1,2)),(-1,F(1,4))],[(1,F(1,3)),(4,F(1,2)),(-1,F(1,6))],[(2,F(1,4)),(4,F(1,4)),(-1,F(1,2))],[(0,F(1,5)),(3,F(2,5)),(-1,F(2,5))]]
A=[]
for i,row in enumerate(trans):
 a=[F(int(i==j)) for j in range(5)]
 for j,p in row:
  if j>=0:a[j]-=p
 A.append(a+[F(1)])
for c in range(5):
 piv=next(r for r in range(c,5) if A[r][c]); A[c],A[piv]=A[piv],A[c]
 q=A[c][c]; A[c]=[v/q for v in A[c]]
 for r in range(5):
  if r!=c:
   q=A[r][c]; A[r]=[A[r][k]-q*A[c][k] for k in range(6)]
E=[A[i][5] for i in range(5)]
dist={0:F(1)}; absorb=F(0)
for _ in range(5):
 nd={}
 for i,pr in dist.items():
  for j,p in trans[i]:
   if j<0:absorb+=pr*p
   else:nd[j]=nd.get(j,F(0))+pr*p
 dist=nd
out['C07']={'expected_steps':str(E[0]),'absorb_by_5':str(absorb),'geometric_trap':'6'}

# C08 spanning trees and edge inclusion.
edges=[(0,1),(0,2),(0,3),(1,2),(1,4),(2,3),(2,4),(2,5),(3,5),(3,6),(4,5),(4,7),(5,6),(5,7),(6,7)]
def tree(es):
 p=list(range(8))
 def f(x):
  while p[x]!=x:p[x]=p[p[x]];x=p[x]
  return x
 for a,b in es:
  a=f(a);b=f(b)
  if a==b:return False
  p[a]=b
 return len({f(i) for i in range(8)})==1
trees=[es for es in combinations(edges,7) if tree(es)]
out['C08']={'trees':len(trees),'containing_01':sum((0,1) in es for es in trees),'independence_trap':str(F(len(trees)*7,len(edges)))}

# C09 transducer probability, synchronous and sequential trap.
def transducer(seq, bad=False):
 s,t=1,0
 for bit in seq:
  if bit==0:
   s=(s+t)%4; t=(t+1)%3
  else:
   old=s; s=(2*s+t+1)%4; t=((s if bad else old)+t)%3
 return s,t
num=0; badnum=0
for bits in product((0,1),repeat=12):
 if sum(bits)!=7:continue
 wt=2**5*3**7
 if transducer(bits)==(2,1):num+=wt
 if transducer(bits,True)==(2,1):badnum+=wt
den=5**12
out['C09']={'probability':str(F(num,den)),'matching_words':num//(2**5*3**7),'sequential_trap':str(F(badnum,den))}

# C10 affine observations modulo 2520.
def f10(x):return (17*x+23)%2520
good=[]
bad10=[]
for x in range(2520):
 y=x
 vals=[]
 for _ in range(5):y=f10(y);vals.append(y)
 if vals[2]%8==5 and vals[3]%9==4 and vals[4]%5==2 and x%7==1:good.append(x)
 # Faulty closed form omits the geometric offset: f^k(x)=17^k*x+23.
 vals_bad=[(pow(17,k,2520)*x+23)%2520 for k in range(1,6)]
 if vals_bad[2]%8==5 and vals_bad[3]%9==4 and vals_bad[4]%5==2 and x%7==1:bad10.append(x)
out['C10']={'count':len(good),'least':min(good) if good else None,'sum_mod_2520':sum(good)%2520,'solutions':good[:20],'omitted_offset_trap':{'count':len(bad10),'least':min(bad10) if bad10 else None,'sum':sum(bad10)%2520}}

# C11 topological slot assignment.
tasks='ABCDEFGH'
pred={ 'A':set(),'B':{'F'},'C':{'A'},'D':{'A'},'E':{'B','C'},'F':set(),'G':{'D','F'},'H':{'E','G'} }
cost=[[7,2,9,8,11,13,14,16],[4,8,3,9,7,12,13,15],[9,6,5,2,8,9,12,14],[8,9,4,7,3,10,11,13],[12,10,8,6,4,2,7,9],[11,7,9,5,8,4,3,6],[14,12,10,8,6,7,2,4],[15,13,11,10,9,8,6,1]]
feas=[]
for p in permutations(tasks):
 pos={t:i for i,t in enumerate(p)}
 if all(all(pos[q]<pos[t] for q in pred[t]) for t in tasks):
  v=sum(cost[ord(t)-65][i] for i,t in enumerate(p));feas.append((v,''.join(p)))
feas.sort()
out['C11']={'minimum':feas[0][0],'order':feas[0][1],'second_cost':next(v for v,p in feas if v>feas[0][0]),'unconstrained_trap':min((sum(cost[ord(t)-65][i] for i,t in enumerate(p)),''.join(p)) for p in permutations(tasks))}

# C12 adaptive urn.
dist={(3,2,1):F(1)}; sixth_red=F(0)
for turn in range(1,7):
 nd={}
 for (r,b,g),pr in dist.items():
  n=r+b+g
  if r:
   st=(r,b+1,g); q=pr*F(r,n); nd[st]=nd.get(st,F(0))+q
   if turn==6:sixth_red+=q
  if b:
   st=(r,b-1,g+1); q=pr*F(b,n); nd[st]=nd.get(st,F(0))+q
  if g:
   st=(r+1,b,g); q=pr*F(g,n); nd[st]=nd.get(st,F(0))+q
 dist=nd
target=max(dist.items(),key=lambda x:x[1])[0]
out['C12']={'most_likely_state':target,'probability':str(dist[target]),'sixth_red':str(sixth_red),'states':len(dist),'fixed_composition_trap':'1/2'}

# C13 cyclic word count by memoized DP and linear-only trap.
@lru_cache(None)
def count13(a,b,c,last,prefix,suffix,cyclic):
 if a+b+c==0:
  if not cyclic:return 1
  ring=suffix+prefix
  return int(last!=prefix[0] and 'ABCA' not in ring)
 total=0
 for ch,n in zip('ABC',(a,b,c)):
  if n and ch!=last and not (suffix+ch).endswith('ABCA'):
   ns=(suffix+ch)[-3:]
   total+=count13(a-(ch=='A'),b-(ch=='B'),c-(ch=='C'),ch,(prefix+ch)[:3],ns,cyclic)
 return total
cyc=count13(6,5,5,'','','',True); count13.cache_clear(); linear=count13(6,5,5,'','','',False)
out['C13']={'cyclic_count':cyc,'linear_trap':linear}

# C14 floored recurrence.
def prime(n):return n>=2 and all(n%d for d in range(2,int(n**.5)+1))
def run14(one_prime=False):
 x=37; chk=0
 for n in range(20):
  isp=prime(n) or (one_prime and n==1)
  x=(7*x+11)//5 if isp else (4*x+9)//3
  chk=(chk+(n+1)*x)%1000003
 return x,chk
out['C14']={'answer':run14(),'one_is_prime_trap':run14(True)}
_x=37;_trace14=[]
for _n in range(20):
 _x=(7*_x+11)//5 if prime(_n) else (4*_x+9)//3;_trace14.append((_n,_x))
out['C14']['trace']=_trace14

# C15 time-dependent shortest route with optional one-minute waits.
graph={'S':[('A',1,0),('B',3,0)],'A':[('T',2,6),('C',3,2)],'B':[('A',2,1),('C',4,0),('D',2,4)],'C':[('T',4,0),('D',1,2)],'D':[('C',1,0),('T',3,3)],'T':[]}
def route_key(path):
 toks=path.split('-'); order={'wait':'0','S':'1S','A':'1A','B':'1B','C':'1C','D':'1D','T':'1T'}
 return tuple(order[t] for t in toks)
def dijkstra(parity=True):
 pq=[(0,route_key('S'),'S','S')]; seen={}
 while pq:
  t,_,u,path=heapq.heappop(pq); key=(u,t%2) if parity else u
  if key in seen:continue
  seen[key]=(t,path)
  if u=='T':return t,path
  if parity:
   np=path+'-wait';heapq.heappush(pq,(t+1,route_key(np),u,np))
  for v,base,pen in graph[u]:
   np=path+'-'+v;heapq.heappush(pq,(t+base+(t%2)*pen,route_key(np),v,np))
out['C15']={'answer':dijkstra(True),'vertex_only_trap':dijkstra(False)}

# C16 poison-move minimax. Landing on total 4 loses immediately; no move also loses.
moves=[(1,0),(2,0),(0,1),(0,2),(1,1)]
@lru_cache(None)
def game(a,b):
 opts=[]
 for da,db in moves:
  if da<=a and db<=b:
   na,nb=a-da,b-db
   if na+nb==4: child=(True,0) # child wins immediately because mover lost
   else: child=game(na,nb)
   opts.append(((da,db),child))
 if not opts:return (False,0)
 wins=[(m,1+r) for m,(cw,r) in opts if not cw]
 if wins:return (True,min(r for _,r in wins))
 return (False,1+max(r for _,(_,r) in opts))
g=game(9,11); best=[m for m in moves if m[0]<=9 and m[1]<=11 and (lambda c:not c[0] and 1+c[1]==g[1])(game(9-m[0],11-m[1]))]
@lru_cache(None)
def game_bad(a,b):
 opts=[]
 for da,db in moves:
  if da<=a and db<=b:
   na,nb=a-da,b-db
   child=(False,0) if na+nb==4 else game_bad(na,nb) # faulty: landing on four wins
   opts.append(child)
 if not opts:return (False,0)
 wins=[1+r for w,r in opts if not w]
 return (True,min(wins)) if wins else (False,1+max(r for _,r in opts))
gb=game_bad(9,11);bestbad=[]
for m in moves:
 if m[0]<=9 and m[1]<=11:
  na,nb=9-m[0],11-m[1];c=(False,0) if na+nb==4 else game_bad(na,nb)
  if not c[0] and 1+c[1]==gb[1]:bestbad.append(m)
out['C16']={'winning':g[0],'remoteness':g[1],'optimal_moves':best,'four_is_winning_trap':{'outcome':gb,'optimal_moves':bestbad}}

# C17 exact interpolation from the ten public ordinates.
vals=[11,8,417,17774,247103,1879476,9809573,39556682,132174099,382736288]
def interpolate(vs):
 row=vs[:];heads=[]
 while row:
  heads.append(row[0]);row=[row[i+1]-row[i] for i in range(len(row)-1)]
 poly=[0];basis=[1]
 for k,h in enumerate(heads):
  h=F(h,math.factorial(k))
  if len(poly)<len(basis):poly += [0]*(len(basis)-len(poly))
  for i,c in enumerate(basis):poly[i]+=h*c
  nb=[0]*(len(basis)+1)
  for i,c in enumerate(basis):nb[i]-=k*c;nb[i+1]+=c
  basis=nb
 return [int(c) if getattr(c,'denominator',1)==1 else c for c in poly]
coef=interpolate(vals)
polyval=lambda x:sum(c*x**i for i,c in enumerate(coef))
badcoef=interpolate(vals[:9])
bad9=sum(c*9**i for i,c in enumerate(badcoef))
out['C17']={'values':vals,'coefficients':coef,'p20':polyval(20),'x7_coefficient':coef[7],'degree8_trap_predicted_p9':bad9}

# C18 preemptive priority queue, boundary order completion then arrivals then dispatch.
arr=[('A',0,4,3),('B',1,3,2),('C',3,2,1),('D',4,1,1),('E',5,4,2),('F',7,2,1),('G',8,3,3)]
def sim18(arrivals_first=False):
 rem={j:w for j,t,w,p in arr}; meta={j:(t,p) for j,t,w,p in arr}; ready=[]; current=None;t=0;done=[]
 while len(done)<len(arr):
  arriving=[j for j,at,w,p in arr if at==t]
  # Correct contract credits the previous interval before new arrivals can preempt.
  # The trap incorrectly admits arrivals first and selects the worker that receives
  # that already elapsed interval's unit.
  if arrivals_first:
   ready.extend(arriving)
   if current is not None:ready.append(current)
   if ready:
    ready=list(dict.fromkeys(ready)); current=min(ready,key=lambda j:(meta[j][1],meta[j][0],j));ready.remove(current)
   if t>0 and current is not None:rem[current]-=1
  elif t>0 and current is not None:
   rem[current]-=1
  if current is not None and rem[current]==0:
   done.append((current,t));current=None
  if not arrivals_first:
   ready.extend(arriving)
   if current is not None:ready.append(current)
   if ready:
    ready=list(dict.fromkeys(ready)); current=min(ready,key=lambda j:(meta[j][1],meta[j][0],j));ready.remove(current)
  t+=1
 return done,sum(t-meta[j][0] for j,t in done)
out['C18']={'answer':sim18(False),'arrival_first_trap':sim18(True)}

if __name__ == '__main__': print(json.dumps(out,indent=2,default=str))
