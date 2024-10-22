<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Анализ новостей кафедры</title>
    <style>
        .form-container {
            width: 500px; /* Ширина контейнера формы */
            margin: 0 auto; /* Центрирование контейнера */
            padding: 20px; /* Отступ вокруг элементов */
            border: 1px solid #ccc; /* Граница контейнера */
            border-radius: 5px; /* Закругленные углы */
        }

        label {
            display: block; /* Расположение меток на отдельных строках */
            margin-bottom: 5px; /* Отступ снизу */
        }

        input[type="radio"] {
            margin-right: 5px; /* Отступ справа от радиокнопки */
        }

        textarea {
            width: 100%; /* Ширина текстовой области */
            height: 100px; /* Высота текстовой области */
            padding: 10px; /* Отступ внутри текстовой области */
            border: 1px solid #ccc; /* Граница текстовой области */
            border-radius: 5px; /* Закругленные углы */
            resize: vertical; /* Возможность изменять высоту */
        }

        input[type="submit"] {
            padding: 10px 20px; /* Отступ внутри кнопки */
            background-color: #4CAF50; /* Зеленый фон */
            color: white; /* Белый цвет текста */
            border: none; /* Убирает стандартную границу */
            border-radius: 5px; /* Закругленные углы */
            cursor: pointer; /* Указатель в виде руки */
        }

        .result {
            margin-top: 20px; /* Отступ сверху */
            padding: 10px; /* Отступ вокруг текста */
            border: 1px solid #ccc; /* Граница результата */
            border-radius: 5px; /* Закругленные углы */
        }
    </style>
</head>
<body>

<div class="form-container">
    <h2>Анализ новостей кафедры</h2>
    <form method="post">
        <label>Выберите кафедру:</label><br>
        <label><input type="radio" name="department" value="ИВЧТ" <?php if(isset($_POST['department']) && $_POST['department'] == 'ИВЧТ') echo 'checked'; ?>> ИВЧТ</label><br>
        <label><input type="radio" name="department" value="ПИНЖ" <?php if(isset($_POST['department']) && $_POST['department'] == 'ПИНЖ') echo 'checked'; ?>> ПИНЖ</label><br>
        <label><input type="radio" name="department" value="ИКСП" <?php if(isset($_POST['department']) && $_POST['department'] == 'ИКСП') echo 'checked'; ?>> ИКСП</label><br>

        <label for="news">Введите новости:</label>
        <textarea id="news" name="news" placeholder="Введите новости с датами, отделённые форматом 01.01.2018"><?php echo isset($_POST['news']) ? htmlspecialchars($_POST['news']) : ''; ?></textarea><br>
        <input type="submit" value="Посмотреть"><br>
    </form>

    <?php
        $department = isset($_POST['department']) ? $_POST['department'] : '';
        $newsText = trim($_POST['news']);
        $datePattern = "/\d{2}\.\d{2}\.\d{4}/u";
        $ivchtPattern = "/ИВЧТ/u";
        $pinzhPattern = "/ПИНЖ/u";
        $ikspPattern = "/ИКСП/u";

        $newsArray = preg_split($datePattern, $newsText, -1, PREG_SPLIT_NO_EMPTY);

        $ivchtCount = 0;
        $pinzhCount = 0;
        $ikspCount = 0;
        foreach ($newsArray as $news) {
            if (preg_match($ivchtPattern, $news)) {
                $ivchtCount++;
            }
            elseif (preg_match($pinzhPattern, $news)) {
                $pinzhCount++;
            }
            elseif (preg_match($ikspPattern, $news)) {
                $ikspCount++;
            }
        }

        echo '<div class="result">';
        if ($department === "ИВЧТ") {
            echo "Количество новостей об ИВЧТ: $ivchtCount";
        } elseif ($department === "ПИНЖ") {
            echo "Количество новостей о ПИНЖ: $pinzhCount";
        } elseif ($department === "ИКСП") {
            echo "Количество новостей, связанных с ИКСП:" . ($ivchtCount + $pinzhCount + $ikspCount);
            echo "<br/>Количество новостей, только с ИКСП:" . ($ikspCount);

        } else {
            echo "Выберите кафедру для анализа.";
        }
        echo '</div>';
    
    ?>
</div>

</body>
</html>

