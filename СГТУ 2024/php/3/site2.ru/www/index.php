<?php
$arr = array("a", "b", "c", array("d", "e", array("f", "g"), "h"), "i", 'k');
print_r($arr[3][1]); 
echo "<br/>";
print_r($arr[3][2][0]); 
echo "<br/>";
echo "<pre>";
print_r($arr);
echo "</pre>";

?>
