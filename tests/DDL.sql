/* 
    Médico ou Paciente:
*/
CREATE TABLE Pessoa(
    id INTEGER identity(1,1) PRIMARY KEY,
    nome varchar(30),
    cpf CHAR(11) UNIQUE
);
/*
    Horários de consultas:
*/
create table Agenda(
    dia DATE,
    hora char(5),  /* Formato hh:nn  (h = hora, n = minuto) */
    medico INTEGER foreign key REFERENCES Pessoa(id),
    paciente integer FOREIGN KEY references Pessoa(id),
    custo float NOT NULL,
    primary key (dia, hora)
);