<?php
session_start();
?>

<!-- Вывод данных -->

<!DOCTYPE html>
<html>
<head>
  <title>Регистрация</title>
</head>
<body>
  <h1>Регистрация</h1>
  <nav>
    <a href="index.php">Главная</a>
    <a href="login.php">Вход</a>
    <a href="register.php">Регистрация</a>
  </nav>

  <form action="register.php" method="post" enctype="multipart/form-data">
    <label for="login">Логин:</label>
    <input type="text" name="login" id="login" required>
    <br>
    <label for="password">Пароль:</label>
    <input type="password" name="password" id="password" required>
    <br>
    <label for="name">Имя:</label>
    <input type="text" name="name" id="name" required>
    <br>
    <label for="surname">Фамилия:</label>
    <input type="text" name="surname" id="surname" required>
    <br>
    <label for="birthday">Дата рождения:</label>
    <input type="date" name="birthday" id="birthday">
    <br>
    <label for="email">Email:</label>
    <input type="email" name="email" id="email" required>
    <br>
    <label for="description">Описание:</label>
    <textarea name="description" id="description"></textarea>
    <br>
    <label for="photo">Фото:</label>
    <input type="file" name="photo" id="photo">
    <br>
    <input type="submit" value="Зарегистрироваться">
  </form>
<?php
// Обработка данных формы
if (isset($_POST['login']) && isset($_POST['password']) && isset($_POST['name']) && isset($_POST['surname']) && isset($_POST['email']) && isset($_POST['description']) && isset($_FILES['photo'])) {
  $login = $_POST['login'];
  $password = $_POST['password'];
  $name = $_POST['name'];
  $surname = $_POST['surname'];
  $email = $_POST['email'];
  $description = $_POST['description'];

  // Проверка на заполнение обязательных полей
  if (empty($login) || empty($password) || empty($name) || empty($surname) || empty($email)) {
    echo "<p>Пожалуйста, заполните все обязательные поля.</p>";
  } else {
    // Загрузка и сохранение фото
    $photo = $_FILES['photo'];
    if ($photo['error'] == 0) {
      $photoData = file_get_contents($photo['tmp_name']);
    }

    // Подключение к базе данных
    $mysqli = new mysqli("localhost", "root", "", "book");

    // Проверка на существование пользователя с таким логином
    $query = "SELECT * FROM person WHERE login = '$login'";
    $result = $mysqli->query($query);
    if ($result->num_rows > 0) {
      echo "<p>Пользователь с таким логином уже существует.</p>";
    } else {
      // Регистрация нового пользователя
      $query = "INSERT INTO person (login, password, name, surname, email, description, photo, date_create) VALUES ('$login', '$password', '$name', '$surname', '$email', '$description', '$photoData', 'NOW()')";

      $mysqli->query($query);
      header("Location: login.php");
    }
    $mysqli->close();
  }
}
?>
</body>
</html>
