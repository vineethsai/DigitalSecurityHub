# DigitalSecurityHub
INFO 441 project

## Setup
Download crispy from by using this command:
`pip install --upgrade django-crispy-forms`
Please, migrate before running. CERT files have been included if using runserver_plus.
runserver_plus included in INSTALLED_APPS, so please uncomment, if not installed on local machine

# ERD
![ERD](https://github.com/vineethsai/DigitalSecurityHub/blob/master/media/Project%20ERD.png)

# API

-------

## Public Django REST API
http://localhost:8000/api/?format=json

Only accepts GET request. You can do a POST request, but it might hose the Database

## Home
https://127.0.0.1:8000/home/

Renders the home page for the application.

## Signup
https://127.0.0.1:8000/accounts/signup
- GET: Displays signup page
- POST: Sends in signup parameters, logs user in and redirects to signup2 (creates USER in user model)

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

## signin
https://127.0.0.1:8000/accounts/signin
- GET: Displays login page if not logged in, else displays user profile
- POST: Sends login credentials to user and redirects to profile page of the user (diaplys user information)

## singout
https://127.0.0.1:8000/accounts/signout
- GET: Signs out the user

## contact
https://127.0.0.1:8000/contact

Submits an inquiry to the admins.

## checkout
https://127.0.0.1:8000/orders/checkout

Allows the user to checkout their cart and add to order.

## cart
Route: https://localhost:8000/cart/
**/**
- GET: Returns a JSON output of all items in the cart, if user exists and has a cart
  - Status 200: Found the cart and displayed that the cart is empty or the user's cart in JSON format.
  - Status 401: User not signed in.
  - Status 404: Could not find the user or cart.
- POST: Will submit the current cart for a new order. This will not delete the current cart.
  - Status 200: JSON output of the created order.
  - Status 401: User not signed in.
  - Status 404: Could not find the user or cart.
  - Status 500: Order or line item could not be created.
- DELETE: Will delete the specified item from the cart. Requires a JSON input with an int "product_id" specified.
  - Status 200: Successfully deleted item.
  - Status 401: User not signed in.
  - Status 404: Could not find the user, cart or specified item in cart.
  - Status 500: Could not load JSON input or failed to delete item.
  - Input example:
  ```json
  {
    "product_id": 1
  }
  ```
- Status 405: Method not allowed.

## shop
Route: https://localhost:8000/shop/
**<int:product_id>/review**
- GET: Will render a page with all reviews for the specified product.
  - Status 200: Renders a page with all the reviews for the specified product.
  - Status 404: Could not find the product
- POST: Will add a new review for that product. Requires a JSON input with a string "review" and int "rating" specified.
  - Status 200: JSON output of created review.
  - Status 401: User not logged in.
  - Status 404: Could not find the product.
  - Status 500: Failed to process JSON input or create review.
  - Input example:
  ```json
  {
    "review": "This was a great product!",
    "rating": 5
  }
  ```
- DELETE: If an admin calls this then all the reviews will be deleted.
  - Status 200: Successfully deleted all reviews for specified product.
  - Status 401: User not logged in.
  - Status 403: User is not an admin.
  - Status 404: Could not find the product.
  - Status 500: Failed to process JSON input or delete all reviews.
- Status 405: Method not allowed.

**review/<int:review_id>**
- GET: Will render the review.
  - Status 200: Renders a page showing the specified review.
  - Status 404: Review could not be found.
- PATCH: Will edit the review. Requires a JSON input with a string "review" specified.
  - Status 200: JSON output of the created review.
  - Status 403: Customer did not write this review.
  - Status 404: Review or customer could not be found.
  - Status 500: Failed to load the JSON input or create the message.
  ```json
  {
    "review": "I changed my review :)."
  }
  ```
- DELETE: If the user is the creator of the review then the message will be deleted.
  - Status 200: Message successfully deleted.
  - Status 403: Customer did not write this review.
  - Status 404: Review or customer could not be found.
  - Status 500: Failed to delete the message.
- Status 405: Method not allowed.

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
- GET: Returns the information of a specific product. Reviews can be posted and internal links are available to add to cart, review, and (if authorized) edit the product.
- POST: Adds the current product to a cart.
- PATCH: Allows an authorized, logged in seller to edit the information of the specified product (as long as it is their product), takes json with title, description, price, stock, and active status. There is a form available for this.
```json
{
  "title": "some title",
  "description": "a description",
  "price": 2.0,
  "stock": 5,
  "active": "true"
}
```
- DELETE: Allows the seller to delete just the specified item (if they own it and are logged in). There is a form available for this.

## orders
**/orders**
- GET: Renders all the users previous orders.

**/orders/checkout**
- GET: Renders the checkout page for the current items in a customer's cart.

**/orders/<int:order_id>**
- GET: Renders page with information about the specified order.  User must be logged in and it must be their order.
- DELETE: Allows the logged in user to delete/cancel their order (if it is their order)
- PATCH: Allows the logged in user to edit the order if it is their order, they can only edit the date not the price, takes a json array.
```json
{
  "order_date": "<some date>"
}
```

# Other Notes
A commit broke the database for a little bit while developing. Some of the commits have pycache files and the db as a result. This was necessary in order to fix the issue.

# If Azure is failing
For a branch that has up to date code with master just without any of the Azure deployment files. checkout `vineeth-final-3`.


