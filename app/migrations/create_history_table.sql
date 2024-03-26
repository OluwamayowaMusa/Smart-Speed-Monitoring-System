-- Create history table in smart_speed database
CREATE TABLE IF NOT EXISTS history(
	id INT NOT NULL AUTO_INCREMENT,
	speed SMALLINT NOT NULL,
	trespassed_at TEXT NOT NULL,
	PRIMARY KEY (id)
);
