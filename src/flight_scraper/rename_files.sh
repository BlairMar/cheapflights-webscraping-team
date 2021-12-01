cd ./flights_information

for file in *.csv
do
  mv "$file" "${file/.csv/_flights.csv}"
done