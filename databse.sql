-- CREATE TABLE users (
--     email VARCHAR(255) PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     hashed_password VARCHAR(255) NOT NULL,
--     last_view BIGINT NOT NULL
-- );

-- -- Create allData table
-- CREATE TABLE allData (
--     id VARCHAR(36) PRIMARY KEY,
--     title VARCHAR(255) NOT NULL,
--     location VARCHAR(100) NOT NULL,
--     company VARCHAR(100) NOT NULL,
--     description NTEXT,
--     dateUpdated BIGINT NOT NULL
-- );

-- Create resumeList table
CREATE TABLE resumeList (
    resumeId INT PRIMARY KEY IDENTITY(1,1),
    resumeName VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- Create applyQueue table
-- CREATE TABLE applyQueue (
--     id VARCHAR(36) NOT NULL,
--     timeOfArrival BIGINT NOT NULL,
--     selectedResume VARCHAR(255) NOT NULL,
--     email VARCHAR(255) NOT NULL
-- );

-- -- Create scoreBoard table
-- CREATE TABLE scoreBoard (
--     contender VARCHAR(255) NOT NULL,
--     score INT NOT NULL,
--     PRIMARY KEY (contender)
-- );
