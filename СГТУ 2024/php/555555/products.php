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
    <style>
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Адаптивная сетка */
            gap: 20px; /* Промежуток между элементами */
        }

        .book {
            border: 1px solid #ddd;
            padding: 15px;
            text-align: center;
        }

        .book img {
            max-width: 100%;
            height: auto;
            margin-bottom: 10px;
        }

        .container h2 { /* Стиль для заголовка "Товары" */
            margin-bottom: 20px; /* Отступ снизу */
            grid-column: span 1; /* Заголовок занимает одну колонку */
        }
    </style>
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
                <h2>Товары</h2>
                <?php
                // Заполнение массива книгами с образцовыми данными
                $books = [
                    ['name' => 'Властелин колец', 'price' => 1500, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=Властелин+Колец'],
                    ['name' => 'Гарри Поттер и Философский камень', 'price' => 800, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=Гарри+Поттер'],
                    ['name' => '1984', 'price' => 700, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=1984'],
                    ['name' => 'Игры престолов', 'price' => 1200, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=Игры+Престолов'],
                    ['name' => 'Гордость и предубеждение', 'price' => 500, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=Гордость+и+Предубеждение'],
                ];

                // Отображение первых 5 книг
                for ($i = 0; $i < 5; $i++) {
                    ?>
                    <div class="book">
                        <img src="<?php echo $books[$i]['image']; ?>" alt="<?php echo $books[$i]['name']; ?>">
                        <h3><?php echo $books[$i]['name']; ?></h3>
                        <p>Цена: <?php echo $books[$i]['price']; ?> руб.</p>
                        <form method="post" action="add_to_cart.php">
                            <input type="hidden" name="book_id" value="<?php echo $i; ?>"> 
                            <button type="submit">Купить</button>
                        </form>
                    </div>
                    <?php
                }
                ?>
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
