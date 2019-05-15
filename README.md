# DigitalSecurityHub
INFO 441 project

# Home: https://127.0.0.1:8000/home/

# ERD
![ERD](https://github.com/vineethsai/DigitalSecurityHub/blob/master/media/Project%20ERD.png)

# API

## Signup https://127.0.0.1:8000/accounts/signup
- GET: Displays signup page
- POST: Sends in singup parameters, logs user in and redirects to signup2 (creates USER in user model)

## signup2 https://127.0.0.1:8000/accounts/signup2 (DO NOT USE THE LINK - FOLLOW PATH USING SIGNUP)
- GET: displays signup2 page, depending on user type (seller vs customer) shows different page

## vendor (internal link)
- POST: sends the required details of seller to API(creates Seller/Company entry in models)
- DELETE: Deltes the vendor from the database - can only be accessedd from user profile page

## customer (internal link)
- POST: sends the required details of seller to API(creates customer entry in models)
- DELETE: Deltes the vendor from the database - can only be accessedd from user profile page

## signin https://127.0.0.1:8000/accounts/signin
- GET: Displays login page if not logged in, else displays user profile
- POST: Sends login credentials to user and redirects to profile page of the user (diaplys user information)

## singout https://127.0.0.1:8000/accounts/signout
- GET: Signs out the user

## cart
**/**
- GET: Returns a JSON output of all items in the cart.
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
