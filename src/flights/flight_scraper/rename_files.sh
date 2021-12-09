cd ./flights_information

for file in *.csv
do
  mv "$file" "${file/_flights.csv/_heathrow_flights.csv}"
done