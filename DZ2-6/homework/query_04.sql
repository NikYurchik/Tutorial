--Знайти середній бал на потоці (по всій таблиці оцінок).
SELECT ROUND(AVG(g.grade),2) avg_grade
FROM grades g;
