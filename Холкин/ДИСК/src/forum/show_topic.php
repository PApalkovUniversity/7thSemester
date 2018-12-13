<?php
 //Задаем SQL-запрос
  $sql="SELECT id, kodofrazdel, name, name_creator, name_last_answer,
 date_last_answer FROM TOPIC WHERE kodofrazdel=".$_GET ['numrazdel']." ORDER BY date_last_answer";
//Выполняем его
  $data=mysql_query ($sql);
 //Задаем SQL-запрос, который вернет имя выбранного //пользователем раздела
  $sql2="SELECT name FROM TOPIC WHERE id=" .$_GET['numrazdel'];
 //Выполняем его
  $data2=mysql_query($sql2);
 //Получаем результат - одна запись
 $line2=mysql_fetch_row($data2);
 //Выводим надпись
 echo "<h1>Список тем для ";
 echo "раздела: ".$line2 [0] ."</h1><BR><BR>";
//Кнопка для создания новой темы
?>

<form action="?show=add_topic&numrazdel=<?php echo $_GET ['numrazdel'] ; ?>" method="post">
<input type="submit" value="Создать новую тему">
</form>
<?php
//Выводим заголовок для таблицы
?>
<table BORDER=1 cellpadding=3 width=100%>
<tr>
<td width=60%>
Название темы
</td>
<td width=10%>
<font size=2>Автор</font>
</td>
<td width=30%>
<font size=2>Последнее сообщение (Kто|Дата)</font>
</td>
</tr>
</table>
<?php
//Выводим список всех тем для выбранного раздела
while($line=mysql_fetch_row($data))
{
?>
<table BORDER=1 cellpadding=20 width=100%>
<tr>
<td width=60%>
<?php
//Это в виде ссылки, она на index.php
//только с параметром message
echo '<a href="?show=message&numtopic='.$line[0].'">' .$line[2].'</a>';
//Если это админ, то он может редактировать название темы //и удалять ее
if ($_SESSION['role']=='admin')
{
?>
<form action="?show=edit_topic&numtopic=<?echo $line[0]?>"
method="post">
<input type="submit" value="Изменить название"> </form>

<form action="?show=del_topic&numtopic=<? echo $line[0]?>" method="post">
<input type="submit" value="Удалить тему"> </form>
<?php
}
//end - if
?>
</td>
<td width=10%> <?php
//Имя создавшего тему
echo $line[3];
?>
</td>
<td width=10%>
<?php
//Имя последнего ответившего
echo $line[4];
?>
</td>
<td width=20%>
<?php
//Дата последнего ответа
echo $line[5];
?>
</td>
</tr>
</table>
<?php
}
//end - while
?>
