# README - Mass Posting Scripts

These scripts allow you to perform mass postings on different social media platforms in an automated manner. Make sure you have the necessary credentials and comply with the usage policies of each platform.

## Requirements

- Have [curl](https://curl.se/) installed.
- Access to the APIs of the platforms where you want to post.
- Authentication credentials (API keys, tokens, etc.).

## How to Run the Scripts

1. **Make the scripts executable:**

   Open a terminal and navigate to the directory where the scripts are located. Then, run the following command for each script:

   ```bash
   chmod +x postIncomes.sh
   chmod +x postExpenses.sh

   ```

2. **Run the script:**

   ```bash
   ./postIncomes.sh
   ./postExpenses.sh
   ```

### Additionally, the scripts require the following URLs

    - Login URL: http://localhost:8000/api/login/
    - Income URL: http://localhost:8000/api/incomes/
    - User Info URL: http://localhost:8000/api/users/
