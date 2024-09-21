<!DOCTYPE html>
<html>
 <body>
  <h2>¬аши данные</h2>
  <form action="welcome.php" method="POST">
   ¬ведите им€
   <input type="text" name="name" /> <br />
   ¬ведите год рождени€
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