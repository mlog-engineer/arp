# arp-collecter
arp-collecter 是一个可以实时抓取航空METAR和TAF报文的小型模块包，该模块包可以进行单个机场的报文查询，也可以进行实时的抓取和保存、归档。其数据源来自于[AWC](https://aviationweather.gov/)。

## 安装与配置
本模块包仅支持Python3.x版本，全部使用Python标准库，无需额外安装依赖库，可以直接下载或者使用`git`克隆代码库:`git clone https://github.com/Clarmy/arp-collecter.git`
文件中包含配置文件`config.json`, 该文件保存了实时抓取程序的配置, 包括保存路径、归档路径、日志路径以及所要抓取的机场列表信息。使用者可以对其内容进行自定义配置。其默认配置如下：
```json
{
  "metar":{
    "log_path":"./data/metar/log/",
    "archive_path":"./data/metar/archive/",
    "realtime_path":"./data/metar/realtime/"
  },
  "taf":{
    "log_path":"./data/taf/log/",
    "archive_path":"./data/taf/archive/",
    "realtime_path":"./data/taf/realtime/"
  },
  "ICAOS":["ZBAA", "ZBTJ", "ZBSJ", "ZBYN", "ZBHH", "ZYTX", "ZYTL",
           "ZYCC", "ZYHB", "ZSSS", "ZSPD", "ZSNJ", "ZSOF", "ZSHC",
           "ZSNB", "ZSFZ", "ZSAM", "ZSQD", "ZHHH", "ZHCC", "ZGHA",
           "ZGGG", "ZGOW", "ZGSZ", "ZGNN", "ZGKL", "ZJHK", "ZJSY",
           "ZUCK", "ZUUU", "ZPPP", "ZLXY", "ZLLL", "ZWWW", "ZWSH",
           "VHHH", "VMMC", "ZUGY", "RCSS", "RCKH", "RCTP"]
}
```
其中log_path是日志保存路径、archive_path是归档路径、realtime_path是实时更新保存路径、ICAOS是所要爬取的机场列表，机场名使用ICAO码。
三个路径可以随意配置，若路径不存在则程序会自动创建。
机场列表默认为中国（包含港澳台）41个国际机场。这41个机场是AWC数据库里有的机场，其他小型国内机场的报文信息在该数据库中查询不到，因此该列表中不予收录。若机场列表中收录了数据库中没有的机场码，爬虫程序仍然可以运行，但是会影响爬取速度，所以建议在修改机场列表之前，先确认该机场的报文信息在AWC数据库中有收录。
查询方法：
进入AWC的METAR检索页面：https://aviationweather.gov/metar
在Request METAR data下面的IDs输入你想要查询的机场ICAO码，点击Get METAR data，若更新的页面中有显示METAR报文，则说明该机场的报文信息存在于AWC数据库。

## 使用方法
### 单个机场查询
对于单个机场信息的查询，按以下示例查询
`$ python collecter.py ZBAA metar`
该命令是查询机场ZBAA（首都国际机场）的最新METAR报文
同理，若要查询首都机场的最新TAF报文，可以执行
`$ python collecter.py ZBAA taf`

### 自动化实时爬取
若想要自动化实时爬取并保存METAR报文数据，可以执行
`$ python oparp.py metar`
或者在服务器上后台运行
`$ nohup python oparp.py metar &`
同理要爬取TAF报文只需将`metar`换为`taf`即可。
执行该命令以后，程序将按照配置文件`config.json`中的设置，爬取机场列表里所有机场的METAR报文，并将结果以`.json`的格式保存在`realtime_path`和`archive_path`路径下。
#### 实时文件
`realtime_path`路径中保存有两个文件：`all_metars.json`和`updated_metars.json`，其中`all_metars.json`保存有所有机场的最新一次返回的报文，`updated_metars.json`保存的是最新一次查询相较于上一次查询所更新的机场的报文信息。
例如某个时次`all_metars.json`中保存的信息：
```
{"ZBAA": "METAR ZBAA 050230Z 08002MPS 040V120 CAVOK M01/M14 Q1031 NOSIG", "ZBTJ": "METAR ZBTJ 050230Z 11001MPS CAVOK 02/M06 Q1031 NOSIG", "ZBSJ": "METAR ZBSJ 050200Z VRB01MPS 1300 R15/1600D -SN BR OVC033 M02/M02 Q1030 BECMG TL0330 1500", "ZBYN": "METAR ZBYN 050230Z 18002MPS 2500 -SN BR FEW020 OVC040 M04/M05 Q1025 NOSIG", "ZBHH": "METAR ZBHH 050200Z VRB01MPS 6000 FEW040 M06/M20 Q1022 NOSIG", "ZYTX": "METAR ZYTX 050230Z VRB01MPS CAVOK M04/M16 Q1033 NOSIG", "ZYTL": "METAR ZYTL 050230Z 08006MPS CAVOK 01/M07 Q1031 NOSIG", "ZYCC": "METAR ZYCC 050200Z 25003MPS 210V310 CAVOK M12/M24 Q1032 NOSIG", "ZYHB": "METAR ZYHB 050200Z 24006MPS CAVOK M13/M22 Q1031 NOSIG", "ZSSS": "METAR ZSSS 050230Z 06007MPS 9999 FEW033 12/06 Q1026 NOSIG", "ZSPD": "METAR ZSPD 050230Z 05007MPS 9999 SCT030 13/06 Q1026 NOSIG", "ZSNJ": "METAR ZSNJ 050200Z 10007MPS 9999 BKN033 09/05 Q1026 NOSIG", "ZSOF": "METAR ZSOF 050200Z 10007MPS 9999 BKN020 08/05 Q1025 NOSIG", "ZSHC": "METAR ZSHC 050230Z 08002MPS 8000 FEW011 BKN018 11/10 Q1026 NOSIG", "ZSNB": "METAR ZSNB 050200Z VRB01MPS 9000 FEW009 BKN026 13/12 Q1026 NOSIG", "ZSFZ": "METAR ZSFZ 050200Z 03007MPS 9999 OVC013 17/14 Q1022 BECMG TL0330 BKN015", "ZSAM": "METAR ZSAM 050200Z 06006MPS 9999 SCT023 22/17 Q1020 NOSIG", "ZSQD": "METAR ZSQD 050200Z 05003MPS 010V080 CAVOK 03/M06 Q1031 NOSIG", "ZHHH": "METAR ZHHH 050200Z 06005MPS 4500 -RA BR OVC040 09/06 Q1022 NOSIG", "ZHCC": "METAR ZHCC 050200Z 36004MPS 5000 -RASN BR SCT015 OVC030 03/01 Q1028 NOSIG", "ZGHA": "METAR ZGHA 050200Z 23002MPS 190V290 3000 BR FEW004 BKN006 OVC040 09/08 Q1022 BECMG TL0350 BKN011 OVC040", "ZGGG": "METAR ZGGG 050230Z 03001MPS 9000 NSC 24/17 Q1017 NOSIG", "ZGOW": "METAR ZGOW 050200Z 12003MPS 080V150 8000 BKN019 BKN033 23/19 Q1019 NOSIG", "ZGSZ": "METAR ZGSZ 050200Z 04002MPS 9999 BKN043 25/21 Q1017 NOSIG", "ZGNN": "METAR ZGNN 050200Z 09003MPS 050V130 6000 SCT007 OVC023 20/18 Q1017 NOSIG", "ZGKL": "METAR ZGKL 050200Z 05003MPS 020V080 9999 SCT020 OVC050 13/08 Q1020 NOSIG", "ZJHK": "METAR ZJHK 050200Z 06005MPS 020V090 9999 SCT013 27/23 Q1016 NOSIG", "ZJSY": "METAR ZJSY 050200Z 10004MPS 060V130 9999 FEW020 29/20 Q1016 NOSIG", "ZUCK": "METAR ZUCK 050200Z 02006MPS 9999 OVC033 12/08 Q1016 NOSIG", "ZUUU": "METAR ZUUU 050200Z 03006MPS 8000 BKN040 11/06 Q1017 NOSIG", "ZPPP": "METAR ZPPP 050200Z 23009MPS CAVOK 12/05 Q1022 NOSIG", "ZLXY": "METAR ZLXY 050200Z VRB01MPS 4000 -SN BR SCT030 OVC050 02/M00 Q1028 NOSIG", "ZLLL": "METAR ZLLL 050200Z 11003MPS 050V150 CAVOK M08/M13 Q1022 NOSIG", "ZWWW": "METAR ZWWW 050230Z 15002MPS CAVOK M11/M14 Q1039 NOSIG", "ZWSH": "METAR ZWSH 050200Z 03003MPS 010V100 4200 DU NSC M07/M12 Q1024 NOSIG", "VHHH": "METAR VHHH 050230Z 09016KT 9999 FEW015 SCT025 25/20 Q1017 NOSIG", "VMMC": "METAR VMMC 050230Z 09013KT 6000 FEW012 SCT022 25/22 Q1017 NOSIG", "ZUGY": "METAR ZUGY 050200Z 05002MPS 020V090 4500 BR SCT004 BKN015 OVC026 08/07 Q1016 BECMG TL0330 18005MPS", "RCSS": "METAR RCSS 050230Z 11013KT 9999 -RA FEW008 SCT020 BKN030 23/20 Q1020 NOSIG RMK A3012", "RCKH": "METAR RCKH 050230Z 26005KT 220V340 9999 FEW016 BKN100 29/20 Q1016 NOSIG RMK A3001", "RCTP": "METAR RCTP 050230Z 06021KT 9999 SCT012 BKN025 22/19 Q1019 NOSIG RMK A3011"}
```
而`updated_metars.json`中保存的信息只有一条
```
{"VHHH": "METAR VHHH 050300Z 09017KT 9999 FEW015 SCT025 26/20 Q1017 NOSIG"}
```
这也就是说在最新一次返回的数据中只有VHHH这个机场的报文更新了，`updated_metars.json`文件就只保存这个更新的报文。而`all_metars.json`保存所有机场的报文，若最新一个时次某机场并未更新，则该机场在`all_metars.json`中会保存上一时次的报文。
爬虫程序将每隔5分钟查询一次，若所有机场的报文都没有更新，则`all_metars.json`，`updated_metars.json`都不会被重写，否则两个文件都会被重写一遍。
#### 归档文件
最新报文除了会在`updated_metars.json`中不断重写，也会归档保存在`archive_path`目录中，该目录将以日期为文件夹来归档保存，每个文件为最新查询时间，例如`201812050135.json`

#### 日志文件
日志信息将保存在`log_path`中，每天自动保存为一个文件，当天实时更新的日志名为`taf`或`metar`，非当天的日志名为`metar.20181203.log`形式。   
日志中   
`2018-12-05 02:11:43,612:INFO: sleeping`表示程序睡眠中   
`2018-12-05 02:15:03,676:INFO: start crawling`表示爬虫程序开始查询
开始查询以后，日志将记录每个机场的查询状态   
```
2018-12-05 02:15:04,595:INFO: (1/41) ZBAA finished
2018-12-05 02:15:07,564:INFO: (2/41) ZBTJ finished
2018-12-05 02:15:10,417:INFO: (3/41) ZBSJ finished
2018-12-05 02:15:13,192:INFO: (4/41) ZBYN finished
2018-12-05 02:15:16,680:INFO: (5/41) ZBHH finished
2018-12-05 02:15:19,441:INFO: (6/41) ZYTX finished
2018-12-05 02:15:22,207:INFO: (7/41) ZYTL finished
2018-12-05 02:15:25,076:INFO: (8/41) ZYCC finished
2018-12-05 02:15:27,947:INFO: (9/41) ZYHB finished
2018-12-05 02:15:30,636:INFO: (10/41) ZSSS finished
2018-12-05 02:15:33,365:INFO: (11/41) ZSPD finished
2018-12-05 02:15:36,234:INFO: (12/41) ZSNJ finished
2018-12-05 02:15:38,996:INFO: (13/41) ZSOF finished
2018-12-05 02:15:41,763:INFO: (14/41) ZSHC finished
2018-12-05 02:15:44,630:INFO: (15/41) ZSNB finished
2018-12-05 02:15:47,394:INFO: (16/41) ZSFZ finished
2018-12-05 02:15:50,281:INFO: (17/41) ZSAM finished
2018-12-05 02:15:53,128:INFO: (18/41) ZSQD finished
2018-12-05 02:15:55,893:INFO: (19/41) ZHHH finished
2018-12-05 02:15:58,621:INFO: (20/41) ZHCC finished
2018-12-05 02:16:01,430:INFO: (21/41) ZGHA finished
2018-12-05 02:16:04,195:INFO: (22/41) ZGGG finished
2018-12-05 02:16:06,953:INFO: (23/41) ZGOW finished
2018-12-05 02:16:09,736:INFO: (24/41) ZGSZ finished
2018-12-05 02:16:12,485:INFO: (25/41) ZGNN finished
2018-12-05 02:16:15,248:INFO: (26/41) ZGKL finished
2018-12-05 02:16:18,013:INFO: (27/41) ZJHK finished
2018-12-05 02:16:20,881:INFO: (28/41) ZJSY finished
2018-12-05 02:16:23,748:INFO: (29/41) ZUCK finished
2018-12-05 02:16:26,615:INFO: (30/41) ZUUU finished
2018-12-05 02:16:29,499:INFO: (31/41) ZPPP finished
2018-12-05 02:16:32,245:INFO: (32/41) ZLXY finished
2018-12-05 02:16:35,120:INFO: (33/41) ZLLL finished
2018-12-05 02:16:38,082:INFO: (34/41) ZWWW finished
2018-12-05 02:16:40,849:INFO: (35/41) ZWSH finished
2018-12-05 02:16:43,716:INFO: (36/41) VHHH finished
2018-12-05 02:16:46,480:INFO: (37/41) VMMC finished
2018-12-05 02:16:49,261:INFO: (38/41) ZUGY finished
2018-12-05 02:16:52,113:INFO: (39/41) RCSS finished
2018-12-05 02:16:54,983:INFO: (40/41) RCKH finished
2018-12-05 02:16:57,848:INFO: (41/41) RCTP finished
```
若机场有报文更新，则日志中将提供记录
```
2018-12-05 02:16:59,849:INFO: ZBAA is updated
2018-12-05 02:16:59,849:INFO: ZBTJ is updated
2018-12-05 02:16:59,849:INFO: ZBSJ is updated
2018-12-05 02:16:59,849:INFO: ZBYN is updated
2018-12-05 02:16:59,850:INFO: ZBHH is updated
2018-12-05 02:16:59,850:INFO: ZYTX is updated
2018-12-05 02:16:59,850:INFO: ZYTL is updated
2018-12-05 02:16:59,850:INFO: ZYCC is updated
2018-12-05 02:16:59,850:INFO: ZYHB is updated
2018-12-05 02:16:59,850:INFO: ZSSS is updated
2018-12-05 02:16:59,850:INFO: ZSPD is updated
2018-12-05 02:16:59,850:INFO: ZSNJ is updated
2018-12-05 02:16:59,850:INFO: ZSOF is updated
2018-12-05 02:16:59,851:INFO: ZSHC is updated
2018-12-05 02:16:59,851:INFO: ZSNB is updated
2018-12-05 02:16:59,851:INFO: ZSFZ is updated
2018-12-05 02:16:59,851:INFO: ZSAM is updated
2018-12-05 02:16:59,851:INFO: ZSQD is updated
2018-12-05 02:16:59,851:INFO: ZHHH is updated
2018-12-05 02:16:59,851:INFO: ZHCC is updated
2018-12-05 02:16:59,851:INFO: ZGHA is updated
2018-12-05 02:16:59,851:INFO: ZGGG is updated
2018-12-05 02:16:59,852:INFO: ZGOW is updated
2018-12-05 02:16:59,852:INFO: ZGSZ is updated
2018-12-05 02:16:59,852:INFO: ZGNN is updated
2018-12-05 02:16:59,852:INFO: ZGKL is updated
2018-12-05 02:16:59,852:INFO: ZJHK is updated
2018-12-05 02:16:59,852:INFO: ZJSY is updated
2018-12-05 02:16:59,852:INFO: ZUCK is updated
2018-12-05 02:16:59,852:INFO: ZUUU is updated
2018-12-05 02:16:59,852:INFO: ZPPP is updated
2018-12-05 02:16:59,853:INFO: ZLXY is updated
2018-12-05 02:16:59,853:INFO: ZLLL is updated
2018-12-05 02:16:59,853:INFO: ZWWW is updated
2018-12-05 02:16:59,853:INFO: ZWSH is updated
2018-12-05 02:16:59,853:INFO: VHHH is updated
2018-12-05 02:16:59,853:INFO: VMMC is updated
2018-12-05 02:16:59,853:INFO: ZUGY is updated
2018-12-05 02:16:59,853:INFO: RCSS is updated
2018-12-05 02:16:59,853:INFO: RCKH is updated
2018-12-05 02:16:59,853:INFO: RCTP is updated
```
查询结束以后将记录保存和归档情况    
`2018-12-05 02:16:59,854:INFO: updated updated_metars.json`表示`updated_metars.json`文件已更新    
`2018-12-05 02:16:59,854:INFO: updated all_metars.json`表示`updated all_metars.json`文件已更新   
`2018-12-05 02:16:59,855:INFO: archived`表示新文件已归档     
若最新查询结果并无新的变化，则日志将提示   
`2018-12-05 02:22:06,138:INFO: last time is not updated`   
若发生错误信息，则日志会对错误信息做相应的记录
