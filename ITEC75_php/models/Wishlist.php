<?php
require '../config/db.php';

class Wishlist {
    private $pdo;

    public function __construct() {
        $this->pdo = (new Database())->pdo;
    }

    public function addToWishlist($user_id, $watch_id) {
        $sql = "INSERT INTO wishlist (user_id, watch_id) VALUES (:user_id, :watch_id)";
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute([
            ':user_id' => $user_id,
            ':watch_id' => $watch_id
        ]);
    }
}
?>
