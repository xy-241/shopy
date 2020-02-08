BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(20) NOT NULL UNIQUE,
	"email"	VARCHAR(120) NOT NULL UNIQUE,
	"image_file"	VARCHAR(20) NOT NULL,
	"password"	VARCHAR(60) NOT NULL,
	"deliveryInfo"	TEXT,
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
CREATE TABLE IF NOT EXISTS "purchase_record" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(100) NOT NULL,
	"itemNum"	INTEGER NOT NULL,
	"date_added"	DATETIME NOT NULL,
	"review"	TEXT,
	"rating"	INTEGER,
	"buyerId"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("buyerId") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "cart_item" (
	"id"	INTEGER NOT NULL,
	"price"	FLOAT,
	"image_file"	VARCHAR(20) NOT NULL,
	"date_added"	DATETIME NOT NULL,
	"title"	VARCHAR(100) NOT NULL,
	"itemNum"	INTEGER NOT NULL,
	"owner_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("owner_id") REFERENCES "user"("id")
);
INSERT INTO "user" VALUES (4,'ads','yu.xin.yang.ads@gmail.com','default.jpg','$2b$12$UvpNv8WiGXScVq/JU.kI9uQmZ.H2hL2OGpfBX92Bd6C6StMDGbY0W','Hougang');
INSERT INTO "admin" VALUES (10000000000,'Admin King','yu.xin.yang.yxy@gmail.com','07916055ebb75007.jpg','$2b$12$bjFMpxWA9RF3OueH5vxa0.Zt6Yj4Vs.Qup.pjsOuhj1IKsawA747i');
INSERT INTO "hacking_product" VALUES (1,9.99,'hackingHat.jpg','2019-09-23 08:15:59.864446','Hacker''s Hat','Every hacker should have one!','outfits',83);
INSERT INTO "hacking_product" VALUES (2,29.99,'hackingHoodie.jpg','2019-09-23 08:15:59.864446','Hacker''s Hoodie','Every hacker should a hoodie','outfits',121);
INSERT INTO "hacking_product" VALUES (3,19.99,'hackingToolPi.jpg','2019-09-23 08:15:59.864446','Pi Zero W','Every hacker should a pi to hack things out','tools',299);
INSERT INTO "hacking_product" VALUES (4,9.99,'hackingToolAd.jpg','2019-09-23 08:15:59.864446','Arduino UNO','Every hacker should have an Arduino UNO to play around!','tools',200);
INSERT INTO "purchase_record" VALUES (1,'Hacker''s Hat',1,'2020-02-05 18:19:28.373901','User didt give any review, 5 stars by default',5,2);
INSERT INTO "purchase_record" VALUES (2,'Hacker''s Hoodie',65,'2020-02-05 18:20:14.618917','User didt give any review, 5 stars by default',5,2);
INSERT INTO "purchase_record" VALUES (3,'Pi Zero W',1,'2020-02-06 04:47:02.836838','User didt give any review, 5 stars by default',5,4);
COMMIT;
