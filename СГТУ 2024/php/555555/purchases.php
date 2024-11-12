<?php 
require 'include/functions.php';
session_start();

// Получаем имя пользователя
$userName = getUserName();

// Обработка кликов
$clicks11 = isset($_SESSION['clicks222'. $userName]) ? $_SESSION['clicks222'. $userName] : 0;
$_SESSION['clicks222'. $userName] = $clicks11 + 1;
// Обработка просмотров страницы
$pageViews = isset($_SESSION['purchases_page_views']) ? $_SESSION['purchases_page_views'] : 0;
$_SESSION['purchases_page_views'] = $pageViews + 1;
$clicks = isset($_SESSION['clicks']) ? $_SESSION['clicks'] : 0;
// Обработка посещенных страниц (куки)
$visitedPages = isset($_COOKIE['visited_pages'. $userName]) ? unserialize($_COOKIE['visited_pages'. $userName]) : [];
$currentUrl = $_SERVER['REQUEST_URI'];
$visitedPages[] = $currentUrl;
setcookie('visited_pages'. $userName, serialize($visitedPages), time() + (365 * 24 * 60 * 60));

// Общее количество кликов (куки)
$totalClicks = isset($_COOKIE['total_clicks'. $userName]) ? $_COOKIE['total_clicks'. $userName] : 0;
setcookie('total_clicks'. $userName, $totalClicks, time() + (365 * 24 * 60 * 60));

// Проверяем, существует ли куки с корзиной
if (isset($_COOKIE['cart'.getUserName()])) {
    // Десериализуем куки в массив
    $cart = unserialize($_COOKIE['cart'.getUserName()]);
} else {
    // Если куки нет, создаем пустой массив
    $cart = [];
}

?>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="menu.css">
    <title>Покупки</title>
</head>
<body>
    <header>
            <h1>Книжный червь</h1>
        </header>

        <nav>
            <ul>
                <li><a href="index.php">Главное меню</a></li>
                <li><a href="about.php">О компании</a></li>
            </ul>
        </nav>
        <div class="sidebar">
            <ul>
                <?php if (getUserName()) { ?>
                    <li><a href="profile.php">Личный кабинет</a></li>
                    <li><a href="purchases.php">Покупки</a></li>
                    <?php if (isAdmin()) { ?>
                        <li><a href="admin.php">Админ</a></li>
                    <?php } ?>
    <li><a href="products.php">Товары</a></li>

    <li><a href="logout.php">Выход</a></li>

                <?php } ?>
                <?php if (!getUserName()) { ?>
                    <li><a href="login.php">Вход</a></li>
                    <li><a href="register.php">Регистрация</a></li>
                <?php } ?>
            </ul>
        </div>
        <div class="content">
            <div class="container">
    <!-- Контент страницы "Покупки" -->
    <p>Количество кликов за этот вход: <?php echo $clicks; ?></p>
    <p>Общее количество кликов за все время: <?php echo $totalClicks; ?></p>
    <p>Количество просмотров этой страницы: <?php echo $_SESSION['purchases_page_views']; ?></p>
    
    <h2>Ваша корзина:</h2>
    <?php if (empty($cart)) { ?>
        <p>Ваша корзина пуста.</p>
    <?php } else { ?>
        <ul>
            <?php foreach ($cart as $book) { ?>
                <li>
                    <img src="<?php echo $book['image']; ?>" alt="<?php echo $book['name']; ?>" width="100">
                    <h3><?php echo $book['name']; ?></h3>
                    <p>Цена: <?php echo $book['price']; ?></p>
                </li>
            <?php } ?>
        </ul>
    <?php } ?>
            </div>
        </div>
    <?php if ($userName) { ?>
        <div class="user-info">
            <p>Привет, <a href="profile.php"><?php echo $userName; ?></a>!</p>
            <p> <a href="logout.php">Выход</a></p>
        </div>
    <?php } ?>
    

</body>
</html>
