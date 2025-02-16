<?php 
require 'include/functions.php';
session_start();

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


// �������� ��� ������������
$userName = getUserName();

// ��������� ������
$clicks11 = isset($_SESSION['clicks222'. $userName]) ? $_SESSION['clicks222'. $userName] : 0;
$_SESSION['clicks222'. $userName] = $clicks11 + 1;
// ��������� ���������� ��������
$pageViews = isset($_SESSION['purchases_page_views']) ? $_SESSION['purchases_page_views'] : 0;
$_SESSION['purchases_page_views'] = $pageViews + 1;
$clicks = isset($_SESSION['clicks']) ? $_SESSION['clicks'] : 0;
// ��������� ���������� ������� (����)
$visitedPages = isset($_COOKIE['visited_pages'. $userName]) ? unserialize($_COOKIE['visited_pages'. $userName]) : array();
$currentUrl = $_SERVER['REQUEST_URI'];
$visitedPages[] = $currentUrl;
setcookie('visited_pages'. $userName, serialize($visitedPages), time() + (365 * 24 * 60 * 60));

// ����� ���������� ������ (����)
$totalClicks = isset($_COOKIE['total_clicks'. $userName]) ? $_COOKIE['total_clicks'. $userName] : 0;
setcookie('total_clicks'. $userName, $totalClicks, time() + (365 * 24 * 60 * 60));

// ���������, ���������� �� ���� � ��������
if (isset($_COOKIE['cart'.getUserName()])) {
    // ������������� ���� � ������
    $cart = unserialize($_COOKIE['cart'.getUserName()]);
} else {
    // ���� ���� ���, ������� ������ ������
    $cart = array();
}

?>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="menu.css">
    <title>�������</title>
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
    <!-- ������� �������� "�������" -->
    <p>���������� ������ �� ���� ����: <?php echo $clicks; ?></p>
    <p>����� ���������� ������ �� ��� �����: <?php echo $totalClicks; ?></p>
    <p>���������� ���������� ���� ��������: <?php echo $_SESSION['purchases_page_views']; ?></p>
    
    <h2>���� �������:</h2>
    <?php if (empty($cart)) { ?>
        <p>���� ������� �����.</p>
    <?php } else { ?>
        <ul>
            <?php foreach ($cart as $book) { ?>
                <li>
                    <img src="<?php echo $book['image']; ?>" alt="<?php echo $book['name']; ?>" width="100">
                    <h3><?php echo $book['name']; ?></h3>
                    <p>����: <?php echo $book['price']; ?></p>
                </li>
            <?php } ?>
        </ul>
    <?php } ?>
            </div>
        </div>

    

</body>
</html>
