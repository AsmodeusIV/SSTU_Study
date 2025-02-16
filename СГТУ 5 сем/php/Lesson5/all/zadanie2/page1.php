<?php
    session_start();
    if (!isset($_SESSION['logged_in']) || !$_SESSION['logged_in']) {
        header("Location: index.php");
        exit;
    }

    // Чтение количества просмотров из файла
    $views = file("views.txt");
    $page1Views = isset($views[0]) ? $views[0] : 0;

    // Увеличение счетчика при нажатии на "Обновить"
    if (isset($_GET['update1'])) {
        $page1Views++;
        file_put_contents("views.txt", $page1Views . "\n");
    }
?>

<!DOCTYPE html>
<html>
<head>
    <title>Страница 1</title>
</head>
<body>
    <h1>Страница 1</h1>

    <p>Привет, <?php echo $_SESSION['username']; ?>!</p>
    <a href='logout.php'>Выйти</a>
    <p>Количество просмотров: <?php echo $page1Views; ?></p>
    <a href="?update1=1">Обновить</a>

    <nav>
        <ul>
            <li><a href="index.php">Главная</a></li>
            <li><a href="page2.php">Страница 2</a></li>
            <li><a href="page3.php">Страница 3</a></li>
        </ul>
    </nav>
</body>
</html>