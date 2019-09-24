-- psql -f mondial-schema.psql
-- psql -f mondial-inputs.psql
-- Part I
SELECT name FROM city WHERE population > 13000000;                        -- projecting the relation city onto the attribute name, and a selection of tuples under the condition of the attribute population being larger than 13M.
SELECT code FROM country WHERE name = 'Sweden';
SELECT name FROM city WHERE country = 'S' AND population > 500000;        --(and works instead of AND)
SELECT name, population, elevation FROM city WHERE elevation < 0;
SELECT SUM(population) FROM city WHERE elevation < 0;   			            --(p.278)
SELECT name FROM city WHERE name LIKE 'Los%' OR name LIKE '%burgh'; 		  --(p.244-45)
SELECT name, population FROM country ORDER BY population DESC LIMIT 5;	  --(p.250)

-- Part II
SELECT country.name, city.name, elevation FROM country, city WHERE city.country = country.code ORDER BY elevation desc nulls last LIMIT 5;
-- SELECT country.name, city.name, elevation FROM country, city WHERE city.country = country.code AND elevation IS NOT NULL ORDER BY elevation DESC LIMIT 5;
(SELECT name FROM city WHERE name LIKE '%q') UNION (SELECT name FROM country WHERE name LIKE 'Z%');

-- Q: how do we execute the sql file?
-- A: in postgres, \i name_of_file.sql


-- GENERAL NOTE:
-- The operations of the traditional relational algebra fall into four broad classes:
-- a) The usual set operations — union, intersection, and difference — applied to relations.
-- b) Operations that remove parts of a relation: “selection” eliminates some rows (tuples), and “projection” eliminates some columns.
-- c) Operations that combine the tuples of two relations, including “Cartesian product,” which pairs the tuples of two relations in all possible ways, and various kinds of “join” operations, which selectively pair tuples from two relations.
-- d) An operation called “renaming” that does not affect the tuples of a re­ lation, but changes the relation schema, i.e., the names of the attributes and/or the name of the relation itself.
-- We generally shall refer to expressions of relational algebra as queries.
