# DigitalSecurityHub
INFO 441 project

# ERD
![ERD][media/project\ ERD.png]

# API
## cart
*/*
- GET: Returns a JSON output of all items in the cart.
- POST: Will submit the current cart for a new order. This will not delete the current cart.
- DELETE: Will delete the specified item from the cart. Requires a JSON input with an int "product_id" specified.

## shop
*<int:product_id>/review*
- GET: Will render a page with all reviews for the specified product.
- POST: Will add a new review for that product. Requires a JSON input with a string "review" and int "rating" specified.
- DELETE: If an admin calls this then all the reviews will be deleted.

*review/<int:review_id>*
- GET: Will render the review.
- PATCH: Will edit the review. Requires a JSON input with a string "review" specified.
- DELETE: If the user is the creator of the review then the message will be deleted.
