<?php 
require './include/functions.php';
session_start();

$visitedPages = isset($_COOKIE['visited_pages'. getUserName()]) ? unserialize($_COOKIE['visited_pages'. getUserName()]) : array();

$currentUrl = $_SERVER['REQUEST_URI'];
$visitedPages[] = $currentUrl;
setcookie('visited_pages'. getUserName(), serialize($visitedPages), time() + (365 * 24 * 60 * 60));
?>

<!DOCTYPE html>
<html>
<head>
    <title>������� ��������</title>
    <link rel="stylesheet" href="menu.css">

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
                <li><a href="profile.php">������ �������</a></li>
                <li><a href="purchases.php">�������</a></li>
                <?php if (isAdmin()) { ?>
                    <li><a href="admin.php">�����</a></li>
                <?php } ?>
    <li><a href="products.php">������</a></li>

    <li><a href="logout.php">�����</a></li>

            <?php } ?>
            <?php if (!getUserName()) { ?>
                <li><a href="login.php">����</a></li>
                <li><a href="register.php">�����������</a></li>
            <?php } ?>
        </ul>
    </div>
    <div class="content">
        <div class="container">
            <h2>����� ����������!</h2>
            <p>�� ���� �������������� ��� �� ����� �����! ����� �� ������� ���������� � ����� �������, �������, ������ � ������ ������. 
               ��� ���� ������������� ������� ������ �������, ������ ���������� � ����� � ����.</p>

            <h3>���� ������</h3>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?</p>

            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
             <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
             <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
             <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </div>
    </div>
</body>
</html>
