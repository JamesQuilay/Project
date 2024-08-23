<?php ob_start(); ?>

<h3>Your Cart</h3>
<?php if (!empty($cartItems)): ?>
    <table class="table">
        <thead>
            <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Price</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($cartItems as $item): ?>
            <tr>
                <td><?php echo $item['name']; ?></td>
                <td><?php echo $item['quantity']; ?></td>
                <td>$<?php echo $item['price']; ?></td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
<?php else: ?>
    <p>Your cart is empty.</p>
<?php endif; ?>

<?php $content = ob_get_clean(); ?>
<?php include 'templates/base.php'; ?>
