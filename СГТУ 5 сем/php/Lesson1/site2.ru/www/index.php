<?php
$fl = 1; 


if ($fl == 1) {
    $zg = "about teacher";
    $str = "Enter name";
} else {
    $zg = "For student"; 
    $str = "Enter your student code";
}
?>
<html>
<head>
<title> <?php echo $zg ?> </title>
</head>
<body>
<h2> <?php echo $zg ?></h2>
<form method="post">
<table style='background-color: #CCCC99;'>
<tr><td> <?php echo $str ?> </td> </tr>
<tr><td><input name='inform' size='10' type='text'></td></tr>
<tr><td><input type='submit' name='submit' value='OK'></td></tr>
</table>
</form>
</body>
</html>
