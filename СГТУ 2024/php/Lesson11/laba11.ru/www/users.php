<?php
session_start();
header('Content-Type: text/html; charset=utf-8');
?>

<!DOCTYPE html>
<html>
<head>
  <title>Пользователи</title>
</head>
<body>
  <h1>Пользователи</h1>
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
  if (isset($_SESSION['login']) && $_SESSION['login'] == 'admin') {
    // Подключение к базе данных
    $mysqli = new mysqli("localhost", "root", "", "book");
    // Получение списка пользователей
    $query = "SELECT * FROM person";
    $result = $mysqli->query($query);
    if ($result->num_rows > 0) {
      echo "<table>";
      echo "<tr>";
      echo "<th>ID</th>";
      echo "<th>Логин</th>";
      echo "<th>Пароль</th>";
      echo "<th>Имя</th>";
      echo "<th>Фамилия</th>";
      echo "<th>Дата рождения</th>";
      echo "<th>Email</th>";
      echo "<th>Описание</th>";
      echo "<th>Фото</th>";
      echo "<th>Дата создания</th>";
      echo "</tr>";
      while ($row = $result->fetch_assoc()) {
        echo "<tr>";
        echo "<td>" . $row['person_id'] . "</td>";
        echo "<td>" . $row['login'] . "</td>";
        echo "<td>" . $row['password'] . "</td>";
        echo "<td>" . $row['name'] . "</td>";
        echo "<td>" . $row['surname'] . "</td>";
        echo "<td>" . $row['birthday'] . "</td>";
        echo "<td>" . $row['email'] . "</td>";
        echo "<td>" . $row['description'] . "</td>";
        echo "<td>";
        if ($row['photo'] != null) {
          echo '<img src="data:image/jpeg;base64,' . base64_encode($row['photo']) . '" width="100px" height="100px">';
        }
        echo "</td>";
        echo "<td>" . $row['date_create'] . "</td>";
        echo "</tr>";
      }
      echo "</table>";
    } else {
      echo "<p>Нет зарегистрированных пользователей.</p>";
    }
    $mysqli->close();
  } else {
    //header("Location: index.php");
  }
  ?>
</body>
</html>
