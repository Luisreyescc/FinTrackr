#!/bin/bash

read -p "Enter login URL: " LOGIN_URL
read -p "Enter income URL: " INCOME_URL
read -p "Enter username: " USERNAME
read -sp "Enter password: " PASSWORD
echo
read -p "Enter the number of incomes to post: " NUM_INCOMES

ACCESS_TOKEN=""

login() {
  RESPONSE=$(curl -s -X POST $LOGIN_URL \
    -H "Content-Type: application/json" \
    -d '{"user_name": "'"$USERNAME"'", "password": "'"$PASSWORD"'"}')

  ACCESS_TOKEN=$(echo $RESPONSE | jq -r .access)

  if [ "$ACCESS_TOKEN" == "null" ] || [ -z "$ACCESS_TOKEN" ]; then
    echo "Login failed. Invalid response: $RESPONSE"
    exit 1
  fi

  echo "Login successful. Token obtained: $ACCESS_TOKEN"
}

get_random_date() {
  START=$(date -d "2000-01-01" +%s)
  END=$(date -d "2024-12-31" +%s)

  RANDOM_TIME=$((START + $(od -An -N4 -i /dev/urandom) % (END - START)))
  RANDOM_DATE=$(date -d @$RANDOM_TIME +"%Y-%m-%d")
  echo $RANDOM_DATE
}

get_random_income() {
  MAX_AMOUNT=999999
  RANDOM_AMOUNT=$(shuf -i 1-$MAX_AMOUNT -n 1)
  echo $RANDOM_AMOUNT
}

post_income() {
  RANDOM_DATE=$(get_random_date)
  RANDOM_INCOME=$(get_random_income)

  DATA='{
    "amount": '"$RANDOM_INCOME"',
    "date": "'"$RANDOM_DATE"'"
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
