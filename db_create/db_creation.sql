CREATE SCHEMA IF NOT EXISTS jarvis_db;

-- Create the total_chats table
CREATE TABLE total_chats (
    total_chats_id INT AUTO_INCREMENT PRIMARY KEY,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create the users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    total_chats_id INT UNIQUE,
    CONSTRAINT fk_total_chats FOREIGN KEY (total_chats_id)
    REFERENCES total_chats (total_chats_id)
);


-- Create the chats table
CREATE TABLE chats (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    total_chats_id INT,
    CONSTRAINT fk_chats_total_chats FOREIGN KEY (total_chats_id)
    REFERENCES total_chats (total_chats_id)
);

-- Create the messages table
CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(255) NOT NULL,
    agent VARCHAR(255) NOT NULL,
    temp DECIMAL(5,2) NOT NULL,
    message TEXT NOT NULL,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    chat_id INT,
    CONSTRAINT fk_messages_chats FOREIGN KEY (chat_id)
    REFERENCES chats (chat_id)
);

CREATE TABLE website_state (
    website_state_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    tts BOOLEAN NOT NULL,
    stt BOOLEAN NOT NULL,
    current_chat INT,
    model_selected VARCHAR(255) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    agent_selected VARCHAR(255) NOT NULL,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_website_state_user FOREIGN KEY (user_id)
        REFERENCES users (user_id),
    CONSTRAINT fk_website_state_chat FOREIGN KEY (current_chat)
        REFERENCES chats (chat_id)
);

-- Create the models table
CREATE TABLE models (
    model_id INT AUTO_INCREMENT PRIMARY KEY,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    model_name VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    model_info TEXT NOT NULL
);

-- Create the functions table
CREATE TABLE functions (
    function_id INT AUTO_INCREMENT PRIMARY KEY,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    function_name VARCHAR(255) NOT NULL,
    function_description TEXT NOT NULL,
    function_inputs TEXT NOT NULL,
    function_output TEXT NOT NULL,
    function_json TEXT NOT NULL
);

-- Create the long_term_memory table first
CREATE TABLE long_term_memory (
    long_term_memory_id INT AUTO_INCREMENT PRIMARY KEY,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    long_term_memory_description TEXT NOT NULL
);

-- Create the contextual_environmental_memory table
CREATE TABLE contextual_environmental_memory (
    contextual_environmental_memory_id INT AUTO_INCREMENT PRIMARY KEY,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    contextual_environmental_memory_description TEXT NOT NULL
);

-- Create the agents table
CREATE TABLE agents (
    agent_id INT AUTO_INCREMENT PRIMARY KEY,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    agent_name VARCHAR(255) NOT NULL,
    agent_description TEXT NOT NULL,
    base_temp FLOAT NOT NULL,
    base_model VARCHAR(255) NOT NULL,
    long_term_memory BOOLEAN NOT NULL,
    task_delegation BOOLEAN NOT NULL,
    contextual_environmental_memory BOOLEAN NOT NULL,
    emotional_intelligence BOOLEAN NOT NULL,
    contextual_environmental_memory_id INT,
    long_term_memory_id INT,
    CONSTRAINT fk_agent_ltm FOREIGN KEY (long_term_memory_id)
        REFERENCES long_term_memory (long_term_memory_id),
    CONSTRAINT fk_agent_ce_memory FOREIGN KEY (contextual_environmental_memory_id)
        REFERENCES contextual_environmental_memory (contextual_environmental_memory_id)
);


-- Table for linking agents to functions (many-to-many relationship)
CREATE TABLE agent_functions (
    agent_id INT,
    function_id INT,
    PRIMARY KEY (agent_id, function_id),
    CONSTRAINT fk_agent_function_agent FOREIGN KEY (agent_id)
        REFERENCES agents (agent_id),
    CONSTRAINT fk_agent_function_function FOREIGN KEY (function_id)
        REFERENCES functions (function_id)
);

-- Create the total_passwords table
CREATE TABLE IF NOT EXISTS total_passwords (
    password_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    password VARCHAR(255) NOT NULL,
    website VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_total_passwords_users FOREIGN KEY (user_id)
        REFERENCES users (user_id)
);

