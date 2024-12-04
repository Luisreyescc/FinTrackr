#!/bin/bash

read -p "enter login url: " login_url
read -p "enter expenses url: " expenses_url
read -p "enter user info url: " user_info_url
read -p "enter username: " username
read -sp "enter password: " password
echo
read -p "enter the number of expenses to post: " num_expenses

access_token=""
user_id=""

login() {
  response=$(curl -s -X POST $login_url \
    -H "Content-Type: application/json" \
    -d '{"user_name": "'"$username"'", "password": "'"$password"'"}')

  echo "login response: $response"

  access_token=$(echo $response | jq -r .access)

  if [ "$access_token" == "null" ] || [ -z "$access_token" ]; then
    echo "login failed. invalid response: $response"
    exit 1
  fi

  echo "login successful. token obtained: $access_token"
}

get_user_id() {
  response=$(curl -s -X GET $user_info_url \
    -H "Authorization: Bearer $access_token")

  echo "user info response: $response"

  user_id=$(echo $response | jq -r '.[0].user_id')

  if [ "$user_id" == "null" ] || [ -z "$user_id" ]; then
    echo "failed to retrieve user id. invalid response: $response"
    exit 1
  fi

  echo "user id obtained: $user_id"
}

get_random_date() {
  START=$(date -d "2000-01-01" +%s)
  END=$(date -d "2024-12-31" +%s)

  RANDOM_TIME=$((START + $(od -An -N4 -i /dev/urandom) % (END - START)))
  RANDOM_DATE=$(date -d @$RANDOM_TIME +"%Y-%m-%d")
  echo $RANDOM_DATE
}

get_random_amount() {
  min_amount=100
  max_amount=9999
  random_amount=$(shuf -i $min_amount-$max_amount -n 1)
  echo "$random_amount"
}

get_random_description() {
  descriptions=("compra de ropa" "pago de servicios" "cena en restaurante" "compra de libros" "boleto de cine" "gasolina" "supermercado" "regalo de cumpleaños")
  random_index=$(shuf -i 0-$((${#descriptions[@]} - 1)) -n 1)
  echo "${descriptions[$random_index]}"
}

get_random_category() {
  categories=("entretenimiento" "alimentación" "transporte" "educación" "salud" "hogar" "servicios" "otros")
  random_index=$(shuf -i 0-$((${#categories[@]} - 1)) -n 1)
  # Enviar como array
  echo "[\"${categories[$random_index]}\"]"
}

post_expense() {
  random_date=$(get_random_date)
  random_amount=$(get_random_amount)
  random_description=$(get_random_description)
  random_category=$(get_random_category)

  data=$(jq -n \
    --arg amount "$random_amount" \
    --arg date "$random_date" \
    --arg description "$random_description" \
    --argjson category "$random_category" \
    --arg user "$user_id" \
    '{
      amount: ($amount | tonumber),
      description: $description,
      date: $date,
      user: $user,
      category: $category
    }')

  response=$(curl -s -X POST $expenses_url \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $access_token" \
    -d "$data")

  echo "response: $response"
}

# main
login
get_user_id
for i in $(seq 1 $num_expenses); do
  echo "posting expense $i"
  post_expense
done
