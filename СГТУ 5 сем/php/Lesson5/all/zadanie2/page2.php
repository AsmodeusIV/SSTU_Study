<?php
    session_start();
    if (!isset($_SESSION['logged_in']) || !$_SESSION['logged_in']) {
        header("Location: index.php");
        exit;
    }

    // Чтение количества просмотров из файла
    $views = file("views.txt");
    $page2Views = isset($views[1]) ? $views[1] : 0;

    // Увеличение счетчика при нажатии на "Обновить"
    if (isset($_GET['update2'])) {
        $page2Views++;
        $views = file("views.txt");
        $views[1] = $page2Views;
        file_put_contents("views.txt", implode("\n", $views));
    }
?>

<!DOCTYPE html>
<html>
<head>
    <title>Страница 2</title>
</head>
<body>
    <h1>Страница 2</h1>

    <p>Привет, <?php echo $_SESSION['username']; ?>!</p>
    <a href='logout.php'>Выйти</a>

    <p>Количество просмотров: <?php echo $page2Views; ?></p>
    <a href="?update2=1">Обновить</a>

    <nav>
        <ul>
            <li><a href="index.php">Главная</a></li>
            <li><a href="page1.php">Страница 1</a></li>
            <li><a href="page3.php">Страница 3</a></li>
        </ul>
    </nav>
</body>
</html>
