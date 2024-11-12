<!DOCTYPE html>
<html>
<head>
    <title>Главная страница</title>
</head>
<body>
    <h1>Добро пожаловать!</h1>

    <?php
        session_start();
        if (isset($_SESSION['username'])) {
            echo "<p>Привет, " . $_SESSION['username'] . "!</p>";
            echo "<a href='logout.php'>Выйти</a>";
        } else {
            echo "<a href='login.php'>Войти</a>";
            echo "<a href='register.php'>Регистрация</a>";
        }
    ?>

    <nav>
        <ul>
            <li><a href="page1.php">Страница 1</a></li>
            <li><a href="page2.php">Страница 2</a></li>
            <li><a href="page3.php">Страница 3</a></li>
        </ul>
    </nav>
</body>
</html>
