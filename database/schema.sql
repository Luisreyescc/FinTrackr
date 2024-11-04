CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash CHAR(64) NOT NULL,
);

CREATE TABLE incomes (
    income_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    source VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE expenses (
    expense_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount DOUBLE,
    description TEXT,
    date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE expense_categories (
    expense_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (expense_id, category_id),
    FOREIGN KEY (expense_id) REFERENCES expenses(expense_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE debts (
    debt_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    debtor_name VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    is_payed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE debt_categories (
    debt_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (debt_id, category_id),
    FOREIGN KEY (debt_id) REFERENCES debts(debt_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
