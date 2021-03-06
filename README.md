# skyscanner-webscraping-team

 ---

### Team Members - Daniel Lund, Faiz Meghjee, Taj Patel, Bola Fadipe

## <ins> Plan </ins>

```txt
3 Scrapers for each part of the skyscanner website: 
- Hotels
- Flights
- Car Hire

Min of 1000 Examples (1 Example == 1 Web Page)

Plan of Action for first couple of weeks: 
Get top 10 most popular destinations from hotels page (Scrape)
Scrape best rated Hotels, Flights and Car Hire for specific dates
Hotels: 15 Pages
Car Hire: 5 Pages
Flights: 10 Pages

Adjust number of pages depending on output. 
```

### <ins> TODO </ins>

- [x] (IN PROGRESS) Create initial class for scraper, including methods to bypass cookies, get list of popular destinations and also interact with search bar
- [x] Spread across different files for tidier file structure
- [x] Make scraper multithreaded using concurrent futures library (ThreadPoolExecutor)
- [ ] Create AWS RDS and EC2 instances
- [ ] Combine all four scrapers to a general scraper class, potentially using inheritance and save each xpath/id/css selector as vars in a seperate file or containerise each scraper individually and run that way to avoid race conditions with threading or other clashing features
