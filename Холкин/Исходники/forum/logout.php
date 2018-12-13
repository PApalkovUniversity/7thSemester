<?php//Уничтожаем сессию
session_start();
session_unset();
session_destroy();
//Перенаправляем пользователя на index.php
header('location:index.php');
?>
