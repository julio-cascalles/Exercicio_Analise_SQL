insert into Pessoa(id, nome, cpf, genero, idade)
values (51, 'Kely Creuza', '619.809.585-13', 'F', 19);
DELETE from Agenda WHERE paciente = 51
;
update Agenda SET hora='09:30', paciente=460
WHERE dia = '2023-04-23' AND medico = 222
