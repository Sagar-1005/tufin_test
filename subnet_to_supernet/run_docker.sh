#!bin/bash
touch coalesce_output.csv

docker build -t subnet_processor .

docker run --rm -v "$(pwd)/coalesce_input.csv:/home/tufin/coalesce_input.csv" -v "$(pwd)/coalesce_output.csv:/home/tufin/coalesce_output.csv" subnet_processor /home/tufin/coalesce_input.csv /home/tufin/coalesce_ouput.csv