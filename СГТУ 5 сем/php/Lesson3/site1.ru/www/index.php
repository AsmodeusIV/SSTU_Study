<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.">
    <title>��������� �������</title>
</head>
<body>

<h2>������� ��������� ��� �������� �������:</h2>

<form action="" method="post">
    ����� �������: <input type="number" name="length"><br><br>
    ������ ������� ��������� �����: <input type="number" name="min"><br><br>
    ������� ������� ��������� �����: <input type="number" name ="max"><br><br>

    <input type= "submit" value= "������� ������">
</form>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
   $length = $_POST['length'];
   $min = $_POST['min'];
   $max = $_POST['max'];

   $array = array();
   for ($i=0; $i<$length; $i++) {
       $array[] = rand($min, $max);
   }

  echo "<h2>��������� ������:</h2>";
	foreach ($array as $index => $value) {
    		echo $value . " ";
	}
$sum = array_sum($array); // ����� ���� ���������
$count = count($array); // ���������� ���������
$average = $sum / $count; // ������� ��������������

echo "<br/>������� ��������������: " . $average;
}
?>

</body>
</html>