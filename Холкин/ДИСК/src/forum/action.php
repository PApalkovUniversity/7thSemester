<?php
//Добавление темы
if($_GET['act']=='add_topic')
{
//Обрабатываем название темы в целях безопасности
$safe_topic=mysql_escape_string($_POST['name_topic']); //SQL-запрос для добавления темы
$sSQL="INSERT INTO TOPIC SET
kodofrazdel=".$_GET['numrazdel']." ,name= '" . $safe_topic."', name_creator= '".$_SESSION['name']."', date_last_answer= '"
. date('Y-m-d')."'";
//Выполняем запрос
mysql_query($sSQL)or die (mysql_error());
//Обрабатываем текст сообщения в целях безопасности
ini_set('display_errors', 'Off');
$safe_message=mysql_escape_string($_POST['message']); //Определяем номер созданной темы
$id=mysql_insert_id();
//SQL-запрос, добавляющий сообщение для вновь созданной темы
$sSQL="INSERT INTO MESSAGE SET kodoftopic=".$id.", textmessage='".$safe_message. "',name_man='" .$_SESSION['name']
."' , date_answer= '".date ( 'Y-m-d')."'";
//Выполняем запрос
mysql_query ($sSQL) or die (mysql_error());
//Выводим надпись и ссылку на список тем для текущего раздела
echo "Тема Создана <BR>";
echo "<a href='index.php?show=topic&numrazdel= ".$_GET['numrazdel']."'>";
echo "Назад к списку тем</a>";
}
//Изменение названия темы
if($_GET['act']=='edit_topic')
{
//Обрабатываем название темы в целях безопасности
$safe_topic=mysql_escape_string($_POST['name_topic']); //SQL-запрос, который изменит название темы
$sSQL="UPDATE TOPIC SET name='".$safe_topic."'
WHERE id=".$_GET['numtopic'];
//Выполняем запрос
mysql_query($sSQL)or die(mysql_error()) ;
//Выбираем код раздела, чтобы можно было перенаправить //пользователя на список тем для этого раздела
$sSQL="SELECT kodofrazdel FROM TOPIC
WHERE id=".$_GET['numtopic'];
//Выполняем запрос
$data=mysql_query($sSQL);
//Получаем результат - одна запись
$line=mysql_fetch_row($data);
//Выводим надпись и ссылку на список тем для текущего раздела echo "Название темы изменено<BR>";
echo "<a href='index.php?show=topic&numrazdel=$line[0]'>"; echo "Назад к списку тем</a>";
}
//Удаление темы и всех ее сообщений

if($_GET['act'] == 'del_topic')
{
//Выбираем код раздела, чтобы можно было вернуться в него
$sSQL="SELECT kodofrazdel FROM TOPIC WHERE id=".$_GET['numtopic']; $data=mysql_query($sSQL);
//Получаем результат - одна запись
$line=mysql_fetch_row($data);
//Удаляем все сообщения для выбранной темы
$sSQL="DELETE FROM MESSAGE WHERE kodoftopic =".$_GET['numtopic'];
mysql_query($sSQL) or die (mysql_error());
//Удаляем саму тему
$sSQL="DELETE FROM TOPIC WHERE id=".$_GET['numtopic']; mysql_query($sSQL)or die(mysql_error( ));
//Выводим надпись и ссылку на список тем для текущего раздела
echo"Тема удалена<BR>";
echo "<a href='index.php?show=topic&numrazdel=$line[0]'>Назад к списку тем</a>";
}
//Добавление нового сообщения
if($_GET['act']=='add_message')
{
//Обрабатываем текст в целях безопасности
$safe_message=mysql_escape_string($_POST['message']);
//Запрос для добавления сообщения
$sSQL="INSERT INTO MESSAGE SET kodoftopic=".$_GET['numtopic'].", textmessage='" . $safe_message."' , name_man= '".$_SESSION[
'name']."' , date_answer= '" . date ('Y-m-d')."'";
//Выполняем запрос
mysql_query($sSQL) or die(mysql_error());
//Теперь добавляем информацию об имени посетителя и дате //размещаемого сообщения для темы, которой принадлежит сообщение
$sSQL="UPDATE TOPIC SET name_last_answer='". $_SESSION['name']."', date_last_answer= '".date('Y-m-d')."'WHERE id=".$_GET['numtopic']; mysql_query($sSQL) or die(mysql_error());
//Выводим надпись и ссылку на список сообщений для текущэй темы
echo"Ответ принят<BR>";
echo "<a href='index.php?show=message&numtopic= ".$_GET['numtopic']."'>";
echo"Назад к обсуждению темы</а>";
}
//Изменение сообщения
if($_GET['act']=='edit_message')
{
//Обрабатываем название в целях безопасности
$safe_message=mysql_escape_string($_POST['message']);
//Меняем текст сообщения
$sSQL="UPDATE MESSAGE SET textmessage='".$safe_message."'

WHERE id=".$_GET['nummessage'];
mysql_query($sSQL) or die(mysql_error());
//Выбираем код темы, чтобы можно было перенаправить //пользователя на список сообщений для этой темы
$sSQL="SELECT kodoftopic FROM MESSAGE WHERE
id=".$_GET['nummessage'];
$data=mysql_query($sSQL);
//Получаем результат - одна запись
$line=mysql_fetch_row($data);
//Выводим надпись и ссылку на список сообщений для текущей темы
echo"Название сообщения изменено<BR>";
echo"<a href = 'index.php?show=message&numtopic=".$line[0]."'>"; echo"Назад к обсуждению темы </a>";
}
//Удаление сообщения
if ($_GET['act']=='del_message')
{
//Выбираем код темы, чтобы можно было вернуться
//в список сообщений для нее
$sSQL="SELECT kodoftopic FROM MESSAGE
WHERE id=". $_GET['nummessage'];
$data=mysql_query($sSQL);
//Получаем результат - одна запись
$line=mysql_fetch_row($data);
//Удаляем выбранное сообщение
$sSQL="DELETE FROM MESSAGE WHERE id=".$_GET['nummessage']; //Выполняем запрос
mysql_query($sSQL)or die(mysql_error());
//Выводим -надпись и ссылку на список сообщений для текущей темы
echo"Тема удалена<BR>";
echo "<a href='index.php?show=message&numtopic=".$line[0]."'>"; echo "Назад к обсуждению темы </a>";
}
?>
