<?php 
require 'include/functions.php';
session_start();

if (!getUserName()) {
    header('Location: index.php');
    exit();
}

$pageViews = isset($_SESSION['purchases_page_views1']) ? $_SESSION['purchases_page_views1'] : 0;
$_SESSION['purchases_page_views1'] = $pageViews + 1;

// Получаем информацию о кликах по кнопке из сессии
$clicks = isset($_SESSION['clicks']) ? $_SESSION['clicks'] : 0;
$clicks1 = isset($_COOKIE['total_clicks'. getUserName()]) ? $_COOKIE['total_clicks'. getUserName()] : 0;
// Обработка клика по кнопке
if (isset($_POST['click'])) {
    $clicks++;
    $clicks1++;
    $_SESSION['clicks'] = $clicks;
    setcookie('total_clicks'. getUserName(), $clicks1, time() + (365 * 24 * 60 * 60));
}

// Получаем информацию о посещенных страницах из куки
$visitedPages = isset($_COOKIE['visited_pages'. getUserName()]) ? unserialize($_COOKIE['visited_pages'. getUserName()]) : [];

// Добавляем текущую страницу в массив посещенных
$currentUrl = $_SERVER['REQUEST_URI'];
$visitedPages[] = $currentUrl;
setcookie('visited_pages'. getUserName(). getUserName(), serialize($visitedPages), time() + (365 * 24 * 60 * 60));

?>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="menu.css">

    <title>Личный кабинет</title>
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
    <p>Количество просмотров этой страницы: <?php echo $_SESSION['purchases_page_views1']; ?></p>
    <h2>Кнопка</h2>
    <form method="POST">
        <button type="submit" name="click">Нажми меня</button>
    </form>
        <h2>Посещенные страницы:</h2>
        <ul>
            <?php foreach ($visitedPages as $page) { ?>
                <li><a href="<?php echo $page; ?>"><?php echo $page; ?></a></li>
            <?php } ?>
        </ul>

            </div>
        </div>
    <?php if (getUserName()) { ?>
                              <div class="user-info">
                                  <p>Привет, <a href="profile.php"><?php echo getUserName(); ?></a>!</p>
                                  <p> <a href="logout.php">Выход</a></p>
                              </div>
    <?php } ?>

    </body>
    </html>
