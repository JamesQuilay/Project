<?php
require_once 'config/db.php';
require_once 'controllers/HomeController.php';
require_once 'controllers/CartController.php';
require_once 'controllers/LoginController.php'; // Include LoginController

// Initialize database connection
$database = new Database();
$db = $database->getConnection();

// Handle routing
$page = isset($_GET['page']) ? $_GET['page'] : 'home';

switch ($page) {
    case 'home':
        $homeController = new HomeController($db);
        $homeController->index();
        break;

    case 'cart':
        $cartController = new CartController($db);
        if (isset($_GET['action']) && $_GET['action'] == 'add') {
            $cartController->addToCart($_GET['id']);
        } else {
            $cartController->index();
        }
        break;

    case 'login':
        $loginController = new LoginController($db);
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $loginController->login();
        } else {
            $loginController->showLoginForm(); // Add a method to show the login form if needed
        }
        break;

    case 'logout':
        $loginController = new LoginController($db);
        $loginController->logout();
        break;

    default:
        echo "Page not found.";
}
?>
