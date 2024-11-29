#!/bin/bash

read -p "Enter login URL: " LOGIN_URL
read -p "Enter expenses URL: " EXPENSES_URL
read -p "Enter user info URL: " USER_INFO_URL
read -p "Enter username: " USERNAME
read -sp "Enter password: " PASSWORD
echo
read -p "Enter the number of expenses to post: " NUM_EXPENSES

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

  RANDOM_TIME=$((START + RANDOM % (END - START)))
  RANDOM_DATE=$(date -d @$RANDOM_TIME +"%Y-%m-%d")
  echo $RANDOM_DATE
}

get_random_amount() {
  MIN_AMOUNT=100
  MAX_AMOUNT=9999
  RANDOM_AMOUNT=$(shuf -i $MIN_AMOUNT-$MAX_AMOUNT -n 1)
  echo "$RANDOM_AMOUNT"
}

get_random_description() {
  DESCRIPTIONS=("Compra de ropa" "Pago de servicios" "Cena en restaurante" "Compra de libros" "Boleto de cine" "Gasolina" "Supermercado" "Regalo de cumpleaños")
  RANDOM_INDEX=$(shuf -i 0-$((${#DESCRIPTIONS[@]} - 1)) -n 1)
  echo "${DESCRIPTIONS[$RANDOM_INDEX]}"
}

get_random_category() {
  CATEGORIES=("Entretenimiento" "Alimentación" "Transporte" "Educación" "Salud" "Hogar" "Servicios" "Otros")
  NUM_CATEGORIES=1 # Asumiendo que solo se selecciona una categoría
  SELECTED_CATEGORIES=$(shuf -e "${CATEGORIES[@]}" -n $NUM_CATEGORIES)
  # Convertir a un arreglo JSON
  CATEGORY_ARRAY=$(printf '%s\n' "${SELECTED_CATEGORIES[@]}" | jq -R . | jq -s .)
  echo "$CATEGORY_ARRAY"
}

post_expense() {
  RANDOM_DATE=$(get_random_date)
  RANDOM_AMOUNT=$(get_random_amount)
  RANDOM_DESCRIPTION=$(get_random_description)
  RANDOM_CATEGORY=$(get_random_category)

  DATA=$(jq -n \
    --arg amount "$RANDOM_AMOUNT" \
    --arg date "$RANDOM_DATE" \
    --arg description "$RANDOM_DESCRIPTION" \
    --argjson category "$RANDOM_CATEGORY" \
    --argjson user "$USER_ID" \
    '{
      amount: ($amount | tonumber),
      description: $description,
      date: $date,
      user: $user,
      category: $category
    }')

  RESPONSE=$(curl -s -X POST $EXPENSES_URL \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -d "$DATA")

  echo "Response: $RESPONSE"
}

# Main
login
get_user_id
for i in $(seq 1 $NUM_EXPENSES); do
  echo "Posting expense $i"
  post_expense
done
