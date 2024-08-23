<?php
require '../config/db.php';

class OrderItem {
    private $pdo;

    public function __construct() {
        $this->pdo = (new Database())->pdo;
    }

    public function createOrderItem($order_id, $watch_id, $quantity, $price_at_order) {
        $sql = "INSERT INTO order_items (order_id, watch_id, quantity, price_at_order) VALUES (:order_id, :watch_id, :quantity, :price_at_order)";
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute([
            ':order_id' => $order_id,
            ':watch_id' => $watch_id,
            ':quantity' => $quantity,
            ':price_at_order' => $price_at_order
        ]);
    }
}
?>
