<?php
// Assuming you have a way to check if a user is authenticated and get user data
session_start();
$is_authenticated = isset($_SESSION['user']);
$current_user = $is_authenticated ? $_SESSION['user'] : null;
$cart_count = isset($_SESSION['cart_count']) ? $_SESSION['cart_count'] : 0;
$watches = []; // This should be populated from your database
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="../static/css/style.css">
    <!-- Add Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
  <div class="container">

    <ul class="nav nav-tabs justify-content-center" style="justify-content: center;">
      <?php if ($is_authenticated): ?>
        <li class="nav-item">
            <a class="nav-link" aria-current="page" href="/profile">Account: <?php echo htmlspecialchars($current_user['first_name'] . " " . $current_user['last_name']); ?></a>
        </li>
      <?php else: ?>
      <li class="nav-item">
        <a class="nav-link" href="/login">Account: Guest</a>
      </li>
      <?php endif; ?>
    </ul>

    <a href="<?php echo $is_authenticated ? '/cart' : '/login'; ?>" class="btn btn-success">
        <img src="../static/images/cart-fill.svg" alt="Icon" style="width: 16px; height: 16px; filter: invert(1);"> <?php echo htmlspecialchars($cart_count); ?> Items In Your Cart
    </a>
    
  </div>
</nav>

<!-- Carousel Section -->
<div id="carouselExampleCaptions" class="carousel slide" data-bs-ride="carousel">
  <div class="carousel-indicators">
    <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2" aria-label="Slide 3"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="../static/images/luxury_watch.jpg" class="d-block w-100" alt="...">
      <div class="carousel-caption d-none d-md-block">
        <h5>Luxury Watch</h5>
        <p>Discover the pinnacle of sophistication with our Luxury Watch collection. Each timepiece is crafted with meticulous attention to detail, featuring premium materials and intricate designs. Perfect for those who appreciate the finer things in life.</p>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../static/images/sport_watch.webp" class="d-block w-100" alt="...">
      <div class="carousel-caption d-none d-md-block">
        <h5>Sport Watch</h5>
        <p>Embrace your active lifestyle with our Sport Watch range. Engineered for precision and durability, these watches are perfect for athletes and adventurers alike. Built to withstand the elements and keep you on track with your goals.</p>
      </div>
    </div>
    <div class="carousel-item">
      <img src="../static/images/casual_watch.jpg" class="d-block w-100" alt="...">
      <div class="carousel-caption d-none d-md-block">
        <h5>Casual Watch</h5>
        <p> Elevate your everyday look with our Casual Watch collection. Designed for versatility and comfort, these watches seamlessly blend with your daily attire, offering both style and functionality for any occasion.</p>
      </div>
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>

<section class="categories py-5">
  <div class="container">
    <h2 class="text-center mb-4">Explore Categories</h2>
    <div class="row text-center">
      <div class="col-md-4">
        <div class="card h-100">
          <img src="../static/images/luxury_watches.jpg" class="card-img-top" alt="Luxury Watches">
          <div class="card-body">
            <h5 class="card-title">Luxury Watches</h5>
            <a href="#shop" class="btn btn-outline-primary">Shop Now</a>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card h-100">
          <img src="../static/images/sport_watches.webp" class="card-img-top" alt="Sports Watches">
          <div class="card-body">
            <h5 class="card-title">Sports Watches</h5>
            <a href="#shop" class="btn btn-outline-primary">Shop Now</a>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card h-100">
          <img src="../static/images/casual_watches.jpg" class="card-img-top" alt="Casual Watches">
          <div class="card-body">
            <h5 class="card-title">Casual Watches</h5>
            <a href="#shop" class="btn btn-outline-primary">Shop Now</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="testimonials py-5 bg-light">
  <div class="container">
    <h2 class="text-center mb-4">What Our Customers Say</h2>
    <div id="carouselTestimonials" class="carousel slide" data-mdb-ride="carousel">
      <div class="carousel-inner">
        <div class="carousel-item active">
          <div class="testimonial text-center">
            <img src="../static/images/john_doe.jpg" alt="Customer" class="rounded-circle mb-3" width="100" height="100">
            <h5 class="mb-1">John Doe</h5>
            <p class="text-muted">"Amazing collection! The watch I bought exceeded my expectations."</p>
          </div>
        </div>
        <div class="carousel-item">
          <div class="testimonial text-center">
            <img src="../static/images/jane_smith.jpg" alt="Customer" class="rounded-circle mb-3" width="100" height="100">
            <h5 class="mb-1">Jane Smith</h5>
            <p class="text-muted">"Excellent service and fast shipping. I love my new watch!"</p>
          </div>
        </div>
      </div>
      <a class="carousel-control-prev" href="#carouselTestimonials" role="button" data-mdb-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </a>
      <a class="carousel-control-next" href="#carouselTestimonials" role="button" data-mdb-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </a>
    </div>
  </div>
</section>

<section class="cta py-5 text-white text-center" style="background-color: #343a40;">
  <div class="container">
    <h2 class="mb-4">Exclusive Limited-Time Offer</h2>
    <p class="lead">Save up to 50% on select watches. Offer ends soon!</p>
    <a href="#shop" class="btn btn-warning btn-lg">Shop Now</a>
  </div>
</section>

<section class="blog py-5" id="shop">
  <div class="container">
    <h2 class="text-center mb-4">Our Products</h2>
    <div class="container mt-4 h-100">
    <?php if (!empty($watches)): ?>
      <div class="row">
        <?php foreach ($watches as $watch): ?>
        <!-- Product Card -->
        <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
            <div class="card">
                <img src="data:image/jpeg;base64,<?php echo base64_encode($watch['image']); ?>" class="card-img-top" alt="Watch Image">
                <div class="card-body">
                    <h5 class="card-title"><?php echo htmlspecialchars($watch['model_name']); ?></h5>
                    <p class="card-text">$<?php echo number_format($watch['price'], 2); ?></p>
                    <a href="/watch/<?php echo $watch['id']; ?>" class="btn btn-primary">View Details</a>
                </div>
            </div>
        </div>
        <?php endforeach; ?>
      </div>
    <?php else: ?>
      <p class="text-center">No products available at the moment.</p>
    <?php endif; ?>
    </div>
    <div class="d-flex justify-content-center mt-4">
      <a href="shop.php" class="btn btn-outline-primary">See All Products</a>
    </div>
  </div>
</section>

<!-- Add Bootstrap and MDB JS -->
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
