<?php
$fl = isset($_GET['fl']) ? intval($_GET['fl']) : 0;
?>

<!DOCTYPE html>
<html>
<head>
    <title>����</title>
    <style>
        .upper p {
            font-size: 28px;
            text-align: center;
        }
        .start p {
            font-size: large;
        }
        .quiz-header {
            border: 5px;
            border-style: dotted;
        }
        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            margin: 20; 
        }
        footer {
            margin-top: auto;
            background-color: #f1f1f1; 
            text-align: center; 
            padding: 10px;
        }
    </style>
</head>
<body>
<header>
    <div class="upper">
        <p>����� ���������� � ��� ����!</p>
        <nav>
            <a href="https://metanit.com/php/tutorial/1.3.php">������� �� PHP</a>
        </nav>
    </div>
</header>
<br>
<main>
    <form>
        <div class="start">
            <p>������� ���� ���� � �������� PHP!</p>
        </div>
        <p>���� ���: <input type="text" name="name"></p>

        <?php
            if ($fl == 0): 
        ?>
            <p><input name="checked1" type="checkbox"> �������� �� �� ����������� � �����?</p>
        <?php
            else:
        ?> 
            <div class="quiz-header">
                <p><b>����� � ��� ���������� �������?</b></p>
                <p><input name="mood" type="radio" value="happy"> ��������</p>
                <p><input name="mood" type="radio" value="sad"> ��������</p>
            </div>

            <div class="buttons">
                <p><input name="checked2" type="checkbox"> ������ �������� ���������� �� �����?</p>
            </div>

            <label for="fruits">�������� ��� ������� �����:</label>
            <select id="fruits" name="fruits">
                <option value="apple">������</option>
                <option value="banana">�����</option>
                <option value="orange">��������</option>
            </select>

            <p><input type="submit" value="���������"></p>
    </form>

    <ul>
        <li>1. ������ 1</li>
        <li>2. ������ 2</li>
        <li>3. ������ 3</li>
        <li>4. ������ 4</li>
    </ul>
<?php endif; ?>
</main>
<footer>
    <p>������� �� ������� � ����� �����!</p>
</footer>
</body>
</html>
