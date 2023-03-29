#!/bin/bash

# Function to generate a random 16-character hexadecimal string
generate_hex_filename() {
  hex_chars="0123456789abcdef"
  filename=""
  for i in {1..16}; do
    random_index=$((RANDOM % 16))
    filename="${filename}${hex_chars:$random_index:1}"
  done
  echo "$filename"
}

# Function to generate a random Base58 string of a given length
generate_base58_string() {
  base58_chars="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
  base58_string=""
  length=$1
  for i in $(seq 1 $length); do
    random_index=$((RANDOM % 58))
    base58_string="${base58_string}${base58_chars:$random_index:1}"
  done
  echo "$base58_string"
}

# Function to set system date and time to a specific datetime
set_system_datetime() {
  target_datetime="$1"
  sudo date -s "$target_datetime"
}

# Generate and commit files for each day from May 8, 2021, onwards
start_date=" 2023-03-30"
end_date="2025-03-15"  # Current date

# Track the number of new files created
new_files=()

# Loop through each day
current_date="$start_date"
while [ "$current_date" != "$end_date" ]; do
  # Generate and commit 0 - 8 files
  num_commits=$((RANDOM % 8))  # Randomly select between 0 to 8 commits
  for (( c=1; c<=$num_commits; c++ )); do
    # Set a random hour, minute, and second for each commit
    random_hour=$(printf "%02d" $((RANDOM % 24)))
    random_minute=$(printf "%02d" $((RANDOM % 60)))
    random_second=$(printf "%02d" $((RANDOM % 60)))
    current_datetime="$current_date $random_hour:$random_minute:$random_second"

    # Set system date and time
    set_system_datetime "$current_datetime"

    if [ "${#new_files[@]}" -lt 30 ]; then
      # Generate random filename and Base58 content
      filename=$(generate_hex_filename)
      length=$((150 + RANDOM % 151))
      base58_string=$(generate_base58_string $length)
      
      # Create the file
      echo "$base58_string" > "$filename"
      new_files+=("$filename")
      
      # Commit the file to git
      git add "$filename"
      git commit --date="$current_datetime" -m "Add file $filename on $current_datetime"
      
      echo "File created and committed: $filename at $current_datetime"
    else
      # Concatenate new Base58 content to one of the new files created during this run
      existing_file=${new_files[$((RANDOM % 30))]}  # Randomly pick an existing new file
      length=$((150 + RANDOM % 151))
      base58_string=$(generate_base58_string $length)
      
      echo "$base58_string" >> "$existing_file"
      
      # Commit the changes to git
      git add "$existing_file"
      git commit --date="$current_datetime" -m "Update file $existing_file on $current_datetime"
      
      echo "File updated and committed: $existing_file at $current_datetime"
    fi
  done

  # Move to the next day
  current_date=$(date -I -d "$current_date + 1 day")
done
