<?php
/**
 * @Author: 郭 璞
 * @File: redis-test.php
 * @Time: 2017/7/11
 * @Contact: 1064319632@qq.com
 * @blog: http://blog.csdn.net/marksinoberg
 * @Description: 使用redis实现一个前N名的统计效果。
 **/

$redis = new Redis();

$redis->connect("localhost", 6379);

$ip = $_SERVER['REMOTE_ADDR'];

if($redis->get($ip)) {
    exit("访问的能不能不要这么频繁？？？");
}
$testarr = ['name'=>'郭璞', 'age'=>22];

echo ($testarr);

$redis->set($ip, true, 30);