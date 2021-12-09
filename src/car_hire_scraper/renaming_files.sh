
cd ./Car_Hire_Data

for file in *.csv
do
  mv "$file" "${file/.csv/_carhire.csv}"
done