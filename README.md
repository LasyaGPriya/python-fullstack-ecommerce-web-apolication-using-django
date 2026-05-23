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

"C:\Users\lasya\OneDrive\Pictures\Screenshots\home page.png"

## Project Structure

- `core/` (or `ecommerce_project/`): Main Django project settings.
- `users/`: Handles custom User model and authentication flows.
- `products/`: Manages categories, products, and reviews.
- `cart/`: Handles shopping cart logic.
- `orders/`: Handles checkout, order creation, and payment simulation.
- `templates/`: Global HTML templates.
- `static/`: Global CSS, JavaScript, and image assets.
