<?php 
require 'include/functions.php';
session_start();
$visitedPages = isset($_COOKIE['visited_pages'. getUserName()]) ? unserialize($_COOKIE['visited_pages'. getUserName()]) : [];

// Добавляем текущую страницу в массив посещенных
$currentUrl = $_SERVER['REQUEST_URI'];
$visitedPages[] = $currentUrl;
setcookie('visited_pages'. getUserName(), serialize($visitedPages), time() + (365 * 24 * 60 * 60));
?>
<html>
<head>
    <title>О компании</title>
    <link rel="stylesheet" href="menu.css">

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
        <h2>О нас</h2>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec libero vitae augue laoreet maximus. Donec a lacus sed magna volutpat varius. Maecenas sed lectus et ipsum facilisis consectetur ac vitae enim. Vivamus lacinia, urna ac faucibus mollis, nulla lorem semper quam, sit amet tincidunt lectus ex sed libero.</p>

        <h2>Наша миссия</h2>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec libero vitae augue laoreet maximus. Donec a lacus sed magna volutpat varius. Maecenas sed lectus et ipsum facilisis consectetur ac vitae enim. Vivamus lacinia, urna ac faucibus mollis, nulla lorem semper quam, sit amet tincidunt lectus ex sed libero.</p>

        <h2>Наши ценности</h2>
        <ul>
            <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
            <li>Sed nec libero vitae augue laoreet maximus.</li>
            <li>Donec a lacus sed magna volutpat varius.</li>
            <li>Maecenas sed lectus et ipsum facilisis consectetur.</li>
        </ul>
    </div>

    <?php if (getUserName()) { ?>
        <div class="user-info">
            <p>Привет, <a href="profile.php"><?php echo getUserName(); ?></a>!</p>
            <p> <a href="logout.php">Выход</a></p>
        </div>
    <?php } ?>

</body>
</html>
