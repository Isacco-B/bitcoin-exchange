# MigrantSchool Web application

- An online Bitcoin exchange platform created with Django. It implements authentication, automatically assigns Bitcoin values, and allows users to create buy and sell orders. Completed orders are recorded on the blockchain.


## Requirements:

- The platform must include an endpoint to manage user registration and login.

<p align="center">
    <img width="80%" src="./asset/img/login.png">
    <img width="80%" src="./asset/img/profile_detail.png">
</p>


- Automatically assign each registered user a variable amount of bitcoins between 1 and 10.

<p align="center">
    <img width="80%" src="./asset/img/homepage.png">
</p>


- Each user can publish one or more buy or sell orders for a certain amount of bitcoins at a certain price.

<p align="center">
    <img width="80%" src="./asset/img/buy_order.png">
    <img width="80%" src="./asset/img/sell_order.png">
</p>

- At the time of publication, if the buy order price is equal to or higher than the sell price of any other user, record the transaction and mark both orders as fulfilled.

<p align="center">
    <img width="80%" src="./asset/img/close_buy_order.png">
    <img width="80%" src="./asset/img/close_sell_order.png">
    <img width="80%" src="./asset/img/detail_buy_order.png">
    <img width="80%" src="./asset/img/detail_sell_order.png">
</p>

- Provide an endpoint to retrieve all active buy and sell orders.

<p align="center">
    <img width="80%" src="./asset/img/order_list.png">
</p>

- Also provide an endpoint to calculate the total profit or loss resulting from each user's transactions.

<p align="center">
    <img width="80%" src="./asset/img/profit.png">
</p>

## Deployment

To deploy this project:
- Create a Virtual Environment
- Clone the repo and install requirements.txt
- Install and run the Mongodb DB server
- Make database migrations
- > `python manage.py runserver`.
- open `http://127.0.0.1:8000/` in browser



## Skills
Django, Djongo, Mongodb, Python, HTML, CSS


## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/isacco-bertoli-10aa16252/)
<br/>
<a href="https://demo2.isaccobertoli.com/">Try Demo</a>
