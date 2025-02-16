<?php
require_once 'Article.php';
require_once 'Person.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Генерация форм</title>
</head>
<body>
    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $formType = $_POST['formType'];

        if ($formType === 'article') {
            $articleForm = new ArticleForm();
            $articleForm->displayForm();
        } elseif ($formType === 'person') {
            $personForm = new PersonForm();
            $personForm->displayForm();
        }
	
    }
else
{
echo '<h1>Выбор типа формы:</h1>';
        echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
        echo '<input type="radio" name="formType" value="article" id="article">';
        echo '<label for="article">Статья</label><br>';
        echo '<input type="radio" name="formType" value="person" id="person">';
        echo '<label for="person">Личность</label><br>';
        echo '<input type="submit" value="Создать форму">';
        echo '</form>';
}

    class ArticleForm {
        public function displayForm() {
            echo '<h2>Форма для статьи:</h2>';
            echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
            echo '<label for="title">Заголовок:</label><br>';
            echo '<input type="text" name="title" id="title"><br>';
            echo '<label for="author">Автор:</label><br>';
            echo '<input type="text" name="author" id="author"><br>';
            echo '<label for="description">Описание:</label><br>';
            echo '<textarea name="description" id="description"></textarea><br>';
            echo '<input type="submit" value="Создать статью">';
            echo '</form>';
        }
    }

    class PersonForm {
        public function displayForm() {
            echo '<h2>Форма для личности:</h2>';
            echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
            echo '<label for="firstName">Имя:</label><br>';
            echo '<input type="text" name="firstName" id="firstName"><br>';
            echo '<label for="lastName">Фамилия:</label><br>';
            echo '<input type="text" name="lastName" id="lastName"><br>';
            echo '<label for="email">Email:</label><br>';
            echo '<input type="email" name="email" id="email"><br>';
            echo '<input type="submit" value="Создать личность">';
            echo '</form>';
        }
    }
    ?>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (isset($_POST['title']) && isset($_POST['author']) && isset($_POST['description'])) {
            $article = new Article($_POST['title'], $_POST['author'], $_POST['description']);
            echo '<h2>Статья создана:</h2>';
            echo 'Заголовок: ' . $article->title . '<br>';
            echo 'Автор: ' . $article->author . '<br>';
            echo 'Описание: ' . $article->description . '<br>';
        } elseif (isset($_POST['firstName']) && isset($_POST['lastName']) && isset($_POST['email'])) {
            $person = new Person($_POST['firstName'], $_POST['lastName'], $_POST['email']);
            echo '<h2>Личность создана:</h2>';
            echo 'Имя: ' . $person->firstName . '<br>';
            echo 'Фамилия: ' . $person->lastName . '<br>';
            echo 'Email: ' . $person->email . '<br>';
        }
    }
    ?>
</body>
</html>
