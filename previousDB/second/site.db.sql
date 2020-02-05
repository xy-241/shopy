BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "cart_item" (
	"id"	INTEGER NOT NULL,
	"price"	FLOAT,
	"image_file"	VARCHAR(20) NOT NULL,
	"date_added"	DATETIME NOT NULL,
	"title"	VARCHAR(100) NOT NULL,
	"itemNum"	INTEGER NOT NULL,
	"owner_id"	INTEGER NOT NULL,
	FOREIGN KEY("owner_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "purchase_record" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(100) NOT NULL,
	"itemNum"	INTEGER NOT NULL,
	"date_added"	DATETIME NOT NULL,
	"review"	TEXT,
	"rating"	INTEGER,
	"buyerId"	INTEGER NOT NULL,
	FOREIGN KEY("buyerId") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "hacking_product" (
	"id"	INTEGER NOT NULL,
	"price"	FLOAT,
	"image_file"	VARCHAR(20) NOT NULL,
	"date_added"	DATETIME NOT NULL,
	"title"	VARCHAR(100) NOT NULL UNIQUE,
	"description"	TEXT NOT NULL,
	"category"	VARCHAR(100) NOT NULL,
	"itemNum"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "admin" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(20) NOT NULL UNIQUE,
	"email"	VARCHAR(120) NOT NULL UNIQUE,
	"image_file"	VARCHAR(20) NOT NULL,
	"password"	VARCHAR(60) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(20) NOT NULL UNIQUE,
	"email"	VARCHAR(120) NOT NULL UNIQUE,
	"image_file"	VARCHAR(20) NOT NULL,
	"password"	VARCHAR(60) NOT NULL,
	"deliveryInfo"	TEXT,
	PRIMARY KEY("id")
);
INSERT INTO "hacking_product" VALUES (1,9.99,'hackingHat.jpg','2019-09-23 08:15:59.864446','Hacker''s Hat','Every hacker should have one!','outfits',84);
INSERT INTO "hacking_product" VALUES (2,29.99,'hackingHoodie.jpg','2019-09-23 08:15:59.864446','Hacker''s Hoodie','Every hacker should a hoodie','outfits',187);
INSERT INTO "hacking_product" VALUES (3,19.99,'hackingToolPi.jpg','2019-09-23 08:15:59.864446','Pi Zero W','Every hacker should a pi to hack things out','tools',300);
INSERT INTO "hacking_product" VALUES (4,9.99,'hackingToolAd.jpg','2019-09-23 08:15:59.864446','Arduino UNO','Every hacker should have an Arduino UNO to play around!','tools',200);
INSERT INTO "admin" VALUES (10000000000,'Admin King','yu.xin.yang.yxy@gmail.com','default.jpg','$2b$12$bjFMpxWA9RF3OueH5vxa0.Zt6Yj4Vs.Qup.pjsOuhj1IKsawA747i');
INSERT INTO "user" VALUES (1,'XinYang','yu.xin.yang.yxy@gmail.com','default.jpg','$2b$12$KzxIXkle3rUAOKF0DU/dcOMJ3lqpHl80Ghn.f6douXnzOPC.f1IP2','Hougang');
INSERT INTO "user" VALUES (2,'Fishing','yu.xin.yang.fishing@gmail.com','default.jpg','$2b$12$lIgkJDOXHUBcKyCaQjC7qOa49/ATwDKVddnXhglD3QHySKxhIPU1W',NULL);
INSERT INTO "user" VALUES (3,'webhosting','yu.xin.yang.webhosting@gmail.com','default.jpg','$2b$12$uq/63Hby9rxvh.SuY3NTI.R8L7YMBoCvam7cTCtnQAMsSyiiXXfiG',NULL);
COMMIT;
