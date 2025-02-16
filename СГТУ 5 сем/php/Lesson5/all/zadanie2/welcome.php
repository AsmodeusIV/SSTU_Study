<?php
    session_start();
    if (!isset($_SESSION['logged_in']) || !$_SESSION['logged_in']) {
        header("Location: index.php");
        exit;
    }
?>

<!DOCTYPE html>
<html>
<head>
    <title>Добро пожаловать</title>
</head>
<body>
    <h1>Добро пожаловать, <?php echo $_SESSION['username']; ?>!</h1>

    <nav>
        <ul>
            <li><a href="index.php">Главная</a></li>
            <li><a href="page1.php">Страница 1</a></li>
            <li><a href="page2.php">Страница 2</a></li>
            <li><a href="page3.php">Страница 3</a></li>
        </ul>
    </nav>
</body>
</html>
