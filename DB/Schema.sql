CREATE TABLE properties (
    property_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    nick_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    property_type VARCHAR(50) CHECK (property_type IN ('Home', 'Vacation Home', 'Condo', 'Multi-Family', 'Commercial Building')),
    is_rental BOOLEAN CHECK (is_rental IN (TRUE, FALSE)),
    created_at VARCHAR(60)
);

CREATE TABLE leases (
    lease_id SERIAL PRIMARY KEY,
    start_date VARCHAR(60) NOT NULL,
    end_date VARCHAR(60) NOT NULL,
    monthly_rent VARCHAR(60) NOT NULL
);

CREATE TABLE property_leases (
     property_id INTEGER NOT NULL,
     lease_id INTEGER,
     PRIMARY KEY (property_id, lease_id),
     FOREIGN KEY (property_id) REFERENCES properties (property_id),
     FOREIGN KEY (lease_id) REFERENCES leases (lease_id)
);

CREATE TABLE tenant_leases (
     tenant_id INTEGER NOT NULL,
     lease_id INTEGER,
     PRIMARY KEY (tenant_id, lease_id),
     FOREIGN KEY (tenant_id) REFERENCES tenants (tenant_id),
     FOREIGN KEY (lease_id) REFERENCES leases (lease_id)
);

CREATE TABLE tenants (
     tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
     name VARCHAR NOT NULL,
     dob DATE NOT NULL,
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
      created_at VARCHAR(60),
      updated_at VARCHAR(60)
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
