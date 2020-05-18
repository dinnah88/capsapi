

# Flask API Documentation
This API is a Capstone Project Submission using chinook.db data pre-processing to return subsetted data frame using Python. You may want to visit the base URL to https://dinnah-apicapstone.herokuapp.com


___
## Endpoints : 

**Annual Sales** : 
> `/sales, method = GET`    

Returning Annual Sales for each Country ordered by Country Name.

**Sales by Genre** : 

> `/country , method = GET `    

Returning List of Country, Genre, and Total Sales ordered by year Year.

**Total amount invoice by Year** : 

> `/data/get/<genre> , method = GET`  

Return Total Quantity of <genre> purchased, based on each Country.

___
## Example :

I want to know how many time Jazz music purchased for each Country

**Request** :  

Method = GET  
URL =  https://dinnah-apicapstone.herokuapp.com/data/get/Jazz

**Response** : 
```json
{"genre":{"11":"Jazz","59":"Jazz","131":"Jazz","179":"Jazz","227":"Jazz","251":"Jazz","275":"Jazz","323":"Jazz","347":"Jazz","443":"Jazz","467":"Jazz","491":"Jazz","515":"Jazz","539":"Jazz","563":"Jazz"},"Country":{"11":"Argentina","59":"Austria","131":"Canada","179":"Czech Republic","227":"Finland","251":"France","275":"Germany","323":"India","347":"Ireland","443":"Poland","467":"Portugal","491":"Spain","515":"Sweden","539":"USA","563":"United Kingdom"},"Total_Qty":{"11":2.0,"59":2.0,"131":13.0,"179":3.0,"227":2.0,"251":11.0,"275":2.0,"323":10.0,"347":3.0,"443":1.0,"467":2.0,"491":2.0,"515":1.0,"539":22.0,"563":4.0}}
```