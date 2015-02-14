# define cluster IPs and ports
# single node configuration can just supply the loopback address
@Server:
127.0.0.1:10010

# Table definition for movie view logs.
@Table:viewlog
i,tkey:time
s,hash:userid
s:moviename
f:viewfraction

# Vector: user summary
@Vector:userstat
s,hash:userid
i,+add:viewtime
s,+last:moviename

# global running tally
@Var:
i,+add:totalserved
