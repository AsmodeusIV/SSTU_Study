<!DOCTYPE html>
<html>
 <body>

 <?php
 if(isset($_POST['submit'])){
	echo "Привет, ".$_POST['name']."! Я знаю, что тебе ".$_POST['age']."лет .";
 } else {
 ?>
 <h2>Ваши данные</h2>
 <form action="" method="POST">
 Введите имя 
 <input type="text" name="name" /> <br />
 Введите год рождения
 <select name="age">
 <?php
 for ($i = 1990;$i <= 2025;$i++) {
  echo "<option value=\"$i\">$i</option>";
 }
 ?>
 </select> <br />
 <input type="submit" name="submit" value="OK" />
 </form>
 <?php } ?>
 </body>
</html>