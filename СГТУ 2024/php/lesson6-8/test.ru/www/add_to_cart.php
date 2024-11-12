<?php
require 'include/functions.php';

session_start();

// Проверяем, существует ли куки с корзиной
if (isset($_COOKIE['cart'.getUserName()])) {
    // Десериализуем куки в массив
    $cart = unserialize($_COOKIE['cart'.getUserName()]);
} else {
    // Если куки нет, создаем пустой массив
    $cart = array();
}

// Проверяем, был ли отправлен запрос на добавление книги в корзину
if (isset($_POST['book_id'])) {
    $book_id = $_POST['book_id'];

    // Предполагаем, что у вас есть массив с данными о книгах
    // Замените это на реальную логику получения данных о книгах
    $books = array(
                    array('name' => 'Властелин колец', 'price' => 1500, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=Властелин+Колец'),
                    array('name' => 'Гарри Поттер и Философский камень', 'price' => 800, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=Гарри+Поттер'),
                    array('name' => '1984', 'price' => 700, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=1984'),
                    array('name' => 'Игры престолов', 'price' => 1200, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=Игры+Престолов'),
                    array('name' => 'Гордость и предубеждение', 'price' => 500, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=Гордость+и+Предубеждение'),
                );

    // Добавляем книгу в корзину в конец массива
    $cart[] = $books[$book_id]; // Используем [] для добавления в конец массива

    // Сериализуем массив корзины и сохраняем в куки
    setcookie('cart'.getUserName(), serialize($cart), time() + (365 * 24 * 60 * 60));

    // Перенаправляем пользователя на страницу с корзиной
    header('Location: products.php');
    exit;
}
?>
<html>
    
</html>
