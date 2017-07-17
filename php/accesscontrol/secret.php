<?php
/**
 * @Author: 郭 璞
 * @File: secret.php
 * @Time: 2017/7/13
 * @Contact: 1064319632@qq.com
 * @blog: http://blog.csdn.net/marksinoberg
 * @Description:
 **/

session_start();

$users = [
    "zhangsan" => "zhangsan",
    "lisi" => "lisi",
    "wangwu" => "wangwu",
    "zhaoliu" => "zhaoliu"
];

$username = $_POST['username'];
$password = $_POST['password'];

if(in_array($username, $users)) {
    if($password===$users[$username]) {
        $_SESSION['username'] = $username;
        echo "Welcome <mark>$username </mark>, you can see secret documents now.";
    }else{
        echo "Sorry, Username not match password.<br>Please check it carefully.";
    }
}else{
    echo "Sorry, you are unauthorized.";
}

