# Lead-List-from-CrunchBase-
This script calls the CrunchBase API and finds the organizations who have Series B funding rounds and have a website. 
The code calls the organizations end point of the API and collects all the unique ids(uuid) listed on the page, 5000 per page. 

Each of the uuid is sent to forward to series_qualifier() function if the organization is a "company" and has a website. 
series_qualifier() calls the write_to_csv() function if the company has received upto Series B funding.

The write_to_csv() function writes name, website_url, linkedin_url, founders, category, country

