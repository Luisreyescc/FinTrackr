# FinTrackr 💰

FinTrackr is a web application designed to help users manage their personal finances effectively. It allows users to register incomes and expenses 💸, categorize them 🏷️, track debts 🧾, and generate detailed reports with visualizations 📊.

## Features

- **Income and Expense Tracking** 💵: Register monthly incomes and expenses with descriptions.
- **Customizable Categories** 🏷️: Categorize transactions using tags like _Food_, _Transport_, _Housing_.
- **Multi-Income Support** 💰: Manage multiple income sources with different payment schedules.
- **Visual Reports** 📈: View expenses and incomes through graphs (pie charts, line charts, etc.) for various time frames (daily, weekly, monthly, annual).
- **Debt Management** 🧾: Record debts owed to others and track repayment status.
- **Historical Data Retrieval** 🗓️: Consult historical expenses by category within specified date ranges.
- **Automated Email Reports** ✉️: Receive periodic emails (configurable frequency) with PDF attachments containing detailed income and expense reports along with balance summaries.
- **Multi-User Support** 👥: Users can register and log in to access their personal financial data securely.
- **Admin Interface** 🛠️: Administrative panel for managing users.

## Technologies Used

- **Frontend**: [Vue.js](https://vuejs.org/).
- **Backend**: [Django](https://www.djangoproject.com/).
- **Database**: [MySQL](https://www.mysql.com/).
- **PDF Generation**: Programmatic PDF generation using [ReportLab](https://www.reportlab.com/opensource/).
- **Password Recovery**: Secure password recovery process through email verification.
- **Docker**: Containerization using [Docker](https://www.docker.com/) for easy setup and deployment.

## Installation

### Prerequisites

- **Docker** and **Docker Compose** installed on your machine.
- A Linux operating system or environment (the application is fully compatible with Linux without the need for emulation).

### Setup Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Luisreyescc/FinTrackr.git
   cd FinTrackr
   ```

2. **Build Docker Images**

   Build the necessary Docker image using the provided `Dockerfiles` and docker-compose.

   ```bash
   docker-compose up --build
   ```

3. **Access the Application**

   - Visit `http://localhost:8080` in your web browser to access the web application.

## Usage

### Registration and Authentication

- **Sign Up** 📝: Register a new account by providing your email and password.
- **Login** 🔐: Access your account using your credentials.

### Managing Finances

- **Add Incomes/Expenses** 💰: Register new incomes and expenses with descriptions, amounts, dates, and categories.
- **Create Categories** 🏷️: Add new custom categories to categorize your transactions effectively.
- **Track Debts** 📄: Record debts owed and monitor repayment status.
- **View Reports** 📊: Access the dashboard to view visual reports of your financial data over different time periods.
- **Configure Email Reports** ✉️: Set up periodic email reports and configure the frequency.

### Administrative Tasks

- **Admin Access** 🛠️: Log in to the admin interface to manage users and view aggregated reports.
- **User Management** 👥: View registered users and their activity.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear messages.
4. Push your branch to your forked repository.
5. Submit a pull request detailing your changes.

Please ensure all new code follows the project's coding conventions and includes appropriate tests.

## Contact

For any questions or support, please contact 📧 <fintracker0@gmail.com>

## Contributors

- [Luis Reyes](https://github.com/Luisreyescc)
- [Ianluck Rojo](https://github.com/Jeanluck-Rop)
- [Isaac Escobar](https://github.com/IsaacEscobar09)
- [David Bernabé](https://github.com/David-Brnb)
- [Gabriel Zárate](https://github.com/GABOZG-004)
