--DROP MATERIALIZED VIEW PopData;
CREATE MATERIALIZED VIEW PopData AS
  SELECT citypops.city, citypops.country, citypops.year, citypops.population,
         city.longitude, city.latitude, city.elevation,
         economy.agriculture, economy.service, economy.industry, economy.inflation
  FROM citypops, city, economy
  WHERE city.name = citypops.city AND economy.country = city.country;

SELECT * FROM PopData WHERE city LIKE 'Santiago%';
SELECT * FROM PopData WHERE city LIKE 'Santiago%';
