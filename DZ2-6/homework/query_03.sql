--Знайти середній бал у групах з певного предмета.
SELECT s.group_id,
       gr.name group_name,
       d.name discipline_name,
       ROUND(AVG(g.grade),2) avg_grade
FROM grades g
JOIN students s ON s.id = g.student_id 
JOIN groups gr ON gr.id = s.group_id 
JOIN disciplines d ON d.id  = g.discipline_id 
WHERE 1=1
  AND d.id = :DISCIPLINE_ID               -- код предмету
GROUP BY s.group_id, gr.name, d.name
ORDER BY s.group_id, AVG(g.grade) DESC;
