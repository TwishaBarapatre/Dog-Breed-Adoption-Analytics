# 🐶 Dog Breed Adoption Analytics

## 📌 Project Overview

Dog Breed Adoption Analytics is a Data Analytics project developed to study dog adoption patterns and identify factors that influence adoption speed. The project analyzes adoption data based on breed, location, age, and size to generate meaningful insights that can help understand adoption behavior.

The project follows a complete analytics workflow including:

* Data Collection
* Data Cleaning & Feature Engineering
* Statistical Analysis
* Data Visualization using Power BI

---

## 🎯 Objectives

* Collect dog adoption data from online pet adoption platforms.
* Clean and structure raw data for analysis.
* Analyze breed-wise adoption trends.
* Analyze location-wise adoption patterns.
* Study the impact of age and size on adoption speed.
* Visualize insights through interactive dashboards.

---

## 🏗️ Project Architecture

Data Collection (Web Scraping)
↓
Raw Dataset (dogs_raw.csv)
↓
Data Cleaning & Feature Engineering
↓
Clean Dataset (dogs_cleaned.csv)
↓
Statistical Analysis
↓
Analytics Datasets
↓
Power BI Dashboard

---

## 🛠️ Technologies Used

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* Requests
* BeautifulSoup4

### Visualization

* Power BI

### Data Storage

* CSV Files

---


## 📊 Dataset Description

### dogs_raw.csv

Raw adoption data collected from online adoption platforms.

Columns:

* dog_id
* name
* breed_primary
* breed_secondary
* age
* size
* gender
* city
* state
* status
* published_at
* fetched_at

---

### dogs_cleaned.csv

Cleaned and transformed dataset.

Columns:

* dog_id
* breed
* age_group
* size
* gender
* city
* state
* days_listed
* status

---

### breed_adoption_stats.csv

Breed-wise adoption analytics.

Columns:

* breed
* total_listings
* avg_days_to_adopt
* fast_adoption_score
* slow_adoption_score

---

### location_adoption_stats.csv

Location-wise adoption analytics.

Columns:

* state
* city
* total_listings
* avg_days_listed
* fast_adoptions

---

## 🔍 Data Collection

The project uses Python-based web scraping to collect dog adoption information from Indian pet adoption platforms.

Libraries Used:

* Requests
* BeautifulSoup
* Pandas

The collected data is stored in:

```text
dogs_raw.csv
```

---

## 🧹 Data Cleaning

The raw dataset is cleaned using Pandas.

Cleaning Tasks:

* Standardize breed names
* Create age groups
* Handle missing values
* Calculate days_listed
* Standardize city and state names
* Standardize gender and size fields

Output:

```text
dogs_cleaned.csv
```

---

## 📈 Data Analysis

Analysis performed:

### Breed Analysis

* Total listings by breed
* Average adoption time
* Fast adoption score
* Slow adoption score

### Location Analysis

* Adoption trends by city
* Adoption trends by state
* Fast adoption regions

### Additional Insights

* Age group impact
* Size impact
* Gender impact

Outputs:

* breed_adoption_stats.csv
* location_adoption_stats.csv

---

## 📊 Dashboard Features

### Overview Dashboard

* Total Dogs Listed
* Average Adoption Time
* Fastest Adopted Breed
* Slowest Adopted Breed

### Breed Analytics Dashboard

* Breed-wise Adoption Trends
* Fastest and Slowest Breeds

### Location Analytics Dashboard

* State-wise Adoption Analysis
* City-wise Adoption Analysis

### Age & Size Dashboard

* Age Group Impact
* Size Impact on Adoption Speed

---

## 📷 Dashboard Screenshots

### Overview Dashboard

(Add Screenshot Here)

### Breed Analytics Dashboard

(Add Screenshot Here)

### Location Analytics Dashboard

(Add Screenshot Here)

### Age & Size Dashboard

(Add Screenshot Here)

---

## 💡 Key Insights

* Some breeds are adopted faster than others.
* Major cities show higher adoption activity.
* Puppies are generally adopted faster than adult dogs.
* Adoption trends vary across locations.
* Age and size influence adoption speed.

---

## ⚠️ Limitations

* Limited public APIs for dog adoption platforms.
* Dependence on web scraping.
* Some realistic generated data was used when real data was limited.
* Website structure changes may affect scraping.

---

## 🚀 Future Enhancements

* Real-time API integration
* Machine Learning adoption prediction
* Larger datasets from multiple adoption platforms
* Live dashboards and automated reporting

---

## 👨‍💻 Authors

### Twisha Barapatre


---

## 📜 License

This project is developed for academic and educational purposes as part of the Capstone Project for the Integrated MCA Programme at GLS University.
