# OCP5_OFF

## Searching some products in the Openfoodfacts base, finding some similar products to replace it, registering the results.

_the user can go back at any moment by entering "r" or "R"_  
_the user can quit at any moment by entering "q" or "Q"_

The program creates it's database.  
The program consults OpenFoodFacts' API.  
The program saves OpenFoodFacts' data in it's database.  

The program asks the user id (e-mail address).  
The user enters it's id.  

The program asks the user to choose between :   
>- 1 : search by category
>- 2 : search in registered favourites

The user enters 1 or 2  

The program checks the user's choice. If correct:   

>**- 1:**     
>>the program asks the user to choose among a list of categories.
>>the user enters the number chosen.
>>the program checks the user's choice. 
>>If correct, the program asks the user to choose among a list of products.
>>the user enters the number chosen.
>>the program checks the user's choice.
>>If correct, the program searches in the database a product with the most similar categories and a better nutriscore.
>>the program displays the substitute with it's related data 
>>(name, brand, nutriscore, description, store where to buy it, link to OFF's page, nutriscore)
>>the user can save the result in the database (enter "s" or "S")
    
>**- 2:**   
>>the program asks the user to choose among a list of categories.  
>>the user enters the number chosen.  
>>the program checks the user's choice.  
>>If correct, the program asks the user to choose among a list of products.  
>>the user enters the number chosen.  
>>the program checks the user's choice.  
>>the program displays the product's related data  
>>>(name, brand, nutriscore, description, store where to buy it, link to OFF's page, nutriscore)  
