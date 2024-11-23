#!/bin/bash

read -p "Enter login URL: " LOGIN_URL
read -p "Enter expenses URL: " EXPENSES_URL
read -p "Enter username: " USERNAME
read -sp "Enter password: " PASSWORD
echo
read -p "Enter the user ID: " USER_ID
read -p "Enter the number of expenses to post: " NUM_EXPENSES

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
  END=$(date -d "2024-11-22" +%s)

  RANDOM_TIME=$((START + $(od -An -N4 -i /dev/urandom) % (END - START)))
  RANDOM_DATE=$(date -d @$RANDOM_TIME +"%Y-%m-%d")
  echo $RANDOM_DATE
}

get_random_amount() {
  MIN_AMOUNT=1000
  MAX_AMOUNT=999999
  RANDOM_AMOUNT=$(shuf -i $MIN_AMOUNT-$MAX_AMOUNT -n 1)
  echo $RANDOM_AMOUNT
}

get_random_description() {
  DESCRIPTIONS=("Groceries for the week" "Rent paid" "New gamer PC" "New smartphone" "Party with friends" "Dining Out" "Utilities" "Entertainment")
  RANDOM_INDEX=$(shuf -i 0-$((${#DESCRIPTIONS[@]} - 1)) -n 1)
  echo "${DESCRIPTIONS[$RANDOM_INDEX]}"
}

get_random_category() {
  CATEGORIES=("Groceries" "Food" "Travel" "Rent" "Utilities" "Entertainment" "Shopping" "Education" "Health" "Transportation" "Bills" "Taxes")
  NUM_CATEGORIES=$(shuf -i 1-2 -n 1)
  SELECTED_CATEGORIES=$(shuf -e "${CATEGORIES[@]}" -n $NUM_CATEGORIES | jq -R . | jq -s .)
  echo $SELECTED_CATEGORIES
}

post_expense() {
  RANDOM_DATE=$(get_random_date)
  RANDOM_AMOUNT=$(get_random_amount)
  RANDOM_DESCRIPTION=$(get_random_description)
  RANDOM_CATEGORY=$(get_random_category)

  DATA='{
    "user": '"$USER_ID"',
    "amount": '"$RANDOM_AMOUNT"',
    "description": "'"$RANDOM_DESCRIPTION"'",
    "date": "'"$RANDOM_DATE"'",
    "category": '"$RANDOM_CATEGORY"'
  }'

  RESPONSE=$(curl -s -X POST $EXPENSES_URL \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -d "$DATA")

  echo "Response: $RESPONSE"
}

# Main
login
for i in $(seq 1 $NUM_EXPENSES); do
  echo "Posting expense $i"
  post_expense
done
