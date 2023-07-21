--Знайти оцінки студентів в окремій групі з певного предмета.
SELECT s.group_id,
       gr.name group_name,
       d.name discipline_name,
       s.fullname,
       g.grade,
       g.date_of 
FROM grades g
JOIN students s ON s.id = g.student_id 
JOIN groups gr ON gr.id = s.group_id 
JOIN disciplines d ON d.id  = g.discipline_id 
WHERE 1=1
  AND d.id = :DISCIPLINE_ID          -- код предмету
  AND gr.id = :GROUP_ID              -- код групи
ORDER BY s.group_id, s.fullname, g.date_of;
