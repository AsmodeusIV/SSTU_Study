<?php
session_start();

// Подключение к базе данных
$mysqli = new mysqli("localhost", "root", "", "book");
$login = $_SESSION['login'];

// Обработка отправленной формы
if (isset($_POST['name']) && isset($_POST['surname']) && isset($_POST['birthday']) && isset($_POST['email']) && isset($_POST['description'])) {
  $name = $_POST['name'];
  $surname = $_POST['surname'];
  $birthday = $_POST['birthday'];
  $email = $_POST['email'];
  $description = $_POST['description'];
$data = NULL;
if (!empty($_FILES['photo']['tmp_name'])) {
  $photo = $_FILES['photo']['tmp_name'];
  $type = $_FILES['photo']['type'];
  $data = file_get_contents($photo);
}

echo $data;
  // Обновление данных в базе данных
  $query = "UPDATE person SET photo='$data', name = '$name', surname = '$surname', birthday = '$birthday', email = '$email', description = '$description' WHERE login = '$login'";
  if ($mysqli->error) {
    echo "Ошибка: " . $mysqli->error;
}

  // Перезагрузка страницы для обновления отображаемых данных
  header("Location: cabinet.php");
}
?>

<!DOCTYPE html>
<html>
<head>
  <title>Личный кабинет</title>
</head>
<body>
  <h1>Личный кабинет</h1>
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

  <?php
  // Извлечение данных из базы данных
  $login = $_SESSION['login'];
  $query = "SELECT * FROM person WHERE login = '$login'";
  $result = $mysqli->query($query);
  $user = $result->fetch_assoc();

  // Вывод формы для редактирования данных
  ?>

  <form action="cabinet.php" method="post" enctype="multipart/form-data">
    <label for="name">Имя:</label>
    <input type="text" name="name" id="name" value="<?php echo $user['name']; ?>">
    <br>
    <label for="surname">Фамилия:</label>
    <input type="text" name="surname" id="surname" value="<?php echo $user['surname']; ?>">
    <br>
    <label for="birthday">День рождения:</label>
    <input type="date" name="birthday" id="birthday" value="<?php echo $user['birthday']; ?>">
    <br>
    <label for="email">Email:</label>
    <input type="email" name="email" id="email" value="<?php echo $user['email']; ?>">
    <br>
    <label for="description">Описание:</label>
    <textarea name="description" id="description"><?php echo $user['description']; ?></textarea>
    <br>
    <label for="photo" name="photo" id="photo">Фото:</label>
    <input type="file" name="photo" id="photo">
    <br>
    <input type="submit" value="Сохранить изменения">
  </form>
</body>
</html>