# DigitalSecurityHub
INFO 441 project

## Setup
Download crispy from by using this command:
`pip install --upgrade django-crispy-forms`

# ERD
![ERD](https://github.com/vineethsai/DigitalSecurityHub/blob/master/media/Project%20ERD.png)

# API

## Home
https://127.0.0.1:8000/home/

## Signup 
https://127.0.0.1:8000/accounts/signup
- GET: Displays signup page
- POST: Sends in singup parameters, logs user in and redirects to signup2 (creates USER in user model)

## signup2 
https://127.0.0.1:8000/accounts/signup2 (DO NOT USE THE LINK - FOLLOW PATH USING SIGNUP)
- GET: displays signup2 page, depending on user type (seller vs customer) shows different page

## vendor 
(internal link)
- POST: sends the required details of seller to API(creates Seller/Company entry in models)
- DELETE: Deletes the vendor from the database - can only be accessed from user profile page/form provided

## customer 
(internal link)
- POST: sends the required details of seller to API(creates customer entry in models)
- DELETE: Deletes the vendor from the database - can only be accessed from user profile page/form provided

**HTML 1.x does NOT support anything but GET and POST for forms, so DELETE and PATCH will NOT work on a browser**

## signin 
https://127.0.0.1:8000/accounts/signin
- GET: Displays login page if not logged in, else displays user profile
- POST: Sends login credentials to user and redirects to profile page of the user (diaplys user information)

## singout 
https://127.0.0.1:8000/accounts/signout
- GET: Signs out the user

## cart
**/**
- GET: Returns a JSON output of all items in the cart, if user exists and has a cart
- POST: Will submit the current cart for a new order. This will not delete the current cart.
- DELETE: Will delete the specified item from the cart. Requires a JSON input with an int "product_id" specified.
```json
{
  "product_id": 1
}
```

## shop
**<int:product_id>/review**
- GET: Will render a page with all reviews for the specified product.
- POST: Will add a new review for that product. Requires a JSON input with a string "review" and int "rating" specified.
```json
{
  "review": "This was a great product!",
  "rating": 5
}
```
- DELETE: If an admin calls this then all the reviews will be deleted.

**review/<int:review_id>**
- GET: Will render the review.
- PATCH: Will edit the review. Requires a JSON input with a string "review" specified.
```json
{
  "review": "I changed my review :)."
}
```
- DELETE: If the user is the creator of the review then the message will be deleted.

## products
**/products**
- GET: Will render a list of all products (just the titles)
- POST: Allows an authorized, logged in vendor to add a new product, requires JSON input with title, description, price, stock, and whether it is currently active (true or false) in the store or not.
```json
{
  "title": "some title",
  "description": "a description",
  "price": 2.0,
  "stock": 5,
  "active": "true"
}
```
- DELETE: Allows the currently logged in vendor to delete all of their products

**/products/<int:product_id>**
- GET: Returns the information of a specific product 
- POST: Adds the current product to a cart.
- PATCH: Allows an authorized, logged in seller to edit the information of the specified product (as long as it is their product), takes json with title, description, price, stock, and active status
```json
{
  "title": "some title",
  "description": "a description",
  "price": 2.0,
  "stock": 5,
  "active": "true"
}
```
- DELETE: Allows the seller to delete just the specified item (if they own it and are logged in)

## orders
**/orders/<int:order_id>**
- GET: Returns information about the specified order in json format.  User must be logged in and it must be their order.
- DELETE: Allows the logged in user to delete/cancel their order (if it is their order)
- PATCH: Allows the logged in user to edit the order if it is their order, they can only edit the date not the price, takes a json array.
```json
{
  "order_date": "<some date>"
}
```


