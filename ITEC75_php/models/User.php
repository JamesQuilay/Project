<?php
class User
{
    private $db;

    // Constructor to initialize database connection
    public function __construct($db)
    {
        $this->db = $db;
    }

    // Fetch user by email
    public function getUserByEmail($email)
    {
        // Prepare SQL statement to find a user by email
        $sql = "SELECT * FROM users WHERE email = :email LIMIT 1";
        $stmt = $this->db->prepare($sql);
        $stmt->bindParam(':email', $email, PDO::PARAM_STR);
        $stmt->execute();

        // Fetch and return user data as an associative array
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }

    // Store a 'Remember Me' token for a user
    public function storeRememberToken($userId, $token)
    {
        // Prepare SQL statement to update the user's remember_token
        $sql = "UPDATE users SET remember_token = :token WHERE id = :userId";
        $stmt = $this->db->prepare($sql);
        $stmt->bindParam(':token', $token, PDO::PARAM_STR);
        $stmt->bindParam(':userId', $userId, PDO::PARAM_INT);

        // Execute the query and return whether it was successful
        return $stmt->execute();
    }

    // Optional: Fetch user by Remember Me token (useful for automatic login)
    public function getUserByRememberToken($token)
    {
        // Prepare SQL statement to find a user by remember_token
        $sql = "SELECT * FROM users WHERE remember_token = :token LIMIT 1";
        $stmt = $this->db->prepare($sql);
        $stmt->bindParam(':token', $token, PDO::PARAM_STR);
        $stmt->execute();

        // Fetch and return user data
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }
}
?>
