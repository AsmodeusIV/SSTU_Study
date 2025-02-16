<?php
session_start();

// Удаление сессии
session_destroy();

// Перенаправление на главную страницу
header("Location: index.php");
?>