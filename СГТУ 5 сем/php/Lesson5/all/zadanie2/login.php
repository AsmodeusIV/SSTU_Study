<?php
    session_start();

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $username = $_POST["username"];
        $password = $_POST["password"];

        $users = file("users.txt");

        foreach ($users as $user) {
            $data = explode(":", trim($user));
            if ($data[0] == $username && $data[1] == $password) {
                $_SESSION["logged_in"] = true;
                $_SESSION["username"] = $username;
                header("Location: welcome.php");
                exit;
            }
        }

        echo "Неверный логин или пароль.";
    }
?>

<!DOCTYPE html>
<html>
<head>
    <title>Вход</title>
</head>
<body>
    <h1>Вход</h1>
    <form action="" method="post">
        <label for="username">Логин:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Пароль:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Войти">
    </form>
    <p>Еще не зарегистрированы? <a href="register.php">Зарегистрируйтесь</a></p>
</body>
</html>
