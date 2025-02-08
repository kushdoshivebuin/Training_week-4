-- 1. Pet id, Pet name, Owner name, Owner surname, Owner city and total expense done for procedures
SELECT p.petid AS pet_id,
    p.name AS pet_name, 
    o.name AS owner_name, 
    o.surname AS owner_surname, 
    o.city AS owner_city,
    SUM(CASE 
            WHEN pd.proceduretype = ph.proceduretype 
                 AND pd.proceduresubcode = ph.proceduresubcode
            THEN pd.price
            ELSE 0
        END)AS total_expense
FROM owners AS o
JOIN pets AS p ON o.ownerid = p.ownerid
JOIN procedurehistory AS ph ON ph.petid = p.petid
JOIN proceduredetails AS pd ON pd.proceduresubcode = ph.proceduresubcode
GROUP BY p.petid, p.name, o.name, o.surname, o.city
ORDER BY p.petid ASC;

select * from procedurehistory where petid = 'X0-8765';
-- 2. City wise count of different different animals
SELECT o.city, p.kind, count(p.kind) as count_of_animals FROM pets as p
JOIN owners AS o ON p.ownerid = o.ownerid
GROUP BY o.city, p.kind
ORDER by o.city ASC;

-- 3. A particular kind of procedure has how much expense for a particular animal
SELECT count(*), ph.proceduretype, ph.proceduresubcode, pd.price*count(*) as total_income FROM procedurehistory as ph
JOIN proceduredetails AS pd ON ph.proceduretype = pd.proceduretype AND ph.proceduresubcode = pd.proceduresubcode
JOIN pets AS p ON ph.petid = p.petid
GROUP BY ph.proceduretype, ph.proceduresubcode, pd.price
ORDER BY ph.proceduretype, ph.proceduresubcode;

-- 4. Display those records which are in the procedurehistory table but not in the pets table
SELECT DISTINCT(ph.petid) FROM procedurehistory AS ph, pets AS p
WHERE ph.petid != p.petid;