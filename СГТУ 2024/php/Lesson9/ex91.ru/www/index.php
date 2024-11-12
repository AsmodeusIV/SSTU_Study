<?php
require_once 'Article.php';
require_once 'Person.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>��������� ����</title>
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
echo '<h1>����� ���� �����:</h1>';
        echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
        echo '<input type="radio" name="formType" value="article" id="article">';
        echo '<label for="article">������</label><br>';
        echo '<input type="radio" name="formType" value="person" id="person">';
        echo '<label for="person">��������</label><br>';
        echo '<input type="submit" value="������� �����">';
        echo '</form>';
}

    class ArticleForm {
        public function displayForm() {
            echo '<h2>����� ��� ������:</h2>';
            echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
            echo '<label for="title">���������:</label><br>';
            echo '<input type="text" name="title" id="title"><br>';
            echo '<label for="author">�����:</label><br>';
            echo '<input type="text" name="author" id="author"><br>';
            echo '<label for="description">��������:</label><br>';
            echo '<textarea name="description" id="description"></textarea><br>';
            echo '<input type="submit" value="������� ������">';
            echo '</form>';
        }
    }

    class PersonForm {
        public function displayForm() {
            echo '<h2>����� ��� ��������:</h2>';
            echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
            echo '<label for="firstName">���:</label><br>';
            echo '<input type="text" name="firstName" id="firstName"><br>';
            echo '<label for="lastName">�������:</label><br>';
            echo '<input type="text" name="lastName" id="lastName"><br>';
            echo '<label for="email">Email:</label><br>';
            echo '<input type="email" name="email" id="email"><br>';
            echo '<input type="submit" value="������� ��������">';
            echo '</form>';
        }
    }
    ?>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (isset($_POST['title']) && isset($_POST['author']) && isset($_POST['description'])) {
            $article = new Article($_POST['title'], $_POST['author'], $_POST['description']);
            echo '<h2>������ �������:</h2>';
            echo '���������: ' . $article->title . '<br>';
            echo '�����: ' . $article->author . '<br>';
            echo '��������: ' . $article->description . '<br>';
        } elseif (isset($_POST['firstName']) && isset($_POST['lastName']) && isset($_POST['email'])) {
            $person = new Person($_POST['firstName'], $_POST['lastName'], $_POST['email']);
            echo '<h2>�������� �������:</h2>';
            echo '���: ' . $person->firstName . '<br>';
            echo '�������: ' . $person->lastName . '<br>';
            echo 'Email: ' . $person->email . '<br>';
        }
    }
    ?>
</body>
</html>
