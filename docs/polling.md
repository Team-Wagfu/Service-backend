# Abstract

client A, wants to notify something/call to client B, 2 things can be notified, and 1 call option.  

if the client wants to call, client A, sends a poll to the server stating 
it want to connect to this particular client, the structure should contain
who its from, who it is to, the type of poll(since all 3 kinds of poll are in the same table),
the number of polls(count of pending notifications in that category), the list or array of 
ids with which the records in teh correpsonding poll type table are identified uniquely  with.

# Tables and Persistence Architecture

## Tables
-polls
    