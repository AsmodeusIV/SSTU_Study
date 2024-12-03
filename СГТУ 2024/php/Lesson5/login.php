<?php 
require 'include/functions.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    if (loginUser($username, $password)) {
        $_SESSION['username'] = $username;
        header('Location: index.php');
        exit();
    } else {
        echo "<p>Неверный логин или пароль.</p>";
    }
}

?>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="menu.css">

    <title>Вход</title>
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
                <li><a href="purchases.php">Покупки</a></li>
                <?php if (isAdmin()) { ?>
                    <li><a href="admin.php">Админ</a></li>
                <?php } ?>
            <?php } ?>
            <?php if (!getUserName()) { ?>
                <li><a href="login.php">Вход</a></li>
                <li><a href="register.php">Регистрация</a></li>
            <?php } ?>
        </ul>
    </div>
    <div class="content">
        <div class="container">
        <h2>Вход</h2>
            <form method="post">
                <label for="username">Логин:</label>
                <input type="text" id="username" name="username" required><br><br>
                <label for="password">Пароль:</label>
                <input type="password" id="password" name="password" required><br><br>
                <input type="submit" value="Вход">
            </form>
            <p>Еще нет аккаунта? <a href="register.php">Зарегистрируйтесь</a></p>
        </div>
    </div>

</body>
</html>
