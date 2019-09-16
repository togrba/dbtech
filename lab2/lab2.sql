CREATE MATERIALIZED VIEW PopData AS
  SELECT year, name, population, country, longitude
  FROM citypops
