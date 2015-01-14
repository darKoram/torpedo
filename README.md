# torpedo
Gather info on RDBMS schema to create minimal datasets from fact and dimension tables using sqlAlchemy

Torpedo aims to solve the following problem.  You wish to test a deployment that relies on an RDBMS.
That schema may contain dozens of tables each of which could have millions of rows.  From this origination
data you may derive analytics and metrics tables which are then used by the deployment.

In this case, if you wish to test deployment, you either have to do some computations on the full tables, and if 
there are large joins this could run into hours or days; or you can exctract a small subset of data to run through
the system.

The problem with small data set extraction is that if you take 500 rows from table A and 500 rows from table B, where
A and B are millions of rows, the A join B will likely have no rows.  The problem is that matching entries on the join
columns can be in any row in different tables.  We need a smart way to extract linked data from a schema.

This is the goal of torpedo.

