<?php
session_start();
?>
<?php
$msg = '';
if (isset($_POST['login']) && isset($_POST['password'])) {
  $login = $_POST['login'];
  $password = $_POST['password'];
  // Подключение к базе данных
  $mysqli = new mysqli("localhost", "root", "", "book");
  // Проверка правильности введенных данных
  $query = "SELECT * FROM person WHERE login = '$login' AND password = '$password'";
  $result = $mysqli->query($query);
  if ($result->num_rows > 0) {
    $_SESSION['login'] = $login;
    header("Location: index.php");
  } else {
     $msg = "<p>Неверный логин или пароль.</p>";
  }
  $mysqli->close();
}
?>
<!-- Вывод данных -->

<!DOCTYPE html>
<html>
<head>
  <title>Вход</title>
</head>
<body>
  <h1>Вход</h1>
  <nav>
    <a href="index.php">Главная</a>
    <a href="login.php">Вход</a>
    <a href="register.php">Регистрация</a>
  </nav>

  <form action="login.php" method="post">
    <label for="login">Логин:</label>
    <input type="text" name="login" id="login">
    <br>
    <label for="password">Пароль:</label>
    <input type="password" name="password" id="password">
    <br>
    <input type="submit" value="Войти">
  </form>
<?php
echo $msg;
?>
</body>
</html>
