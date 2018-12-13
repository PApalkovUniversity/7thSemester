<?php
echo "<H2>Редактирование сообщения</H2>";
//SQL-запрос, который выберет данные по теме
$sql="SELECT id, textmessage FROM MESSAGE WHERE id=" .$_GET['nummessage'];
//Выполняем запрос
$data=mysql_query($sql) or die(mysql_error()); //Получаем результат - одна запись
$line=mysql_fetch_row($data);
?>
<form action="?act=edit_message&nummessage=<?php echo $line[0]?>" method="post">
Текст сообщения : <BR>
<textarea name="message" cols=40 rows=5><?=$line[1]?>
</textarea>
<BR>
<input type="submit" value="Изменить"> </form>
