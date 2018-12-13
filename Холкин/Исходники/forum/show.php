<?php
//Запуск данного скрипта без параметра show, переданного //в GET-строке, приведет к выводу разделов
require_once ('connect.php');
if (!isset($_GET['show']))
{
//Задаем SQL-запрос
$sql="SELECT id, name FROM TOPIC where kodofrazdel=0"; //Выполняем его
$data=mysql_query($sql);
//Надпись "Список разделов"
echo "<a href=none></a>";
echo "<br/><h1>Список paздeлoв</h1><br/>"; //Выводим список всех разделов
if ($_SESSION['role']=='admin') {
?>

<form action="?show=add_chapter&numrazdel=<?php echo $_GET ['numrazdel'] ; ?>" method="post">
<input type="submit" value="Создать новый раздел">
<br/>
<br/>

<?php
}
while($line=mysql_fetch_row($data))
{
?>
<table BORDER=1 cellpadding=20 width=100%>
<tr>
<td>
<?php
//Ссылка на index.php только с параметром show-topic
echo '<a href="?show=topic&numrazdel= '.$line[0] .'">'.$line[1]."</a><br/>";
if ($_SESSION['role']=='admin')
{
?>
<form action="?show=edit_chapter&numtopic=<?echo $line[0]?>"
method="post">
<input type="submit" value="Изменить название"> </form>

<form action="?show=del_chapter&numtopic=<? echo $line[0]?>" method="post">
<input type="submit" value="Удалить тему"> </form>
<?php
}
//end - if
?>
</td>
</tr> </table>
<?php
}
//Больше ничего выполнять не стоит exit;
}
// end -
if (isset($_GET['show'])) {
//Если задан параметр show, то в зависимости от него //выводим соответствующую информацию
switch ($_GET ['show'] )
{
//Если нужно вывести темы для выбранного раздела
case 'topic' :
require_once ('show_topic.php');
 break;
//Если нужно вывести сообщения для выбранной темы
case 'message':
require_once ('show_message.php'); break;
//Если нужно вывести форму создания темы
case 'add_topic' :
require_once ('show_addtopic.php'); break;
//Если нужно вывести форму редактирования темы
case 'edit_topic':
require_once('show_edittopic.php');
break;
//Если нужно удалить тему
case 'del_topic':
  require_once('show_deltopic.php');
break;

case 'add_chapter' :
require_once ('show_addchapter.php'); break;
//Если нужно вывести форму редактирования темы
case 'edit_chapter':
require_once('show_editchapter.php');
break;
//Если нужно удалить тему
case 'del_chapter':
  require_once('show_delchapter.php');
break;

//Если нужно вывести форму редактирования сообщения
case 'edit_message':
  require_once('show_editmessage.php'); break;
//Если нужно удалить сообщение
case 'del_message':
  require_once('show_delmessage.php'); break;
}
}
//end - case
?>
