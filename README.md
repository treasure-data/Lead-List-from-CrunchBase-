# Lead-List-from-CrunchBase-
This script calls the CrunchBase API and finds the organizations who have up to Series B funding rounds and have a website. 
The code calls the organizations end point of the API and collects all the unique ids(uuid) listed on the page, 5000 per page. 

Each of the uuid is sent to forward to series_qualifier() function if the organization is a "company" and has a website. 
series_qualifier() calls the write_to_csv() function if the company has received upto Series B funding.

The write_to_csv() function writes name, website_url, linkedin_url, founders, category, country

The page variable has been set to 75, becasue all the data up to 75 pages has been stored in the  after filtering in master_data-master_data.csv

A total of 25,000 HTTPrequest error were excepted out all the 375,000 companies listed. 



