<?php
echo "<H2>Создание темы</H2>";
?>
<form action="?act=add_topic&numrazdel=<?php echo $_GET['numrazdel']?>" method="post">
Название темы:<BR>
<input name="name_topic" type="text" value="">
<BR>
Текст сообщения:<BR>
<textarea name="message" cols=40 rows=5></textarea> <BR>
<input type="submit" value="Создать тему">
</form>
