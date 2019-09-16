--CREATE MATERIALIZED VIEW PopData AS
  SELECT citypops.country, citypops.year, city.name, citypops.population,
         city.longitude, city.latitude, city.elevation,
         economy.agriculture, economy.service, economy.industry, economy.inflation
  FROM citypops, city, economy
  WHERE city.name = citypops.city;