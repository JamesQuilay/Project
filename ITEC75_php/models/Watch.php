<?php
require '../config/db.php';

class Watch {
    private $pdo;

    public function __construct($db) {
        $this->pdo = $db->pdo; // Ensure $db is correctly passed to constructor
    }

    public function createWatch($model_name, $price, $description, $stock_quantity, $status, $image) {
        $sql = "INSERT INTO watches (model_name, price, description, stock_quantity, status, image) VALUES (:model_name, :price, :description, :stock_quantity, :status, :image)";
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute([
            ':model_name' => $model_name,
            ':price' => $price,
            ':description' => $description,
            ':stock_quantity' => $stock_quantity,
            ':status' => $status,
            ':image' => $image
        ]);
    }

    public function getAllWatches($page = 1, $perPage = 8) {
        $offset = ($page - 1) * $perPage;
        $stmt = $this->pdo->prepare("SELECT * FROM watches LIMIT :offset, :perPage");
        $stmt->bindParam(':offset', $offset, PDO::PARAM_INT);
        $stmt->bindParam(':perPage', $perPage, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
?>
