CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    merchant VARCHAR(128) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'pending',
    risk_score DECIMAL(5, 2),
    risk_level VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS risk_scores (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER REFERENCES transactions(id),
    risk_score DECIMAL(5, 2) NOT NULL,
    risk_level VARCHAR(10) NOT NULL,
    factors TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO transactions (user_id, amount, merchant, currency, status) VALUES
    ('user-seed-1', 25.00, 'Coffee Shop', 'USD', 'processed'),
    ('user-seed-2', 150.00, 'Electronics Store', 'USD', 'processed');
