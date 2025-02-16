<?php 
require 'include/functions.php';
session_start();
$visitedPages = isset($_COOKIE['visited_pages'. getUserName()]) ? unserialize($_COOKIE['visited_pages'. getUserName()]) : array();

$cookie_lifetime = 10; 

if (isset($_COOKIE['auth'])) {
    // ��������� ������� �������� ����
    $cookie_creation_time = $_COOKIE['auth'];
    // ��������, ������� �� ����� ����
    if (time() - $cookie_creation_time > $cookie_lifetime) {
        // ��������������� �� �������� �����������
	session_destroy();
        header("Location: login.php");
        exit;
    }
    setcookie('auth', time(), time() + 60, '/');
} else {
    header("Location: login.php");
    exit;
}


// ��������� ������� �������� � ������ ����������
$currentUrl = $_SERVER['REQUEST_URI'];
$visitedPages[] = $currentUrl;
setcookie('visited_pages'. getUserName(), serialize($visitedPages), time() + (365 * 24 * 60 * 60));
?>
<html>
<head>
    <title>� ��������</title>
    <link rel="stylesheet" href="menu.css">
    <style>
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* ���������� ����� */
            gap: 20px; /* ���������� ����� ���������� */
        }

        .book {
            border: 1px solid #ddd;
            padding: 15px;
            text-align: center;
        }

        .book img {
            max-width: 100%;
            height: auto;
            margin-bottom: 10px;
        }

        .container h2 { /* ����� ��� ��������� "������" */
            margin-bottom: 20px; /* ������ ����� */
            grid-column: span 1; /* ��������� �������� ���� ������� */
        }
    </style>
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
                <h2>������</h2>
                <?php
                // ���������� ������� ������� � ����������� �������
                $books = array(
                    array('name' => '��������� �����', 'price' => 1500, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=���������+�����'),
                    array('name' => '����� ������ � ����������� ������', 'price' => 800, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=�����+������'),
                    array('name' => '1984', 'price' => 700, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=1984'),
                    array('name' => '���� ���������', 'price' => 1200, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=����+���������'),
                    array('name' => '�������� � �������������', 'price' => 500, 'image' => 'https://placehold.co/300x400/ccc/000.png?text=��������+�+�������������'),
                );

                // ����������� ������ 5 ����
                for ($i = 0; $i < 5; $i++) {
                    ?>
                    <div class="book">
                        <img src="<?php echo $books[$i]['image']; ?>" alt="<?php echo $books[$i]['name']; ?>">
                        <h3><?php echo $books[$i]['name']; ?></h3>
                        <p>����: <?php echo $books[$i]['price']; ?> ���.</p>
                        <form method="post" action="add_to_cart.php">
                            <input type="hidden" name="book_id" value="<?php echo $i; ?>"> 
                            <button type="submit">������</button>
                        </form>
                    </div>
                    <?php
                }
                ?>
            </div>
        </div>

    <?php if (getUserName()) { ?>
        <div class="user-info">
            <p>������, <a href="profile.php"><?php echo getUserName(); ?></a>!</p>
                        <p> <a href="logout.php">�����</a></p>
                    </div>
                <?php } ?>

            </body>
            </html>
