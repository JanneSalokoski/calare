DROP TABLE IF EXISTS collections 	CASCADE;
DROP TABLE IF EXISTS resources 		CASCADE;
DROP TABLE IF EXISTS access_groups 	CASCADE;
DROP TABLE IF EXISTS users 			CASCADE;
DROP TABLE IF EXISTS bookings 		CASCADE;
DROP TABLE IF EXISTS resource_bookings CASCADE;

CREATE TABLE collections (
	serial_id 	SERIAL PRIMARY KEY,
	uuid_id 	UUID UNIQUE DEFAULT gen_random_uuid(),

	name 		TEXT NOT NULL
);

CREATE TABLE resources (
	serial_id 	SERIAL PRIMARY KEY,
	uuid_id 	UUID UNIQUE DEFAULT gen_random_uuid(),

	name 		TEXT NOT NULL,

	collection_id INT NOT NULL REFERENCES collections(serial_id)
);

CREATE TABLE access_groups (
	serial_id 	SERIAL PRIMARY KEY,
	uuid_id 	UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),

	name 		TEXT NOT NULL
);

CREATE TABLE users (
	serial_id 	SERIAL PRIMARY KEY,
	uuid_id 	UUID UNIQUE DEFAULT gen_random_uuid(),

	name 		TEXT NOT NULL,
	password 	TEXT NOT NULL,
	
	access_group_id INT NOT NULL REFERENCES access_groups(serial_id)
);

CREATE TABLE bookings (
	serial_id 	SERIAL PRIMARY KEY,
	uuid_id 	UUID UNIQUE DEFAULT gen_random_uuid(),

	title 		TEXT NOT NULL,
	description TEXT,
	start_time 	TIMESTAMP NOT NULL,
	end_time 	TIMESTAMP NOT NULL,

	user_id 	INT NOT NULL REFERENCES users(serial_id)
);

CREATE TABLE resource_bookings (
	serial_id 	SERIAL PRIMARY KEY,
	uuid_id 	UUID UNIQUE DEFAULT gen_random_uuid(),

	booking_id 	INT NOT NULL REFERENCES bookings(serial_id),
	resource_id INT NOT NULL REFERENCES resources(serial_id)
);

-- mock data

INSERT INTO collections (name)
VALUES
	  ('Uusi ylioppilastalo')
	, ('Domus Gaudium')
	;

INSERT INTO resources (name, collection_id)
VALUES
	  ('Alina', 		(SELECT serial_id FROM collections WHERE name='Uusi ylioppilastalo'))
	, ('Wilhelmsson', 	(SELECT serial_id FROM collections WHERE name='Uusi ylioppilastalo'))
	, ('Groudon', 		(SELECT serial_id FROM collections WHERE name='Domus Gaudium'))
	;

INSERT INTO access_groups (name)
VALUES
	  ('Admin')
	, ('User')
	, ('Guest')
	;

INSERT INTO users (name, password, access_group_id)
VALUES
	  ('Admin', 'password', (SELECT serial_id FROM access_groups WHERE name='Admin'))
	, ('Test', 	'password', (SELECT serial_id FROM access_groups WHERE name='User'))
	;

INSERT INTO bookings (title, description, start_time, end_time, user_id)
VALUES
	  (
		'Event 1'
		, ''
		, TIMESTAMP '2024-05-17 10:00:00'
		, TIMESTAMP '2024-05-17 12:00:00'
		, (SELECT serial_id FROM users WHERE name='Admin')
	  )
	  , (
		'Event 2'
		, ''
		, TIMESTAMP '2024-05-17 13:00:00'
		, TIMESTAMP '2024-05-17 16:00:00'
		, (SELECT serial_id FROM users WHERE name='Test')
	  )
	;

INSERT INTO resource_bookings (booking_id, resource_id)
VALUES
	(
		  (SELECT serial_id FROM bookings WHERE serial_id=1)
		, (SELECT serial_id FROM resources WHERE name='Alina')
	)
