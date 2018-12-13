<?php
 //хостинг1
 $sqlhost="localhost";
 //имя пользователя
 $sqluser="root";
 //пароль
 $sqlpass="";
 //имя базы данных
 $db="forum";
 //Подключаемся к MySQL
mysql_connect($sqlhost, $sqluser,$sqlpass)or die("MySQL не
доступен! ".mysql_error());
//подключаемся к базе данных
 mysql_select_db($db)or die("Нет соединения с базой данных
".mysql_error());

mysql_set_charset("utf8")
 ?>
