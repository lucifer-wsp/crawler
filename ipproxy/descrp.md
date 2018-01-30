## IPProxy 爬虫介绍

* 爬虫介绍
	* 最初始的目的是为了获取国内某平台的数据，由于该平台存在访问限制，于是就想到用代理池，本人承诺未做任何攻击或损坏他人利益的事情。代理池的ip主要是针对国内一些免费的代理网站爬取的http和https的，爬取后的ip在piplines的时候插入到了数据库中。

		```
		http://www.xicidaili.com/
		http://ip.zdaye.com/dayProxy.html
		http://www.ip3366.net/
		http://www.66ip.cn/index.html
		http://www.goubanjia.com/free/index.shtml
		https://www.kuaidaili.com/free/
		http://www.nianshao.me/
		http://www.httpsdaili.com/free.asp
		```
		
	* ip有效性检测：目前是获取淘宝的页面数据来判断，当前不区分国内外代理。
	
	```
		http://ip.filefab.com/index.php
		http://ip.chinaz.com/getip.aspx
	```
	
	* goubanjia网站的代理ip端口做了处理，后端返回的数据之后前端对端口又做了重新计算，js有点儿复杂，没怎么看懂，因此该网站暂时还无法获取。
	
* 数据库介绍
	* 数据库主要保存了ip的一些常用信息，ip地址、ip协议[HTTP/HTTPS]、ip支持的类型[GET/POST]、ip的刷新时间、ip是否存活和ip的响应时间。
	数据库表设计：
	
		```
		CREATE TABLE `proxy_info` (
		  `protocal` smallint(1) NOT NULL DEFAULT '1',
		  `alive` smallint(1) NOT NULL DEFAULT '1',
		  `response_time` float(5,2) DEFAULT NULL,
		  `check_time` varchar(20) DEFAULT NULL,
		  `ip_port` varchar(30) NOT NULL,
		  PRIMARY KEY (`ip_port`)
		) ENGINE=InnoDB DEFAULT CHARSET=latin1;
		```
		
声明：_该代码仅供学习参考，不会用于商业利益，侵删_ 