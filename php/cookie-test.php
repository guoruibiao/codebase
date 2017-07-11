<?php
/**
 * @Author: 郭 璞
 * @File: cookie-test.php
 * @Time: 2017/7/11
 * @Contact: 1064319632@qq.com
 * @blog: http://blog.csdn.net/marksinoberg
 * @Description: Cookie 操作相关。
 **/


$historyid = $_GET['historyid'];
$product = $_GET['product'];
if ( $_COOKIE[$historyid] ) {
    setcookie($historyid, "", time());
}
setcookie("history[$historyid]", $product, time() + 60);


//var_dump($_COOKIE[2]);

echo "您最近浏览了：";
$result = $_COOKIE['history'];
$result = array_reverse($result);
foreach ($result as $key=>$value) {
    echo "$key ↑: [$value]<br>";
}
?>
<ul>
    <li><a href="http://localhost/learn/rubbish/cookie-test.php?historyid=1&product=PHP">5天精通PHP</a></li>
    <li><a href="http://localhost/learn/rubbish/cookie-test.php?historyid=2&product=MySQL">一小时MySQL包教包会</a></li>
    <li><a href="http://localhost/learn/rubbish/cookie-test.php?historyid=3&product=Python">2天玩转Python</a></li>
    <li><a href="http://localhost/learn/rubbish/cookie-test.php?historyid=4&product=Java">一周成为高级Java工程师</a></li>
    <li><a href="http://localhost/learn/rubbish/cookie-test.php?historyid=5&product=Nodejs">Nodejs 3天包分配</a></li>
</ul>