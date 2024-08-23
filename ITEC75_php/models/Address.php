<?php
require '../config/db.php';

class Address {
    private $pdo;

    public function __construct() {
        $this->pdo = (new Database())->pdo;
    }

    public function createAddress($user_id, $address_line, $city, $state, $postal_code, $country) {
        $sql = "INSERT INTO addresses (user_id, address_line, city, state, postal_code, country) VALUES (:user_id, :address_line, :city, :state, :postal_code, :country)";
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute([
            ':user_id' => $user_id,
            ':address_line' => $address_line,
            ':city' => $city,
            ':state' => $state,
            ':postal_code' => $postal_code,
            ':country' => $country
        ]);
    }
}
?>
