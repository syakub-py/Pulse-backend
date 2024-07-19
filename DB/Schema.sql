CREATE TABLE properties (
    property_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(100),
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
    user_id INT REFERENCES properties(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES chats(chat_id),
    sender_id INTEGER REFERENCES properties(user_id),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
