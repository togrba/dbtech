-- Part I
SELECT name FROM city WHERE population > 13000000;
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
