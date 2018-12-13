<html>
<head>
    <title>Форум</title>
    <link href="static/style.css" rel="stylesheet" type="text/css">
</head>

<body>
	<div class="container">
	  <div class="header"><a href="index.php">ПРИРОДА РОССИИ ФОРУМ</a></div>
			<div class="search" align="center">
      </body>
      <?php
      //Запускаем сессию
      session_start();
      //Подключаемся к MySQL и базе данных FORUM
      require_once ('connect.php');
      //Если пользователь не авторизован, //то выводим ссылку нa login. php
      if(!isset($_SESSION['autorized']))
      {
      ?>
      <p align='right'>
      <h1><a href='login.php'>Авторизация</а><br></h1> </p>
        <br/>
      <h1><a href='signup.php'>Регистрация</а><br></h1> </p>
      <?php
      $_SESSION['name']='guest';
      $_SESSION['role'] = 'user';
      }
      else
      {
      //Если пользователь авторизован,то сообщаем ему об этом //и выводим ссылку на logout.php
      echo "<p style='text-align:right'>Вы авторизованы под ником: ".$_SESSION['name']."</br>";
      echo "<a href='logout.php'>Выход</а></р><br/><br/>";
      echo "<a href=none></a>";
      //Если выполняется действие,
      if(isset($_GET['act'])) {
      //то подключаем модуль, отвечающий за это, //и совершаем действие
      require_once ('action.php');
      }
      //Иначе осуществляем простой вывод информации else
      require_once ('show.php');
      }
      ?>
      <a href=none></a>
			</div>
	    <h4>&nbsp;</h4>
	  <div class="footer">

	    <p><em>Любое копирование материалов с этого сайта запрещено</em></p>
	  <!-- end .footer --></div>
	  <!-- end .container --></div>



</html>
