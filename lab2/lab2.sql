--DROP MATERIALIZED VIEW PopData;
CREATE MATERIALIZED VIEW PopData AS
  -- SELECT
  -- citypops.year, citypops.city, citypops.population, citypops.country,
  -- city.longitude, city.latitude, city.elevation,
  -- economy.agriculture, economy.service, economy.industry, economy.inflation
  -- FROM citypops
  -- JOIN city ON citypops.city = city.name
  -- JOIN economy ON citypops.country = economy.country;


  SELECT
  year, city, cp.population, cp.country,
  longitude, latitude, elevation,
  agriculture, service, industry, inflation
  FROM citypops cp, city c, economy e
  WHERE cp.city = c.name AND c.country = e.country;


-- city attributes doubles


 SELECT * FROM PopData WHERE city LIKE 'Santiago%';


-- run: \i lab2.sql
