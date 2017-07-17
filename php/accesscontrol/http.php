<?php
/**
 * @Author: 郭 璞
 * @File: http.php
 * @Time: 2017/7/13
 * @Contact: 1064319632@qq.com
 * @blog: http://blog.csdn.net/marksinoberg
 * @Description: 通过HTTP的Authenticate 进行访问控制。
 **/

// 合法的用户，可以是存储在数据库中或者其他的存储介质中。
$users = [
    "zhangsan" => "zhangsan",
    "lisi" => "lisi",
    "wangwu" => "wangwu",
    "zhaoliu" => "zhaoliu"
];

if(!isset($_SERVER['PHP_AUTH_USER'])) {
    header("HTTP/1.1 401 Unauthorized");
    header("WWW-Authenticate: Basic realm='PHP Secured'");
    exit("Unauthorized");
}

if($users[$_SERVER['PHP_AUTH_USER']] != $_SERVER['PHP_AUTH_PW']) {
    header("HTTP/1.1 401 Unauthorized");
    header("WWW-Authenticate: Basic realm='PHP Secured'");
    exit("Unauthorized");
}

echo "You are credentials were:<br/>";
echo "Username: ".$_SERVER['PHP_AUTH_USER']."<br />";
echo "Password: ".$_SERVER['PHP_AUTH_PW']."<br />";

?>
