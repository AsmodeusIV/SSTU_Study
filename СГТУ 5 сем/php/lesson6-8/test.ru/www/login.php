<?php 
require 'include/functions.php';
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    if (loginUser($username, $password)) {
        $_SESSION['username'] = $username;
         setcookie('auth', time(), time() + 60, '/');
        header('Location: index.php');
        exit();
    } else {
        echo "<p>�������� ����� ��� ������.</p>";
    }
}

?>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="menu.css">

    <title>����</title>
</head>
<body>
    <header>
        <h1>������� �����</h1>
    </header>

    <nav>
        <ul>
            <li><a href="index.php">������� ����</a></li>
            <li><a href="about.php">� ��������</a></li>
        </ul>
    </nav>
    <div class="sidebar">
        <ul>
            <?php if (getUserName()) { ?>
                <li><a href="purchases.php">�������</a></li>
                <?php if (isAdmin()) { ?>
                    <li><a href="admin.php">�����</a></li>
                <?php } ?>
            <?php } ?>
            <?php if (!getUserName()) { ?>
                <li><a href="login.php">����</a></li>
                <li><a href="register.php">�����������</a></li>
            <?php } ?>
        </ul>
    </div>
    <div class="content">
        <div class="container">
        <h2>����</h2>
            <form method="post">
                <label for="username">�����:</label>
                <input type="text" id="username" name="username" required><br><br>
                <label for="password">������:</label>
                <input type="password" id="password" name="password" required><br><br>
                <input type="submit" value="����">
            </form>
            <p>��� ��� ��������? <a href="register.php">�����������������</a></p>
        </div>
    </div>

</body>
</html>
