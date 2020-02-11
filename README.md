# Project - HaHu
### *Data analysis hobby project built on Python and SQL*

The underlying concept of the project derived from my fellow classmate and highschoolfriend (and a very promising "Pythoner") @geriski, both of us were tired of our current career path, and wished for something more promising. Data analysis was a topic of interest amongst us, we decided to start a joint hobbyproject after reading an introduction book to Python (Python Crash Course by Eric Matthews, I'm strongly recommeneding for everyone who starts without any prior programming knowledge, just like I did). The book's challenges and tasks generated significant enthusiasm towards the topic, so following @geriski's suggestion we've tried to analyze the **secondhand car market** of Hungary. 🧐

This repository is the third version of the original concept, with every version it's significantly evolved and improved, the only drawback is the 50% fall back in the number of the contributors. 😔

#### The project consists of three main phases:
- [X] 1) Collecting the data 
- [ ] 2) Descriptive Analytics
- [ ] 3) Predictive Analytics

## Phase 1 - Collecting the dataset
The desired dataset is based on the country's biggest used car offer site: [hasznaltauto.hu](https://www.hasznaltauto.hu), the key challenges were the 
* selection of advertisements 
* finding the valuable bits of information within the raw data
* storing the data efficiently and effectively

### Phase 1 - Data Download Module / Wireframe

![Data Download Module Wireframe](/phase1_data_download/phase1_data_download.png)

Dictionary for better understanding:

Phrase | Meaning
-------|--------
ResultPage | an URL that is containing the Advertisement URLs; typically 15-20 Advertisement URLs are forming one ResultSite; shorter form: ResSite, ResPage
AdvertisementURL | this URL represents a used car advertisement; this page contains all the "deal" related data of a car offer; shorter form: AdvertURL
CatalogURL | Nested URL on the Advertisement page; not obligatory to provide it when the user uploads an advertisement; additional data of a car, mostly technical and manufacturing informations are accessable via this URL

#### Phase 1 - Data Download Module / Database structure

![Database diagram](/phase1_data_download/data_structure.png)

Unique values:

Table | Unique value
----- | ------------
Advertisements | hirkod
Catalogs | catalog_url
Full_Data | hirkod


### Phase 1 - Data Download Module Wireframe

## Phase 2 - Collecting the dataset
Coming soon...
## Phase 3 - Collecting the dataset
Coming soon...
