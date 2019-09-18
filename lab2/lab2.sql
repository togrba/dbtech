-- Q1A

-- DROP MATERIALIZED VIEW PopData;
CREATE MATERIALIZED VIEW PopData AS
  SELECT
  citypops.year, citypops.city, citypops.population, citypops.country,
  city.longitude, city.latitude, city.elevation,
  economy.agriculture, economy.service, economy.industry, economy.inflation
  FROM citypops
  JOIN city ON citypops.city = city.name AND citypops.country = city.country
  JOIN economy ON citypops.country = economy.country;

SELECT * FROM PopData WHERE city LIKE 'Santiago%';


-- Q1B

-- We choose materialized view instead of virtual view because we want to work
-- with a stored table.


-- Q2A
