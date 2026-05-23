# Django eCommerce Application

A fully functional, responsive, full-stack eCommerce application built with Python and Django.

## Features

- **User Authentication**: Registration, login, logout, and profile management.
- **Product Catalog**: Product listing, category filtering, search functionality, and detailed product pages.
- **Cart System**: Add to cart, remove from cart, update quantities, dynamic total calculation.
- **Order & Checkout**: Dedicated checkout page, address form, dummy payment integration, order history.
- **Admin Panel**: Manage users, products, categories, and orders securely.
- **UI Design**: Modern, responsive UI similar to popular eCommerce platforms built using vanilla CSS.

## Reviews

- Customers can leave product reviews and star ratings on product detail pages.
- Review counts and average ratings are displayed for each product.
- Authenticated users can submit or update one review per product.

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript
- **Database**: SQLite (default)

## Setup Instructions

1. **Prerequisites**
   - Python 3.8 or higher installed on your system.

2. **Clone/Navigate to Project**
   Navigate to the project root directory where `manage.py` is located.

3. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```

4. **Activate Virtual Environment**
   - **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

5. **Install Dependencies**
   Since Pillow and Django are the only dependencies, you can install them manually or generate a `requirements.txt`:
   ```bash
   pip install django pillow
   ```

6. **Apply Migrations**
   Make sure you're in the project root directory (where manage.py is located), then run:
   ```bash
   python manage.py migrate
   ```

7. **Populate Database with Sample Data**
   Run the custom management command to add sample categories and products:
   ```bash
   python manage.py populate_db
   ```

8. **Create a Superuser (Optional)**
   To access the admin panel, create a superuser account:
   ```bash
   python manage.py createsuperuser
   ```

9. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

10. **Access the Application**
    - Store/Frontend: `http://127.0.0.1:8000/`
    - Admin Panel: `http://127.0.0.1:8000/admin/`

## Screenshots of project how its works

1.Home page

<img width="1897" height="912" alt="home page" src="https://github.com/user-attachments/assets/df60b58b-1864-4c7d-bfc3-ccedf744a542" />

2.Login Page

<img width="1897" height="911" alt="Login Page" src="https://github.com/user-attachments/assets/b277d8dc-5c1b-473b-9ef9-22348072250a" />

3.Product Detail Page
<img width="1894" height="912" alt="Product Detail Page" src="https://github.com/user-attachments/assets/f48a69a6-08bd-4d73-a9c0-293c43320c8e" />

4.Shopping Cart

<img width="1894" height="913" alt="Shopping Cart" src="https://github.com/user-attachments/assets/58e6d759-fdee-4825-9692-877f52111bdb" />


5.Shipping Address

<img width="1883" height="902" alt="Checkout Page" src="https://github.com/user-attachments/assets/08379496-e7c4-48eb-aff6-43708826539c" />


6.Oder Placed
<img width="1895" height="911" alt="Screenshot 2026-04-30 182525" src="https://github.com/user-attachments/assets/1948b9d6-a406-4bb1-a18b-444e00659e24" />


7.Order History
<img width="1886" height="909" alt="Order History" src="https://github.com/user-attachments/assets/354a037f-3e9e-480c-a23a-3a9f976c2d62" />


8.Admin Login
<img width="1901" height="968" alt="admin Login" src="https://github.com/user-attachments/assets/f86fea42-0d66-4b81-b8b7-54dc1e1f6fbc" />


9.Admin Home Page
<img width="1908" height="907" alt="Admin Home page" src="https://github.com/user-attachments/assets/0487b6a7-082f-4f95-9bd9-138f79cb8548" />


10.Updating Products
<img width="1896" height="895" alt="Updation products" src="https://github.com/user-attachments/assets/2b8d493a-fb86-47af-852f-ada0beb76aac" />


## Project Structure

- `core/` (or `ecommerce_project/`): Main Django project settings.
- `users/`: Handles custom User model and authentication flows.
- `products/`: Manages categories, products, and reviews.
- `cart/`: Handles shopping cart logic.
- `orders/`: Handles checkout, order creation, and payment simulation.
- `templates/`: Global HTML templates.
- `static/`: Global CSS, JavaScript, and image assets.
