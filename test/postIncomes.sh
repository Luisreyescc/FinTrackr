#!/bin/bash

read -p "Enter login URL: " LOGIN_URL
read -p "Enter income URL: " INCOME_URL
read -p "Enter username: " USERNAME
read -sp "Enter password: " PASSWORD
echo
read -p "Enter the number of incomes to post: " NUM_INCOMES

ACCESS_TOKEN=""
USER_ID=""

login() {
  RESPONSE=$(curl -s -X POST $LOGIN_URL \
    -H "Content-Type: application/json" \
    -d '{"user_name": "'"$USERNAME"'", "password": "'"$PASSWORD"'"}')

  ACCESS_TOKEN=$(echo $RESPONSE | jq -r .access)
  USER_ID=$(echo $RESPONSE | jq -r .user_id)

  if [ "$ACCESS_TOKEN" == "null" ] || [ -z "$ACCESS_TOKEN" ]; then
    echo "Login failed. Invalid response: $RESPONSE"
    exit 1
  fi

  echo "Login successful. Token obtained: $ACCESS_TOKEN"
  echo "User ID: $USER_ID"
}

get_random_date() {
  START=$(date -d "2000-01-01" +%s)
  END=$(date -d "2024-11-22" +%s)

  RANDOM_TIME=$((START + $(od -An -N4 -i /dev/urandom) % (END - START)))
  RANDOM_DATE=$(date -d @$RANDOM_TIME +"%Y-%m-%d")
  echo $RANDOM_DATE
}

get_random_income() {
  MAX_AMOUNT=999999
  RANDOM_AMOUNT=$(shuf -i 1-$MAX_AMOUNT -n 1)
  echo $RANDOM_AMOUNT
}

get_random_description() {
  DESCRIPTIONS=("Freelance Work" "Gift" "Investment Return" "Salary Bonus" "Other Income")
  RANDOM_INDEX=$(shuf -i 0-$((${#DESCRIPTIONS[@]} - 1)) -n 1)
  echo "${DESCRIPTIONS[$RANDOM_INDEX]}"
}

get_random_source() {
  SOURCES=("Job" "Side Business" "Investments" "Freelance" "Other")
  RANDOM_INDEX=$(shuf -i 0-$((${#SOURCES[@]} - 1)) -n 1)
  echo "${SOURCES[$RANDOM_INDEX]}"
}

post_income() {
  RANDOM_DATE=$(get_random_date)
  RANDOM_INCOME=$(get_random_income)
  RANDOM_DESCRIPTION=$(get_random_description)
  RANDOM_SOURCE=$(get_random_source)

  DATA='{
    "amount": '"$RANDOM_INCOME"',
    "date": "'"$RANDOM_DATE"'",
    "description": "'"$RANDOM_DESCRIPTION"'",
    "source": "'"$RANDOM_SOURCE"'",
    "user": '"$USER_ID"'
  }'

  RESPONSE=$(curl -s -X POST $INCOME_URL \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -d "$DATA")

  echo "Response: $RESPONSE"
}

# Main
login
for i in $(seq 1 $NUM_INCOMES); do
  echo "Posting income $i"
  post_income
done
