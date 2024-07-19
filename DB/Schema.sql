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

CREATE TABLE financial_transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES properties(user_id),
    property_id INT REFERENCES properties(property_id),
    transaction_type VARCHAR(50),
    amount DECIMAL(10, 2),
    date DATE,
    description TEXT,
    plaid_transaction_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE todo_list (
    todo_id SERIAL PRIMARY KEY,
    property_id INT REFERENCES properties(property_id),
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ai_interactions (
    interaction_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES properties(user_id),
    property_id INT REFERENCES properties(property_id),
    request TEXT,
    response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
