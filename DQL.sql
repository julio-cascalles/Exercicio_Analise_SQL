select genero , 
    avg(idade),count(*)
FROM 
    Pessoas p 
    left JOIN
        Trabalho t ON (p.id = t.pessoa)
    RIGHT join 
        Endereco e on (p.id = e.pessoa)
where
    estado_civil not LIKE '%ado' AND uf = 'SP'
    OR salario > 5000 or departamento in (14, 25, 38)
GROUP BY
    genero
order by
    3 DESC
