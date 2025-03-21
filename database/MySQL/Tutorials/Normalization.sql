Normal Forms in DBMS
Normal Forms

Description of Normal Forms

First Normal Form (1NF)

A relation is in first normal form if every attribute in that relation is single-valued attribute. 

Second Normal Form (2NF)

A relation that is in First Normal Form and every non-primary-key attribute is fully functionally dependent on the primary key, then the relation is in Second Normal Form (2NF).

Third Normal Form (3NF)

A relation is in the third normal form, if there is no transitive dependency for non-prime attributes as well as it is in the second normal form. A relation is in 3NF if at least one of the following conditions holds in every non-trivial function dependency X –> Y.

X is a super key.
Y is a prime attribute (each element of Y is part of some candidate key).
Boyce-Codd Normal Form (BCNF)

For BCNF the relation should satisfy the below conditions

The relation should be in the 3rd Normal Form.
X should be a super-key for every functional dependency (FD) X−>Y in a given relation. 
Fourth Normal Form (4NF)

A relation R is in 4NF if and only if the following conditions are satisfied: 

It should be in the Boyce-Codd Normal Form (BCNF).
The table should not have any Multi-valued Dependency.
Fifth Normal Form (5NF)

 A relation R is in 5NF if and only if it satisfies the following conditions:

R should be already in 4NF. 
It cannot be further non loss decomposed (join dependency).