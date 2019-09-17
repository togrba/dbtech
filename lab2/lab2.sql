--DROP MATERIALIZED VIEW PopData;
CREATE MATERIALIZED VIEW PopData AS
  SELECT city, country, year, population
  FROM citypops
  JOIN city ON citypops.city = city.name;

  -- SELECT longitude, latitude, elevation
  -- FROM city
  -- UNION ALL
  -- SELECT agriculture, service, industry, inflation
  -- FROM economy;

SELECT * FROM PopData WHERE city LIKE 'Santiago%';


-- run: \i lab2.sql
