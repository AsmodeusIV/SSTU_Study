<?php
  session_start(); // Инициализация сессии

  // Проверка, был ли отправлен запрос
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    // Чтение данных из файла
    $users = file("users.txt");

    // Проверка на существование пользователя
    foreach ($users as $user) {
      $data = explode(":", trim($user));
      if ($data[0] == $username && $data[1] == $password) {
        $_SESSION["logged_in"] = true;
        $_SESSION["username"] = $username;
        header("Location: welcome.php");
        exit;
      }
    }

    // Пользователь не найден
    echo "Неверный логин или пароль.";
  }
?>
<html> </html>