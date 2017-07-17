<?php
/**
 * @Author: 郭 璞
 * @File: login.php
 * @Time: 2017/7/13
 * @Contact: 1064319632@qq.com
 * @blog: http://blog.csdn.net/marksinoberg
 * @Description:
 **/
session_start();


$html = <<< EOD
<form action="secret.php" method="POST">

    <legend>
        用户登录
    </legend>
    <fieldset>
        <label for="username">Username:</label>
        <input type="text" name="username"><br/>
        <br>
        <label for="password">Password:</label>
        <input type="password" name="password"><br/>
        <br>
        <input type="submit" value="登录">
    </fieldset>

</form>
EOD;

// 输出表单
echo $html;
