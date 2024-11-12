<?php

function registerUser($username, $password) {
    $users = file_get_contents('data/users.txt');
    $users = explode("\n", $users);
    foreach ($users as $user) {
        if (trim($user) === $username) {
            return false;
        }
    }
    $users[] = $username . ':' . md5($password);
    file_put_contents('data/users.txt', implode("\n", $users));
    return true;
}

function loginUser($username, $password) {
    $users = file_get_contents('data/users.txt');
    $users = explode("\n", $users);
    foreach ($users as $user) {
        list($user, $hash) = explode(':', $user);
        if (trim($user) === $username && md5($password) === $hash) {
            return true;
        }
    }
    return false;
}

function getUserName() {
    if (isset($_SESSION['username'])) {
        return $_SESSION['username'];
    }
    return '';
}

function isAdmin() {
    return getUserName() === 'admin';
}

function userExists($username) {
       // Подключаемся к базе данных (замените connectToDatabase() на свою функцию)
       $conn = connectToDatabase();

       // Запрос на проверку существования пользователя
       $sql = "SELECT COUNT(*) FROM users WHERE username = ?";
       $stmt = $conn->prepare($sql);
       $stmt->bind_param("s", $username);
       $stmt->execute();
       $result = $stmt->get_result();
// Fetch the row as an associative array
	$row = $result->fetch_assoc();

// Access the count value
	$count = $row['COUNT(*)'];

       $stmt->close();
       $conn->close();

       return $count > 0;
   }

function getAdminPageContent() {
    $content = "<h1>Диагностическая информация о сеансе</h1>";
    $content .= "<p>Имя сеанса: " . session_name() . "</p>";
    $content .= "<p>Идентификатор сеанса: " . session_id() . "</p>";
    $content .= "<p>Путь сохранения сеанса: " . session_save_path() . "</p>";
    $content .= "<p>Закодированный сеанс: " . session_encode() . "</p>";
    return $content;
}

?>
