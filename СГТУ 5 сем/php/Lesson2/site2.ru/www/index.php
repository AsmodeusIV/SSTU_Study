<!DOCTYPE html>
<html>
 <body>
  <h2>���� ������</h2>
  <form action="welcome.php" method="POST">
   ������� ���
   <input type="text" name="name" /> <br />
   ������� ��� ��������
   <select name="age">
    <?php
    for ($i = 1990; $i <= 2025; $i++) {
        echo "<option value=\"$i\">$i</option>";
    }
    ?>
   </select> <br />
   <input type="submit" name="submit" value="OK" />
  </form>
 </body>
</html>