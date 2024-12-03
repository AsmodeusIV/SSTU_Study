

<?php
  // Проверка, был ли отправлен запрос
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    // Чтение данных из файла
    $users = file("users.txt");

    // Проверка на существование логина
    foreach ($users as $user) {
      $data = explode(":", trim($user));
      if ($data[0] == $username) {
        echo "Логин уже занят.";
        exit;
      }
    }

    // Добавление нового пользователя в файл
    $file = fopen("users.txt", "a");
    fwrite($file, "$username:$password\n");
    fclose($file);

    echo "Регистрация прошла успешно!";
  }
?>
