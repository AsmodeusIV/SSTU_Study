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

if (!getUserName()) {
    header('Location: index.php');
    exit();
}

$pageViews = isset($_SESSION['purchases_page_views1']) ? $_SESSION['purchases_page_views1'] : 0;
$_SESSION['purchases_page_views1'] = $pageViews + 1;

// �������� ���������� � ������ �� ������ �� ������
$clicks = isset($_SESSION['clicks']) ? $_SESSION['clicks'] : 0;
$clicks1 = isset($_COOKIE['total_clicks'. getUserName()]) ? $_COOKIE['total_clicks'. getUserName()] : 0;
// ��������� ����� �� ������
if (isset($_POST['click'])) {
    $clicks++;
    $clicks1++;
    $_SESSION['clicks'] = $clicks;
    setcookie('total_clicks'. getUserName(), $clicks1, time() + (365 * 24 * 60 * 60));
}

// �������� ���������� � ���������� ��������� �� ����
$visitedPages = isset($_COOKIE['visited_pages'. getUserName()]) ? unserialize($_COOKIE['visited_pages'. getUserName()]) : array();

// ��������� ������� �������� � ������ ����������
$currentUrl = $_SERVER['REQUEST_URI'];
$visitedPages[] = $currentUrl;
setcookie('visited_pages'. getUserName(). getUserName(), serialize($visitedPages), time() + (365 * 24 * 60 * 60));

?>
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="menu.css">

    <title>������ �������</title>
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
    <p>���������� ���������� ���� ��������: <?php echo $_SESSION['purchases_page_views1']; ?></p>
    <h2>������</h2>
    <form method="POST">
        <button type="submit" name="click">����� ����</button>
    </form>
        <h2>���������� ��������:</h2>
        <ul>
            <?php foreach ($visitedPages as $page) { ?>
                <li><a href="<?php echo $page; ?>"><?php echo $page; ?></a></li>
            <?php } ?>
        </ul>

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
