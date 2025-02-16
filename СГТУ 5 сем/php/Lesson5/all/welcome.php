<?php
  session_start();

  // Проверка авторизации
  if (!isset($_SESSION["logged_in"]) || !$_SESSION["logged_in"]) {
    header("Location: index.html");
    exit;
  }

  echo "Добро пожаловать, " . $_SESSION["username"] . "!";
?>
