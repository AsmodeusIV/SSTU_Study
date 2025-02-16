<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.">
    <title>Генератор массива</title>
</head>
<body>

<h2>Введите параметры для создания массива:</h2>

<form action="" method="post">
    Длина массива: <input type="number" name="length"><br><br>
    Нижняя граница случайных чисел: <input type="number" name="min"><br><br>
    Верхняя граница случайных чисел: <input type="number" name ="max"><br><br>

    <input type= "submit" value= "Создать массив">
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

  echo "<h2>Созданный массив:</h2>";
	foreach ($array as $index => $value) {
    		echo $value . " ";
	}
$sum = array_sum($array); // Сумма всех элементов
$count = count($array); // Количество элементов
$average = $sum / $count; // Среднее арифметическое

echo "<br/>Среднее арифметическое: " . $average;
}
?>

</body>
</html>