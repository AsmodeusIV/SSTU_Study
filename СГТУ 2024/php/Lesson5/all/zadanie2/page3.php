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
    <title>Страница 3</title>
</head>
<body>
    <h1>Страница 3</h1>

    <p>Привет, <?php echo $_SESSION['username']; ?>!</p>
    <a href='logout.php'>Выйти</a>

    <nav>
        <ul>
            <li><a href="index.php">Главная</a></li>
            <li><a href="page1.php">Страница 1</a></li>
            <li><a href="page2.php">Страница 2</a></li>
        </ul>
    </nav>
</body>
</html>
