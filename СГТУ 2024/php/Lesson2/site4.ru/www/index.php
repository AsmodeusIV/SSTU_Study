<!DOCTYPE html>
<html>
<body>
<h2>Ваши данные</h2>

<form action="" method="POST">
 Введите имя
 <input type="text" name="name" value="<?= $_POST['name']; ?>" /> <br />
 Введите год рождения
 <select name="age">
 <?php
 for ($i = 1990; $i <= 2025; $i++) {
     $selected = "";
     if(isset($_POST['age']) && $_POST['age'] == $i) {
         $selected = "selected";
     }
     echo "<option value=\"$i\" $selected>$i</option>";
 }
 ?>
 </select> <br />
<input type="submit" name="submit" value="OK" />
</form>
<br />
<?php
if(isset($_POST['submit'])){
 echo "Привет, ".$_POST['name']."! Я знаю, что тебе ".$_POST['age']." лет .";
}
?>
</body>
</html>