<?php 
require 'include/functions.php';
session_start();

if (!isAdmin()) {
    header('Location: index.php');
    exit();
}

    $visitedPages = isset($_COOKIE['visited_pages'. getUserName()]) ? unserialize($_COOKIE['visited_pages'. getUserName()]) : [];

    // Добавляем текущую страницу в массив посещенных
    $currentUrl = $_SERVER['REQUEST_URI'];
    $visitedPages[] = $currentUrl;
    setcookie('visited_pages'. getUserName(), serialize($visitedPages), time() + (365 * 24 * 60 * 60));
?>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="menu.css">

    <title>Администратор</title>
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
    <li><a href="logout.php">Выход</a></li>
            <?php } ?>
            <?php if (!getUserName()) { ?>
                <li><a href="login.php">Вход</a></li>
                <li><a href="register.php">Регистрация</a></li>
            <?php } ?>
            <li><a href="products.php">Товары</a></li>
        </ul>
    </div>

    <?php if (getUserName()) { ?>
                              <div class="user-info">
                                  <p>Привет, <a href="profile.php"><?php echo getUserName(); ?></a>!</p>
                                  <p> <a href="logout.php">Выход</a></p>
                              </div>
    <?php } ?>
    <div class="content">
    <div class="container">
    <?php echo getAdminPageContent(); ?>
    </div>
    </div>
</body>
</html>
