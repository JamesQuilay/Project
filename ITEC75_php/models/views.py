from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort, Response
from flask_login import login_required, current_user
from .models import User, Watch, Order, OrderItem, Watch, Cart, Address
from . import db
from sqlalchemy.sql import func
from sqlalchemy import desc
import os
from werkzeug.utils import secure_filename




views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    page = request.args.get('page', 1, type=int)  # Get the current page number, default is 1
    per_page = 8  # Number of items per page
    watches = Watch.query.paginate(page=page, per_page=per_page)

    

    cart_count = 0

    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('views.admin_overview'))
        
        cart_count = sum(item.quantity for item in current_user.cart_items)
    
    return render_template("home.html", user=current_user, cart_count=cart_count, watches=watches)

    

@views.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not authenticated'}), 401

    data = request.get_json()
    watch_id = data.get('watch_id')

    # Find the watch and add to cart
    watch = Watch.query.get(watch_id)
    if not watch:
        return jsonify({'error': 'Watch not found'}), 404

    # Check if the item already exists in the cart
    cart_item = Cart.query.filter_by(user_id=current_user.id, watch_id=watch_id).first()
    if cart_item:
        if cart_item.quantity < watch.stock_quantity:
            cart_item.quantity += 1
        else:
            return jsonify({'error': f'Cannot add more than {watch.stock_quantity} of this item'}), 400
    else:
        if watch.stock_quantity > 0:
            cart_item = Cart(user_id=current_user.id, watch_id=watch_id, quantity=1)
            db.session.add(cart_item)
        else:
            return jsonify({'error': 'This item is out of stock'}), 400

    db.session.commit()

    # Calculate the updated cart count of unique items
    unique_item_count = Cart.query.filter_by(user_id=current_user.id).count()

    return jsonify({'cart_count': unique_item_count})



@views.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.quantity * item.watch.price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


@views.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    data = request.get_json()
    cart_id = data.get('cart_id')
    action = data.get('action')
    
    cart_item = Cart.query.get(cart_id)
    if cart_item:
        if action == 'increase':
            if cart_item.quantity < cart_item.watch.stock_quantity:
                cart_item.quantity += 1
            else:
                return jsonify({'error': f'Cannot add more than {cart_item.watch.stock_quantity} of this item'}), 400
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                db.session.delete(cart_item)
        
        db.session.commit()
        
        return jsonify({'success': True})
    return jsonify({'error': 'Item not found'}), 404


@views.route('/remove_cart_item', methods=['POST'])
@login_required
def remove_cart_item():
    data = request.get_json()
    cart_id = data.get('cart_id')
    
    cart_item = Cart.query.get(cart_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Item not found'}), 404

@views.route('/cart_count', methods=['GET'])
@login_required
def cart_count():
    unique_item_count = Cart.query.filter_by(user_id=current_user.id).count()
    return jsonify({'cart_count': unique_item_count})

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'POST':
        # Retrieve the form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        address_line = request.form.get('address')  # Ensure this matches your model field
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')
        postal_code = request.form.get('postal_code')

        # Update the current_user with the new data
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email

        # Handle address updating/adding
        if current_user.addresses:
            # If the user already has an address, update it
            address = current_user.addresses[0]  # Assuming the user has only one address
            address.address_line = address_line
            address.city = city
            address.state = state
            address.country = country
            address.postal_code = postal_code
        else:
            # If the user has no address, create a new one
            new_address = Address(
                address_line=address_line,
                city=city,
                state=state,
                country=country,
                postal_code=postal_code,
                user_id=current_user.id
            )
            db.session.add(new_address)

        try:
            # Save changes to the database
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('views.user_profile'))  
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'danger')
           

    return render_template('profile.html', user=current_user, current_route='user_profile')








@views.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Validate old password and passwords match
        if not current_user.check_password(old_password):
            flash('Old password is incorrect!')
            return redirect(url_for('views.change_password'))

        if new_password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('views.change_password'))

        # Update the password
        current_user.set_password(new_password)
        # Commit changes to the database
        db.session.commit()

        flash('Password changed successfully!')
        return redirect(url_for('views.user_profile'))

    return render_template('profile.html', user=current_user, current_route='change_password')




@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        # Retrieve form data
        email_address = request.form.get('emailAddress')
        buyer_info = request.form.get('buyerInfo')
        address_line = request.form.get('address_line')
        city = request.form.get('city')
        state = request.form.get('state')
        postal_code = request.form.get('postal_code')
        country = request.form.get('country')
        payment_method = request.form.get('paymentMethod')

        # Fetch current user's cart items
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        if not cart_items:
            flash('Your cart is empty! Please add items before checkout.', 'danger')
            return redirect(url_for('views.cart'))

        # Calculate total price
        total_price = sum(item.quantity * item.watch.price for item in cart_items)

        # Check if stock is sufficient for each item
        for item in cart_items:
            if item.quantity > item.watch.stock_quantity:
                flash(f"Sorry, not enough stock for {item.watch.model_name}.", 'danger')
                return redirect(url_for('views.view_cart'))

        # Create a new order for the user
        new_order = Order(
            user_id=current_user.id,
            total_price=total_price
        )
        db.session.add(new_order)
        db.session.commit()

        # Add each item in the cart to the OrderItems table
        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                watch_id=item.watch_id,
                quantity=item.quantity,
                price_at_order=item.watch.price
            )
            db.session.add(order_item)

            # Update stock quantity for the watch
            item.watch.stock_quantity -= item.quantity

        # Commit changes to order items and stock
        db.session.commit()

        # Clear user's cart after successful order
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        # Redirect to order confirmation page
        flash('Order placed successfully!', 'success')
        return redirect(url_for('views.order_confirmation', order_id=new_order.id))

    # Fetch current user's cart items and address for displaying in checkout
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total_amount_to_pay = sum(item.quantity * item.watch.price for item in cart_items)

    # Fetch user's address
    user_address = Address.query.filter_by(user_id=current_user.id).first()
    address_values = {
        'address_line': user_address.address_line if user_address else '',
        'city': user_address.city if user_address else '',
        'state': user_address.state if user_address else '',
        'postal_code': user_address.postal_code if user_address else '',
        'country': user_address.country if user_address else '',
    }

    # Render the checkout page with cart items, total amount, and address
    return render_template('checkout.html', user=current_user, cart_items=cart_items, total_amount_to_pay=total_amount_to_pay, address_values=address_values)





@views.route('/order_confirmation/<int:order_id>', methods=['GET'])
@login_required
def order_confirmation(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    return render_template('order_confirmation.html', order=order)

@views.route('/featured')
def featured_watch():
    return render_template('featured.html')


@views.route('/product/<int:product_id>', methods=['GET'])
def product_details(product_id):
    watch = Watch.query.get_or_404(product_id)  # Fetch the product or return a 404 error
    return render_template('product_details.html', watch=watch)


@views.route('/order_status/<int:order_id>')
@login_required
def order_status(order_id):
    # Fetch the order and related data
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Fetch order items and associated watches
    order_items = OrderItem.query.filter_by(order_id=order_id).all()
    watch_items = [Watch.query.get(item.watch_id) for item in order_items]

    # Fetch user's address
    user_address = Address.query.filter_by(user_id=current_user.id).first()

    return render_template('order_status.html', order=order, order_items=order_items, watch_items=watch_items, address=user_address)











@views.route('/admin_dashboard')
@login_required
def admin_overview():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', category='error')
        return redirect(url_for('views.home'))

    # Fetch data from the database
    total_products = Watch.query.count()
    total_orders = Order.query.count()
    total_sales = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    pending_orders_count = Order.query.filter_by(status='Pending').count()

    # Fetch recent orders and users
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    # Generate additional data if needed (e.g., for charts)
    # For example, top-selling products or inventory status can be computed here

    return render_template('admin_panel.html', section='overview',
                           total_products=total_products,
                           total_orders=total_orders,
                           total_sales=total_sales,
                           pending_orders_count=pending_orders_count,
                           recent_orders=recent_orders,
                           recent_users=recent_users,
                           user=current_user)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/admin/products', methods=['GET', 'POST'])
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', category='error')
        return redirect(url_for('views.admin_products'))

    if request.method == 'POST':
        # Get form data
        model_name = request.form.get('model_name')
        price = request.form.get('price')
        stock_quantity = request.form.get('stock_quantity')
        description = request.form.get('description')
        status = request.form.get('status')

        # Validate form data
        if not model_name or not price or not stock_quantity or not description:
            flash('Please fill out all required fields.', category='error')
            return render_template('admin_panel.html', section='products', user=current_user)

        # Handle image upload
        image = request.files.get('image')
        if image and allowed_file(image.filename):
            image_binary = image.read()
        else:
            flash('Invalid image file.', category='error')
            return redirect(url_for('views.admin_products'))

        # Create new product
        new_watch = Watch(
            model_name=model_name,
            price=float(price),
            stock_quantity=int(stock_quantity),
            description=description,
            status=status,
            image=image_binary
        )

        # Add to database
        db.session.add(new_watch)
        db.session.commit()

        flash('Product added successfully!', category='success')

        # Redirect to avoid resubmission on refresh
        return redirect(url_for('views.admin_products'))

    page = request.args.get('page', 1, type=int)  # Get the current page number, default is 1
    watches = Watch.query.paginate(page=page, per_page=8)  # Limit to 8 items per page
    return render_template('admin_panel.html', section='products', user=current_user, watches=watches)


@views.route('/admin/products/delete/<int:product_id>', methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', category='error')
        return redirect(url_for('views.admin_products'))

    product = Watch.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', category='success')
    else:
        flash('Product not found.', category='error')

    return redirect(url_for('views.admin_products'))


@views.route('/admin/products/edit/<int:product_id>', methods=['POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', category='error')
        return redirect(url_for('views.admin_products'))

    product = Watch.query.get(product_id)
    if product:
        # Update product details
        product.model_name = request.form.get('model_name')
        product.price = float(request.form.get('price'))
        product.stock_quantity = int(request.form.get('stock_quantity'))
        product.description = request.form.get('description')
        product.status = request.form.get('status')

        # Handle image upload
        image = request.files.get('image')
        if image and allowed_file(image.filename):
            new_image_binary = image.read()
            product.image = new_image_binary
        
        try:
            db.session.commit()
            flash('Product updated successfully!', category='success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {str(e)}', category='error')
    else:
        flash('Product not found.', category='error')

    return redirect(url_for('views.admin_products'))



@views.route('/product_image/<int:product_id>')
def product_image(product_id):
    product = Watch.query.get_or_404(product_id)
    if product and product.image:
        return Response(product.image, mimetype='image/jpeg')  # Adjust MIME type if necessary
    else:
        abort(404)







@views.route('/admin/sales')
@login_required
def admin_sales():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', category='error')
        return redirect(url_for('views.home'))
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()

    if request.method == 'POST':
        order_id = request.form.get('order_id')
        new_status = request.form.get('status')
        order = Order.query.get(order_id)
        if order:
            order.status = new_status
            db.session.commit()
            flash('Order status updated successfully!', 'success')
        else:
            flash('Order not found.', 'error')
        return redirect(url_for('views.admin_sales'))

    # Total sales and total orders
    total_sales = db.session.query(func.sum(Order.total_price)).scalar() or 0
    total_orders = Order.query.count()

    # Sales per day (for the last 7 days)
    sales_per_day = db.session.query(
        func.date(Order.created_at),
        func.sum(Order.total_price)
    ).group_by(func.date(Order.created_at)).order_by(func.date(Order.created_at)).limit(7).all()

    # Top-selling products
    top_selling_products = db.session.query(
        Watch.model_name,
        func.sum(OrderItem.quantity).label('total_quantity')
    ).join(OrderItem).group_by(Watch.model_name).order_by(desc('total_quantity')).limit(5).all()

    


    return render_template('admin_panel.html', section='sales', 
                           total_sales=total_sales, total_orders=total_orders,
                           sales_per_day=sales_per_day, top_selling_products=top_selling_products,
                           user=current_user, recent_orders=recent_orders)


@views.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        return redirect(url_for('views.home'))
    
    # Fetch all users from the database
    users = User.query.all()
    return render_template('admin_panel.html', section='users', users=users, user=current_user)


@views.route('/admin/users/edit/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', category='error')
        return redirect(url_for('views.admin_users'))

    user = User.query.get(user_id)
    if user:
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.is_admin = request.form.get('is_admin') == 'True'

        db.session.commit()
        flash('User updated successfully!', category='success')
    else:
        flash('User not found.', category='error')

    return redirect(url_for('views.admin_users'))


@views.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', category='error')
        return redirect(url_for('views.admin_users'))

    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', category='success')
    else:
        flash('User not found.', category='error')

    return redirect(url_for('views.admin_users'))


@views.route('/admin/pending-orders')
@login_required
def admin_pending_orders():
    pending_orders = Order.query.filter_by(status='Pending').all()
    pending_orders_count = len(pending_orders)
    total_pending_amount = sum(order.total_price for order in pending_orders)

    return render_template(
        'admin_panel.html',
        section='pending_orders',
        user=current_user,
        orders=pending_orders,
        pending_orders_count=pending_orders_count,
        total_pending_amount=total_pending_amount
    )







