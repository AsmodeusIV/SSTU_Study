<?php 
require 'include/functions.php';
session_start();
$visitedPages = isset($_COOKIE['visited_pages'. getUserName()]) ? unserialize($_COOKIE['visited_pages'. getUserName()]) : array();

// ��������� ������� �������� � ������ ����������
$currentUrl = $_SERVER['REQUEST_URI'];
$visitedPages[] = $currentUrl;
setcookie('visited_pages'. getUserName(), serialize($visitedPages), time() + (365 * 24 * 60 * 60));
?>
<html>
<head>
    <title>� ��������</title>
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
        <h2>� ���</h2>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec libero vitae augue laoreet maximus. Donec a lacus sed magna volutpat varius. Maecenas sed lectus et ipsum facilisis consectetur ac vitae enim. Vivamus lacinia, urna ac faucibus mollis, nulla lorem semper quam, sit amet tincidunt lectus ex sed libero.</p>

        <h2>���� ������</h2>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec libero vitae augue laoreet maximus. Donec a lacus sed magna volutpat varius. Maecenas sed lectus et ipsum facilisis consectetur ac vitae enim. Vivamus lacinia, urna ac faucibus mollis, nulla lorem semper quam, sit amet tincidunt lectus ex sed libero.</p>

        <h2>���� ��������</h2>
        <ul>
            <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
            <li>Sed nec libero vitae augue laoreet maximus.</li>
            <li>Donec a lacus sed magna volutpat varius.</li>
            <li>Maecenas sed lectus et ipsum facilisis consectetur.</li>
        </ul>
    </div>

    <?php if (getUserName()) { ?>
        <div class="user-info">
            <p>������, <a href="profile.php"><?php echo getUserName(); ?></a>!</p>
            <p> <a href="logout.php">�����</a></p>
        </div>
    <?php } ?>

</body>
</html>
