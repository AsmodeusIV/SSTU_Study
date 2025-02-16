<?php 
require 'include/functions.php';
session_start();

session_destroy();

header('Location: index.php');
exit();
?>
