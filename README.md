# Project - HaHu
### *Data analysis hobby project built on Python and SQL*

The underlying concept of the project derived from my fellow classmate and highschoolfriend (and a very promising "Pythoner") @geriski, both of us were tired of our current career path, and wished for something more promising. Data analysis was a topic of interest amongst us, we decided to start a joint hobbyproject after reading an introduction book to Python (Python Crash Course by Eric Matthews, I'm strongly recommeneding for everyone who starts without any prior programming knowledge, just like I did). The book's challenges and tasks generated significant enthusiasm towards the topic, so following @geriski's suggestion we've tried to analyze the **secondhand car market** of Hungary. 🧐

This repository is the third version of the original concept, with every version it's significantly evolved and improved, the only drawback is the 50% fall back in the number of the contributors. 😔

#### The project consists of four main modules:
- [X] 1) Collecting the data
- [X] 2) Updating the database
- [ ] 3) Descriptive Analytics
- [ ] 4) Predictive Analytics

## Module 1 - Collecting the dataset
The desired dataset is based on the country's biggest used car offer site: [hasznaltauto.hu](https://www.hasznaltauto.hu), the key challenges were the 
* selection of advertisements 
* finding the valuable bits of information within the raw data
* storing the data efficiently and effectively

The tasks related to the first phase were maintained and logged in [JIRA KANBAN project](https://attilakiss.atlassian.net/secure/RapidBoard.jspa?rapidView=8&projectKey=PH&selectedIssue=PH-13&atlOrigin=eyJpIjoiMzg1NDBjOTM4YWU4NDk3YWFkMDE0ZjAwOWFhZWU5NDEiLCJwIjoiaiJ9) / [JIRA cummulative report](https://attilakiss.atlassian.net/projects/PH?selectedItem=com.atlassian.jira.jira-projects-plugin%3Areport-page)

### Module 1 - Data Download Module / Process Wireframe

![Data Download Module Wireframe 1](/other_documentation/phase1/Data_download_v2_1.png)


![Data Download Module Wireframe 2](/other_documentation/phase1/Data_download_v2_2_data_downloading_and_storing.png)


Dictionary for better understanding:

Phrase | Meaning
-------|--------
ResultPage | an URL that is containing the Advertisement URLs; typically 15-20 Advertisement URLs are forming one ResultSite; shorter form: ResSite, ResPage
AdvertisementURL | this URL represents a used car advertisement; this page contains all the "deal" related data of a car offer; shorter form: AdvertURL
CatalogURL | Nested URL on the Advertisement page; not obligatory to provide it when the user uploads an advertisement; additional data of a car, mostly technical and manufacturing informations are accessable via this URL

### Module 1 - Data Download Module / Database structure

![Database diagram](/module1_data_download/data_structure.png)

Unique values:

Table | Unique value
----- | ------------
Advertisements | hirkod
Catalogs | catalog_url
Full_Data | hirkod

The database is pretty simple and straighforward, all the important data stored in two main tables. It is easy to join the Advertisements and the Catalogs on the _catalog_url_. I'm going to dedicate more focus to the queries rather than split the dataset into many tables.

The relation between the different URLs:

![URLs Relation](/module1_data_download/URLs_relation.png)

* One ResultSite contains many Advertisement URLs, so the connection is one-to-many.
* One Advertisement URL (site) contains only one (or none) Catalog URL, so the connection is one-to-one.
* In the Catalog URL's perspective the connection with the Advertisement URLs is one-to-many again.


### Module 1 - Data Download Module / 1) ResultSite gathering

* The [initial URL](https://www.hasznaltauto.hu/szemelyauto) is hardcoded into the program; 
* The algorithm uses RegEx for selecting all the URLs from the raw HTML site. 
  * If the found URL is matching with both of the keywords, the URL is a ResultSite. 
* The initial URL contains the first and the last result site as well, so the range is given. 
* The function prompts the user for the first ResultSite and the number of ResultSites for further analysis.
* The ResultSites are saved in a list.

### Module 1 - Data Download Module / 2) Advertisement URL gathering

* The program loops through the list of ResultSites, in every itteration looks for the AdvertisementURLs with a similar RegEx analysis. 
* The selected URLs are saved in a list. 
* In the next step the program request a query from the database's URLs table for the already saved AdvertisementURLs, and validating the list of the new AdvertisementURLs. 
  * The unsaved URLs are passing into the validated URLs list.


### Module 1 - Data Download Module / 3) Advertisement URL analysis

* The program loops through the list of previously validated URLs, in each itteration it is investigating an AdvertisementURLs
* In the first step of the analysis, the algorithm is using a predefined set of attributes about the Advertisement data. The scanning method based on RegEx 
* Three main categories of data is saved by this analysis: 
  * attributes of the advertisement; 
  * description (that is a freetext field, had to handled slightly differently...); 
  * CatalogURL (if found)
* The valuable data is saved in a nested dictionary 
* If any of the previously defined attributes is missing from the advertisement, the attribute is filled up with blank value

### Module 1 - Data Download Module / 4) Catalog URL analysis

The next analysis is calling the CatalogURL from the Advertisement URL analysis' result dictionary. 
* The program request a query from the database's URLs table for the already saved CatalogURLs
  * if the CatalogURL had been saved before, it skips this step. 
* The method is similar to the one that had been used in 3) step, unless it is using a different predefined set of attributes as key values for RegEx
* The valuable data is saved in a dictionary. 
* If CatalogURL could not be found in the advertisement, the CatalogURL value equals 'no_catalog', and the attributes had been filled up with blank values.

### Module 1 - Data Download Module / 5) Data Compilation and SQL commiting

In the next step the program compiles the gathered and analysed data into three dictionaries:
* AdvertisementData
* CatalogData
* URLData

Each of them is used in the corresponding SQL statement; the program commits into the tables after the carry out of any full AdvertisementURL analysis (Advertisement + Catalog). 

After a successfull commit, the algorithm selects the following AdvertisementURL from the validated advertisement list. 
If the validated advertisement list is finished, it selects the next ResultSite in order to find the AdvertisementURLs.

## Module 2 - Updating the database

Since the program does not have any direct access to the site's database, the program had been improved with an updating module, which checks the availability of the advertisements. If the URL is not reachable anymore, the program sets the sales_date to the date of connection attempt.


### Module 2 - Updating the database / Process Wireframe

![Update Module Wireframe](/module2_data_analysis/Phase2_Status_update.png)


### Module 2 - Updating the database / 1) Updating

The program requests a query for the saved AdvertisementURLs from the Advertisements Table of the database where the status of the URL is Open or NULL (NULL means it has not been evaluated yet by the perspective of sales status). In the next step it is trying to request every URL that the query resulted. 
* If the request is successfull, it sets the sales status to open; 
* If the request is not feasible, it sets the sales status to sold and the sales date to the date of the request attempt

## Module 3 - Descriptive Analytics
Soon
## Module 4 - Predictive Analytics
Soon
