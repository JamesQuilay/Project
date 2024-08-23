<?php
require_once '../models/Cart.php';
require_once '../models/Watch.php'; // Correct model name

class CartController {
    private $cart;
    private $watchModel; // Change from Product to Watch

    public function __construct($db) {
        // Initialize Cart object and pass necessary arguments if needed
        $this->cart = new Cart($db); // Pass the $db argument if required in Cart class constructor
        $this->watchModel = new Watch(); // Initialize the Watch model
    }

    // Add a product to the cart
    public function addToCart($productId) {
        $this->cart->addToCart($productId); // Ensure this method exists in Cart class
        $this->index(); // Reload the cart page after adding
    }

    // Show the cart
    public function index() {
        $products = $this->watchModel->getAllWatches(); // Fetch all watches
        $cartItems = $this->cart->getCartItems($products); // Ensure getCartItems method exists in Cart class
        require 'templates/cart.php'; // Render cart page
    }
}

?>
