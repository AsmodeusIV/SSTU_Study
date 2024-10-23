<!DOCTYPE html>
<html>
<head>
<title>Проверка формы</title>
</head>
<body>

<h1>Проверка формы</h1>

<?php
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
      $surname = trim($_POST["surname"]);
      $age = trim($_POST["age"]);

     
      $is_valid_surname = true;
      $parts = explode("-", $surname); 

      foreach ($parts as $part) {
          $part = trim($part); 
          if (!ctype_alpha($part) && !mb_check_encoding($part, 'UTF-8')) { // 
              $is_valid_surname = false;
              break; 
          }
          if (!preg_match('/^[А-Яа-я\s\']+$/u', $part)) { 
              $is_valid_surname = false;
              break; 
          }
      }

     
      if (count($parts) > 2) {
          $is_valid_surname = false;
      }


      if (!is_numeric($age) || $age <= 0) {
          $is_valid_surname = false;
          echo "Неверный формат возраста. Введите число больше 0. <br>";
      }

      if (empty($surname) || empty($age)) {
          echo "Не все поля заполнены. <br>";
      }

      if ($is_valid_surname && is_numeric($age) && $age > 0) {
          echo "Введенные данные верны. <br>";
      } else {
          echo "Неверный формат фамилии. Введите русские или английские буквы, возможно с дефисом, пробелами или апострофами. <br>";
      }
  }
  ?>

<form method="post">
  Фамилия: <input type="text" name="surname" value="<?php echo $_POST['surname']; ?>"><br>
  Возраст: <input type="text" name="age" value="<?php echo $_POST['age']; ?>"><br>
  <input type="submit" value="Ok">
</form>

</body>
</html>
