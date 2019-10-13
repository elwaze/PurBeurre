# OCP5_OFF

## Searching some products in the Openfoodfacts base, finding some similar products to replace it, registering the results.

The program creates it's database.  
The program consults OpenFoodFacts' API.  
The program saves OpenFoodFacts' data in it's database.  

The program asks the user id (e-mail address).  
The user enters it's id.  

The program asks the user to choose between :   
>- 1 : search in registered favourites
>- 2 : search for a new product

The user enters 1 or 2  

The program checks the user's choice. If correct:   

>**- 2:**
>>The program asks the user to choose among a list of categories.
>>The user enters the number chosen.
>>The program checks the user's choice.
>>If correct, the program asks the user to choose among a list of products.
>>The user enters the number chosen. \n
>>The program checks the user's choice.
>>If correct, the program searches in the database a product from the same category with a better nutriscore.
>>The program displays the substitute with it's related information.
>>(name, nutriscore, store where to buy it, link to OFF's page)
>>The program asks the user if he wants to save the result in the database (o/n for yes or no).
>>If asked, the program saves the products to the users favorites in the database.
    
>**- 1:**
>>The program asks the user to choose among a list of products.
>>The user enters the number chosen.
>>The program checks the user's choice.
>>If correct, the program displays the product's saved substitute and displays its related information.
>>(name, store where to buy it, link to OFF's page, nutriscore)

The program asks the user if he wants to continue (o/n for yes or no).
If the user enters yes, the program goes back to the choice between 1 and 2.
If the user enters no, the program quits.
