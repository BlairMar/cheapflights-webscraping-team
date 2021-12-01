for file in *.csv
do
    mv "$file" "$file""_flights.csv"
done