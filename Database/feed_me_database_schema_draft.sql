# Create schemas

CREATE DATABASE IF NOT EXISTS feedme;

# Create tables
CREATE TABLE IF NOT EXISTS user
(
    id INT NOT NULL,
    username VARCHAR(255) NOT NULL,
    encrpt_pw VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    is_admin tinyint,
    email VARCHAR(255) NOT NULL,
    created DATE,
    modified DATE,
    deleted DATE,
    PRIMARY KEY(id)
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS video
(
    id INT NOT NULL,
    user_id INT NOT NULL,
    is_public tinyint,
    file_path VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    duration INT,
    insctruction LONGTEXT,
    price INT,
    view_count BIGINT,
    rating tinyint,
    suspended tinyint,
    suspended_date DATE,
    created DATE,
    modified DATE,
    deleted DATE,
    PRIMARY KEY(id)
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS comment
(
    id INT NOT NULL,
    user_id INT NOT NULL,
    video_id INT NOT NULL,
    comment LONGTEXT,
    suspended tinyint,
    suspended_date DATE,
    created DATE,
    modified DATE,
    deleted DATE,
    PRIMARY KEY(id)
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS timeMarker
(
    id INT NOT NULL,
    content VARCHAR(255),
    PRIMARY KEY(id)
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS videoTimeMarkerMapping
(
    id INT NOT NULL,
    video_id INT ,
    time_point INT,
    time_marker_id INT,
    deleted DATE,
    PRIMARY KEY(id)
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS ingredient
(
    id INT NOT NULL,
    ingredient VARCHAR(255),
    PRIMARY KEY(id)
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS videoIngredientMapping
(
    id INT NOT NULL,
    ingredient_id INT,
    video_id INT,
    created DATE,
    deleted DATE,
    PRIMARY KEY(id)
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS taste
(
    id INT NOT NULL,
    taste VARCHAR(255),
    PRIMARY KEY(id)
) ENGINE=MYISAM;

CREATE TABLE IF NOT EXISTS videoTasteMapping
(
    id INT NOT NULL,
    taste_id INT,
    video_id INT,
    created DATE,
    deleted DATE,
    PRIMARY KEY(id)
) ENGINE=MYISAM;


-- # Create FKs
-- ALTER TABLE comment
--     ADD    FOREIGN KEY (user_id)
--     REFERENCES user(id)
-- ;
    
-- ALTER TABLE comment
--     ADD    FOREIGN KEY (video_id)
--     REFERENCES video(id)
-- ;
    
-- ALTER TABLE video
--     ADD    FOREIGN KEY (user_id)
--     REFERENCES user(id)
-- ;
    
-- ALTER TABLE videoTimeMarkerMapping
--     ADD    FOREIGN KEY (video_id)
--     REFERENCES video(id)
-- ;
    
-- ALTER TABLE videoTimeMarkerMapping
--     ADD    FOREIGN KEY (time_marker_id)
--     REFERENCES timeMarker(id)
-- ;
    
-- ALTER TABLE videoIngredientMapping
--     ADD    FOREIGN KEY (ingredient_id)
--     REFERENCES ingredient(id)
-- ;
    
-- ALTER TABLE videoIngredientMapping
--     ADD    FOREIGN KEY (video_id)
--     REFERENCES video(id)
-- ;
    
-- ALTER TABLE videoTasteMapping
--     ADD    FOREIGN KEY (taste_id)
--     REFERENCES taste(id)
-- ;
    
-- ALTER TABLE videoTasteMapping
--     ADD    FOREIGN KEY (video_id)
--     REFERENCES video(id)
-- ;
    

# Create Indexes

