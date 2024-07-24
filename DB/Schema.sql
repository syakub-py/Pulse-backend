CREATE TABLE properties (
    property_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL UNIQUE,
    nick_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    image_urls VARCHAR(255),
    property_type VARCHAR(50) CHECK (property_type IN ('Home', 'Vacation Home','Apartment', 'Condo')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE smart_devices (
    device_id SERIAL PRIMARY KEY,
    property_id INT REFERENCES properties(property_id),
    device_name VARCHAR(255) NOT NULL,
    device_type VARCHAR(100),
    device_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES properties(user_id),
    property_id INT REFERENCES properties(property_id),
    transaction_type VARCHAR(50),
    amount DECIMAL(10, 2),
    date TIMESTAMP,
    description VARCHAR(200),
    plaid_transaction_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE todo (
    todo_id SERIAL PRIMARY KEY,
    property_id INT REFERENCES properties(property_id),
    description VARCHAR(2000) NOT NULL,
    status VARCHAR(50) CHECK (status IN ('active', 'inactive', 'pending')),
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chats (
    chat_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    chat_id SERIAL REFERENCES chats(chat_id),
    role VARCHAR(10) CHECK (role IN ('user', 'assistant')) NOT NULL,
    message TEXT NOT NULL,
    created_at VARCHAR(60)
);
