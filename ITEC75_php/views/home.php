<?php
// views/home.php
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <!-- Add CSS and JS links -->
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
        <div class="container">
            <ul class="nav nav-tabs justify-content-center" style="justify-content: center;">
                <?php if ($current_user && $current_user['is_authenticated']): ?>
                    <li class="nav-item">
                        <a class="nav-link" aria-current="page" href="/profile">Account: <?= $current_user['first_name'] . " " . $current_user['last_name'] ?></a>
                    </li>
                <?php else: ?>
                    <li class="nav-item">
                        <a class="nav-link" href="/login">Account: Guest</a>
                    </li>
                <?php endif; ?>
            </ul>

            <?php if ($current_user && $current_user['is_authenticated']): ?>
                <a href="/cart" class="btn btn-success">
                    <img src="../static/images/cart-fill.svg" alt="Icon" style="width: 16px; height: 16px; filter: invert(1);"> <?= $cart_count ?> Items In Your Cart
                </a>
            <?php else: ?>
                <a href="/login" class="btn btn-success">
                    <img src="../static/images/cart-fill.svg" alt="Icon" style="width: 16px; height: 16px; filter: invert(1);"> <?= $cart_count ?> Items In Your Cart
                </a>
            <?php endif; ?>
        </div>
    </nav>

    <!-- Carousel Section -->
    <!-- Convert this section similarly -->

    <!-- Categories Section -->
    <!-- Convert this section similarly -->

    <!-- Testimonials Section -->
    <!-- Convert this section similarly -->

    <!-- CTA Section -->
    <!-- Convert this section similarly -->

    <!-- Products Section -->
    <section class="blog py-5" id="shop">
        <div class="container">
            <h2 class="text-center mb-4">Our Products</h2>
            <div class="container mt-4 h-100">
                <?php if ($products): ?>
                    <div class="row">
                        <?php foreach ($products as $product): ?>
                        <!-- Product Card -->
                        <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
                            <div class="card h-100 position-relative">
                                <?php if ($product['status'] == 'Active'): ?>
                                    <div class="badge-sale">Sale</div>
                                <?php endif; ?>
                                <div class="product-image">
                                    <?php if ($product['image']): ?>
                                        <img src="../static/images/<?= $product['image'] ?>" alt="<?= $product['model_name'] ?>">
                                    <?php else: ?>
                                        <p>No Image</p>
                                    <?php endif; ?>
                                </div>
                                <div class="card-body">
                                    <h5 class="card-title"><?= $product['model_name'] ?></h5>
                                    <p class="card-text text-muted">$<?= $product['price'] ?></p>
                                    <p class="card-text small"><?= substr($product['description'], 0, 30) . '...' ?></p>
                                    <div class="star-rating">
                                        ★★★★☆ <!-- Placeholder for star rating -->
                                    </div>
                                    <div class="mt-3">
                                        <?php if ($product['status'] == 'Active'): ?>
                                            <?php if ($current_user && $current_user['is_authenticated']): ?>
                                                <button class="btn btn-primary btn-sm mb-2 add-to-cart-btn" 
                                                        data-watch-id="<?= $product['id'] ?>"
                                                        onclick="addToCart(this)">Add to Cart</button>
                                            <?php else: ?>
                                                <button class="btn btn-primary btn-sm mb-2" 
                                                        onclick="redirectToLogin()">Add to Cart</button>
                                            <?php endif; ?>
                                            <a href="product_details.php?id=<?= $product['id'] ?>" class="btn btn-secondary btn-sm mb-2">View Details</a>
                                        <?php else: ?>
                                            <a href="/login" class="btn btn-secondary btn-sm mb-2">Add to Cart</a>
                                            <a href="product_details.php?id=<?= $product['id'] ?>" class="btn btn-secondary btn-sm mb-2">View Details</a>
                                        <?php endif; ?>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <?php endforeach; ?>
                    </div>
                <?php else: ?>
                    <p>No Products Available.</p>
                <?php endif; ?>
            </div>
        </div>
    </section>

    <!-- Pagination -->
    <!-- Convert this section similarly -->

    <!-- Blog Section -->
    <!-- Convert this section similarly -->

    <!-- Newsletter Section -->
    <!-- Convert this section similarly -->

    <!-- Add necessary JavaScript for handling cart actions -->
    <script>
        function addToCart(button) {
            var watchId = button.getAttribute('data-watch-id');
            
            // Show the loading spinner
            document.getElementById('loading-spinner').style.display = 'flex';

            fetch('/add_to_cart.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ watch_id: watchId })
            })
            .then(response => response.json())
            .then(data => {
                // Hide the loading spinner
                document.getElementById('loading-spinner').style.display = 'none';
                
                if (data.error) {
                    alert(data.error);
                } else {
                    // Update the cart count on the page
                    updateCartCount(data.cart_count);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Hide the loading spinner in case of an error
                document.getElementById('loading-spinner').style.display = 'none';
            });
        }

        function updateCartCount(count) {
            var cartButton = document.querySelector('.btn-success');
            if (cartButton) {
                cartButton.innerHTML = `
                    <img src="../static/images/cart-fill.svg" alt="Icon" style="width: 16px; height: 16px; filter: invert(1);">
                    ${count} Items In Your Cart
                `;
            }
        }

        // Update cart count on page load
        document.addEventListener('DOMContentLoaded', function() {
            fetch('/get_cart_count.php')
                .then(response => response.json())
                .then(data => {
                    updateCartCount(data.cart_count);
                });
        });

        function redirectToLogin() {
            window.location.href = '/login.php';
        }
    </script>
</body>
</html>
