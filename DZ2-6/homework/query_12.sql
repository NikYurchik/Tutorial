--Оцінки студентів у певній групі з певного предмета на останньому занятті.
SELECT g.id group_id,
       g.name group_name,
       s.fullname,
       g3.discipline_id,
       g3.discipline_name,
       g3.max_date, 
       (SELECT g2.grade
        FROM grades g2
        WHERE g2.discipline_id = g3.discipline_id
          AND g2.student_id = s.id
          AND g2.date_of = g3.max_date) grade
FROM groups g 
JOIN students s ON s.group_id  = g.id 
JOIN (SELECT g2.discipline_id,     -- предмети з останніми датами занять
             d.name discipline_name,
             MAX(g2.date_of) max_date
		FROM grades g2
		JOIN disciplines d ON d.id = g2.discipline_id
		GROUP BY g2.discipline_id, d.name) g3
WHERE 1=1
  AND g.id = :GROUP_ID                    -- код групи
  AND g3.discipline_id = :DISCIPLINE_ID   -- код предмету
ORDER BY g.id, case when grade is NULL then grade else 0 end DESC , s.id
