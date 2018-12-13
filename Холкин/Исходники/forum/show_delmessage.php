<?php
echo "<H2>Удаление сообщения</H2>";
//SQL-запрос, который выберет идент. номер удаляемого сообщения
$sql="SELECT id FROM MESSAGE WHERE id=" .$_GET['nummessage'];
//Выполняем запрос
$data=mysql_query ($sql) or die (mysql_error()) ;
//Получаем результат - одна запись
$line=mysql_fetch_row($data) ;
//Выводим надпись
echo"Вы действительно хотите удалить выбранное сообщение?";
?>
<form action="?act=del_message&nummessage=<?php echo $line[0]?>" method="post">
<input type="submit" value="Да">
</form>
<form action="index.php" method="post">
<input type="submit" value="Отмена">
</form>
