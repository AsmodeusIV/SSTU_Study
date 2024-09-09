<?php
$fl = isset($_GET['fl']) ? intval($_GET['fl']) : 0;
?>

<!DOCTYPE html>
<html>
<head>
    <title>Квиз</title>
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
        <p>Добро пожаловать в наш квиз!</p>
        <nav>
            <a href="https://metanit.com/php/tutorial/1.3.php">Учебник по PHP</a>
        </nav>
    </div>
</header>
<br>
<main>
    <form>
        <div class="start">
            <p>Начните свой путь в изучении PHP!</p>
        </div>
        <p>Ваше имя: <input type="text" name="name"></p>

        <?php
            if ($fl == 0): 
        ?>
            <p><input name="checked1" type="checkbox"> Согласны ли вы участвовать в квизе?</p>
        <?php
            else:
        ?> 
            <div class="quiz-header">
                <p><b>Какое у вас настроение сегодня?</b></p>
                <p><input name="mood" type="radio" value="happy"> Счастлив</p>
                <p><input name="mood" type="radio" value="sad"> Грустный</p>
            </div>

            <div class="buttons">
                <p><input name="checked2" type="checkbox"> Хотите получить результаты на почту?</p>
            </div>

            <label for="fruits">Выберите ваш любимый фрукт:</label>
            <select id="fruits" name="fruits">
                <option value="apple">Яблоко</option>
                <option value="banana">Банан</option>
                <option value="orange">Апельсин</option>
            </select>

            <p><input type="submit" value="Отправить"></p>
    </form>

    <ul>
        <li>1. Вопрос 1</li>
        <li>2. Вопрос 2</li>
        <li>3. Вопрос 3</li>
        <li>4. Вопрос 4</li>
    </ul>
<?php endif; ?>
</main>
<footer>
    <p>Спасибо за участие в нашем квизе!</p>
</footer>
</body>
</html>
