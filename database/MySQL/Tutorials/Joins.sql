/* Title: Joins in MySQL

Joins
Joins are a fundamental concept for working with relational databases. They act as the bridge between tables, allowing you to combine data from multiple tables based on defined relationships. There are different types of joins, such as INNER, FULL, RIGHT, and LEFT.

Here, 

-> The LEFT JOIN includes all rows from the left table and matching rows from the right table. The result set 
    will contain NULL for the rows that don’t have a matching row on the right side. 
-> Conversely, RIGHT JOIN consists of all records from the right table rows and 
    matching rows from the left while leaving unmatched entries from the left side as NULL.
-> ‍INNER JOIN is the default join, which only returns the rows where the join 
    condition is met in both tables. 
-> The FULL JOIN combines left and right join results, including all rows from both tables,    
    even if there’s no match in the other table. 
*/