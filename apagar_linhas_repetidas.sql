CREATE TABLE "BBDC3.SA3" AS SELECT * FROM "BBDC3.SA";

DELETE from "BBDC3.SA3"

ALTER TABLE "BBDC3.SA3"
ADD numero INT ;


INSERT INTO "BBDC3.SA3" With "CTE" as (Select Datetime,Close,row_number()
Over (partition by Datetime order by Datetime) as contagem_elemento
From "BBDC3.SA")

Select * from "CTE" where contagem_elemento =1 order by Datetime;

CREATE TABLE "BBDC3.SA4" (
	"Datetime"	TIMESTAMP,
	"Close"	FLOAT
);

INSERT into "BBDC3.SA4"
SELECT Datetime, Close from "BBDC3.SA3"

/* Falta somente dropar a outra tabela e renomear ela*/

DROP TABLE "BBDC3.SA3"

ALTER TABLE "BBDC3.SA4" RENAME TO "BBDC3.SA3"