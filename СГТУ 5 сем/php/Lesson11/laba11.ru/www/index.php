<?php
session_start();
?>


<!DOCTYPE html>
<html>
<head>
  <title>Главная страница</title>
</head>
<body>
  <h1>Главная страница</h1>
	<?php
if (isset($_SESSION['login'])) {
  // Пользователь авторизован
  echo '<nav>
    <a href="index.php">Главная </a> 
    <a href="cabinet.php">Личный кабинет </a> ';
if($_SESSION['login'] == 'admin'){
    echo '<a href="users.php">Пользователи </a>';
}
    echo '<a href="logout.php">Выход</a>
  </nav>';
} else {
  // Пользователь не авторизован
  echo '<nav>
    <a href="index.php">Главная</a>
    <a href="login.php">Вход</a>
    <a href="register.php">Регистрация</a>
  </nav>';
}
?>
  <p>Добро пожаловать на главную страницу нашего сайта.</p>
</body>
</html>
