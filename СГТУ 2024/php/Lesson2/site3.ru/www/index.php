<!DOCTYPE html>
<html>
 <body>

 <?php
 if(isset($_POST['submit'])){
	echo "������, ".$_POST['name']."! � ����, ��� ���� ".$_POST['age']."��� .";
 } else {
 ?>
 <h2>���� ������</h2>
 <form action="" method="POST">
 ������� ��� 
 <input type="text" name="name" /> <br />
 ������� ��� ��������
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