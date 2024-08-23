<?php
require '../config/db.php';

class Order {
    private $pdo;

    public function __construct() {
        $this->pdo = (new Database())->pdo;
    }

    public function createOrder($user_id, $total_price, $status) {
        $sql = "INSERT INTO orders (user_id, total_price, status) VALUES (:user_id, :total_price, :status)";
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute([
            ':user_id' => $user_id,
            ':total_price' => $total_price,
            ':status' => $status
        ]);
    }
}
?>
