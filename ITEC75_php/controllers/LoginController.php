<?php
require_once 'models/User.php'; // Include your User model for database interaction
require_once 'utils/Session.php'; // Include session utility if you have one

// Ensure session is started
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

class LoginController
{
    private $userModel;

    public function __construct($db)
    {
        $this->userModel = new User($db);
    }

    // Handle login form submission
    public function login()
    {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            // Get input from POST request
            $email = trim($_POST['email']);
            $password = $_POST['password'];
            $remember = isset($_POST['remember']);

            // Validate inputs
            if (empty($email) || empty($password)) {
                $_SESSION['flash_messages']['danger'][] = 'Please fill in all required fields.';
                return;
            }

            // Attempt to find the user by email
            $user = $this->userModel->getUserByEmail($email);

            if ($user && password_verify($password, $user['password'])) {
                // Password is correct
                // Create session and remember user if needed
                Session::setUser($user);

                if ($remember) {
                    $this->setRememberMeToken($user['id']);
                }

                // Redirect to a protected page or homepage
                header('Location: /profile');
                exit();
            } else {
                // Invalid credentials
                $_SESSION['flash_messages']['danger'][] = 'Invalid email or password.';
            }
        }

        // Include login view if form is not submitted
        include 'views/login.php';
    }

    // Set a Remember Me token in cookies
    private function setRememberMeToken($userId)
    {
        $token = bin2hex(random_bytes(16));
        $expiry = time() + (86400 * 30); // 30 days

        // Store the token in the database for the user
        $this->userModel->storeRememberToken($userId, $token);

        // Set the token in a cookie
        setcookie('remember_token', $token, $expiry, '/', '', false, true);
    }

    // Handle logout and remove Remember Me cookie
    public function logout()
    {
        Session::destroy();
        setcookie('remember_token', '', time() - 3600, '/', '', false, true); // Delete cookie
        header('Location: /login');
        exit();
    }
    
    public function showLoginForm() {
        require 'views/login.php'; // Render the login view
    }
    
}
?>
