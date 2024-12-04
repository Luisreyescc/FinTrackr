#!/bin/bash

read -p "Enter login URL: " LOGIN_URL
read -p "Enter income URL: " INCOME_URL
read -p "Enter user info URL: " USER_INFO_URL
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

  echo "Login response: $RESPONSE"

  ACCESS_TOKEN=$(echo $RESPONSE | jq -r .access)

  if [ "$ACCESS_TOKEN" == "null" ] || [ -z "$ACCESS_TOKEN" ]; then
    echo "Login failed. Invalid response: $RESPONSE"
    exit 1
  fi

  echo "Login successful. Token obtained: $ACCESS_TOKEN"
}

get_user_id() {
  RESPONSE=$(curl -s -X GET $USER_INFO_URL \
    -H "Authorization: Bearer $ACCESS_TOKEN")

  echo "User info response: $RESPONSE"

  USER_ID=$(echo $RESPONSE | jq -r '.[0].user_id')

  if [ "$USER_ID" == "null" ] || [ -z "$USER_ID" ]; then
    echo "Failed to retrieve user ID. Invalid response: $RESPONSE"
    exit 1
  fi

  echo "User ID obtained: $USER_ID"
}

get_random_date() {
  START=$(date -d "2000-01-01" +%s)
  END=$(date -d "2024-12-31" +%s)

  RANDOM_TIME=$((START + $(od -An -N4 -i /dev/urandom) % (END - START)))
  RANDOM_DATE=$(date -d @$RANDOM_TIME +"%Y-%m-%d")
  echo $RANDOM_DATE
}

get_random_income() {
  MIN_AMOUNT=100
  MAX_AMOUNT=9999
  RANDOM_AMOUNT=$(shuf -i $MIN_AMOUNT-$MAX_AMOUNT -n 1)
  echo "$RANDOM_AMOUNT"
}

get_random_description() {
  DESCRIPTIONS=("nomina de banco" "pago de proyecto" "bonificación" "regalo" "otro ingreso")
  RANDOM_INDEX=$(shuf -i 0-$((${#DESCRIPTIONS[@]} - 1)) -n 1)
  echo "${DESCRIPTIONS[$RANDOM_INDEX]}"
}

get_random_category() {
  CATEGORIES=("work" "investment" "gift" "bonus" "other")
  RANDOM_INDEX=$(shuf -i 0-$((${#CATEGORIES[@]} - 1)) -n 1)
  echo "${CATEGORIES[$RANDOM_INDEX]}"
}

post_income() {
  RANDOM_DATE=$(get_random_date)
  RANDOM_INCOME=$(get_random_income)
  RANDOM_DESCRIPTION=$(get_random_description)
  RANDOM_CATEGORY=$(get_random_category)

  DATA=$(jq -n \
    --arg amount "$RANDOM_INCOME" \
    --arg date "$RANDOM_DATE" \
    --arg description "$RANDOM_DESCRIPTION" \
    --arg category "$RANDOM_CATEGORY" \
    --argjson user "$USER_ID" \
    '{
      amount: ($amount | tonumber),
      description: $description,
      date: $date,
      category: [$category],
      user: $user
    }')

  RESPONSE=$(curl -s -X POST $INCOME_URL \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -d "$DATA")

  echo "Response: $RESPONSE"
}

# Main
login
get_user_id
for i in $(seq 1 $NUM_INCOMES); do
  echo "Posting income $i"
  post_income
done
one
