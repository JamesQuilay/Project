<?php
require_once '../models/Watch.php';

class HomeController {
    private $productModel;

    public function __construct($db) {
        $this->productModel = new Watch($db);
    }

    public function index() {
        $products = $this->productModel->getAllWatches();
        require '../templates/home.php'; // Adjust path if needed
    }
}
?>
