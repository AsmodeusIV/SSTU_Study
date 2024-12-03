<?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $username = $_POST["username"];
        $password = $_POST["password"];

        $users = file("users.txt");

        foreach ($users as $user) {
            $data = explode(":", trim($user));
            if ($data[0] == $username) {
                echo "Логин уже занят.";
                exit;
            }
        }

        $file = fopen("users.txt", "a");
        fwrite($file, "$username:$password\n");
        fclose($file);

        echo "Регистрация прошла успешно! <a href='login.php'>Войдите</a>";
    }
?>

<!DOCTYPE html>
<html>
<head>
    <title>Регистрация</title>
</head>
<body>
    <h1>Регистрация</h1>
    <form action="" method="post">
        <label for="username">Логин:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Пароль:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Зарегистрироваться">
    </form>
    <p>Уже зарегистрированы? <a href="login.php">Войдите</a></p>
</body>
</html>
