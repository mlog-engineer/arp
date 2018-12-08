# arp-collecter
arp-collecter 是一个可以实时抓取航空METAR和TAF报文的小型模块包，该模块包可以进行单个机场的报文查询，也可以进行实时的抓取和保存、归档。其数据源来自于[AWC](https://aviationweather.gov/)。

## 安装与配置
本模块包仅支持Python3.x版本，全部使用Python标准库，无需额外安装依赖库，可以直接下载或者使用`git`克隆代码库。文件中包含配置文件`config.json`, 该文件保存了实时抓取程序的配置, 包括保存路径、归档路径、日志路径以及所要抓取的机场列表信息。使用者可以对其内容进行自定义配置。其默认配置如下：
```json
{
  "metar":{
    "log_path":"/mnt/data14/liwt/opr/metar/log/",
    "archive_path":"/mnt/data14/liwt/opr/metar/archive/",
    "buffer_path":"/mnt/data14/liwt/opr/metar/buffer/",
    "realtime_path":"/mnt/data14/liwt/opr/metar/realtime/"
  },
  "taf":{
    "log_path":"/mnt/data14/liwt/opr/taf/log/",
    "archive_path":"/mnt/data14/liwt/opr/taf/archive/",
    "buffer_path":"/mnt/data14/liwt/opr/taf/buffer/",
    "realtime_path":"/mnt/data14/liwt/opr/taf/realtime/"
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
### 机场有效性检查
本模块包提供了对机场是否存在于AWC数据库进行检查的程序   
首先编辑`airports.json`文件，例如我要检查的机场代码为`ZBAA`（首都机场）和`ZBNY`（南苑机场），则在`airports.json`文件内写入：   
```json
[
  "ZBAA", "ZBNY"
]
```
若要增加其他机场，则可以在该列表后面按相应格式追加   
编辑完成以后执行`python ispt.py`，屏幕上会打印出每个机场的检验结果，valid表示有效，invalid表示无效   
```
inspecting ZBAA
valid
inspecting ZBNY
invalid
```
程序结束以后会将结果保存在`ispt_result.json`文件内   
```json
{"valid": ["ZBAA"], "invalid": ["ZBNY"]}
```

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
执行该命令以后，程序将按照配置文件`config.json`中的设置，爬取机场列表里所有机场的METAR报文，并将结果以`.json`的格式保存在`realtime_path`、`buffer_path`和`archive_path`路径下。   

#### 实时文件与缓存文件
`realtime_path`路径中保存有一个文件：`updated_metars.json`，该文件保存的是最新一次查询相较于上一次查询所更新的机场的报文信息。
`buffer_path`路径中保存有一个文件：`all_metars.json`，该文件保存有所有机场的最新一次返回的报文。   
例如某个时次`all_metars.json`中保存有全部41个机场的报文信息：   
```json
{
    "ZBAA": "METAR ZBAA 080200Z 30009MPS 280V340 CAVOK M06/M28 Q1042 NOSIG",
    "ZBTJ": "METAR ZBTJ 080200Z 33007MPS CAVOK M06/M25 Q1042 NOSIG",
    "ZBSJ": "METAR ZBSJ 080200Z 31004MPS CAVOK M04/M21 Q1043 NOSIG",
    "ZBYN": "METAR ZBYN 080200Z 35002MPS 300V030 CAVOK M11/M27 Q1038 NOSIG",
    "ZBHH": "METAR ZBHH 080200Z 18004MPS CAVOK M18/M26 Q1037 NOSIG",
    "ZYTX": "METAR ZYTX 080200Z 23004MPS 190V250 CAVOK M12/M24 Q1036 NOSIG",
    "ZYTL": "METAR ZYTL 080200Z VRB01MPS 0300 R28/0500V0750 +SN BKN023 M09/M11 Q1038 BECMG TL0330 1000 -SN",
    "ZYCC": "METAR ZYCC 080200Z 27005MPS 240V300 CAVOK M16/M29 Q1029 NOSIG",
    "ZYHB": "METAR ZYHB 080200Z 24006MPS CAVOK M17/M26 Q1026 NOSIG",
    "ZSSS": "METAR ZSSS 080200Z 33006MPS CAVOK 03/M02 Q1037 NOSIG",
    "ZSPD": "METAR ZSPD 080200Z 33009MPS CAVOK 04/M01 Q1036 NOSIG",
    "ZSNJ": "METAR ZSNJ 080200Z 05003MPS 360V090 CAVOK 01/M09 Q1040 NOSIG",
    "ZSOF": "METAR ZSOF 080200Z 07004MPS 030V090 CAVOK 01/M07 Q1040 NOSIG",
    "ZSHC": "METAR ZSHC 080200Z 34005MPS 310V020 7000 -SN BKN040 03/M03 Q1038 NOSIG",
    "ZSNB": "METAR ZSNB 080200Z 33006MPS 7000 -RAPL SCT010 BKN020 OVC050 03/01 Q1036 BECMG TL0330 -RA",
    "ZSFZ": "METAR ZSFZ 080200Z 02007MPS 9999 -RA OVC016 11/07 Q1029 NOSIG",
    "ZSAM": "METAR ZSAM 080200Z 04006MPS 360V060 9999 BKN027 17/10 Q1025 NOSIG",
    "ZSQD": "METAR ZSQD 080200Z 32007MPS 290V360 CAVOK M03/M12 Q1040 NOSIG",
    "ZHHH": "METAR ZHHH 080200Z 04004MPS 9999 -SN NSC 01/M03 Q1037 NOSIG",
    "ZHCC": "METAR ZHCC 080200Z 04004MPS 360V070 CAVOK M03/M13 Q1042 NOSIG",
    "ZGHA": "METAR ZGHA 080200Z 35005MPS 2700 -RA BR SCT005 BKN009 OVC050 02/02 Q1034 BECMG TL0300 3200 BKN011 OVC050",
    "ZGGG": "METAR ZGGG 080200Z 02006MPS 9999 BKN026 13/07 Q1025 NOSIG",
    "ZGOW": "METAR ZGOW 080200Z 04002MPS 360V110 9999 SCT023 18/12 Q1024 NOSIG",
    "ZGSZ": "METAR ZGSZ 080200Z 03006MPS 9999 BKN036 15/10 Q1024 NOSIG",
    "ZGNN": "METAR ZGNN 080200Z 34003MPS 6000 -RA FEW005 SCT010 OVC026 10/09 Q1026 NOSIG",
    "ZGKL": "METAR ZGKL 080200Z 04003MPS 8000 -RA FEW020 BKN026 OVC040 06/03 Q1030 NOSIG",
    "ZJHK": "METAR ZJHK 080200Z 07008MPS 9999 BKN007 OVC026 22/21 Q1019 NOSIG",
    "ZJSY": "METAR ZJSY 080200Z 10008MPS 9999 SCT021 28/23 Q1017 NOSIG",
    "ZUCK": "METAR ZUCK 080200Z 03003MPS 5000 -RA BR FEW005 SCT011 OVC040 05/04 Q1029 NOSIG",
    "ZUUU": "METAR ZUUU 080200Z 02003MPS 8000 -RA FEW006 SCT010 BKN020 04/04 Q1029 NOSIG",
    "ZPPP": "METAR ZPPP 080200Z 22005MPS 9999 BKN020 OVC036 12/09 Q1025 NOSIG",
    "ZLXY": "METAR ZLXY 080200Z 07007MPS CAVOK M04/M20 Q1039 NOSIG",
    "ZLLL": "METAR ZLLL 080200Z VRB01MPS 9999 -SN BKN040 M11/M15 Q1022 NOSIG",
    "ZWWW": "METAR ZWWW 080200Z VRB01MPS 6000 NSC M18/M21 Q1031 NOSIG",
    "ZWSH": "METAR ZWSH 080200Z 06002MPS 4500 BR BKN030 M08/M10 Q1025 NOSIG",
    "VHHH": "METAR VHHH 080200Z 35005KT 300V020 9999 FEW014 SCT035 17/11 Q1023 NOSIG",
    "VMMC": "METAR VMMC 080200Z 36017KT 9999 FEW012 SCT028 16/13 Q1023 NOSIG",
    "ZUGY": "METAR ZUGY 080200Z 01005MPS 330V070 9999 -RA FEW009 BKN015 OVC030 M00/M02 Q1027 NOSIG",
    "RCSS": "METAR RCSS 080200Z 09015KT 9999 VCSH FEW006 SCT020 BKN030 20/16 Q1025 NOSIG RMK A3028",
    "RCKH": "METAR RCKH 080200Z 36006KT 310V040 9999 FEW015 SCT030 BKN080 24/17 Q1019 NOSIG RMK A3011",
    "RCTP": "METAR RCTP 080200Z 05022KT 9999 FEW008 BKN012 BKN030 18/16 Q1025 NOSIG RMK A3027"
}
```
`updated_metars.json`中保存的信息为   
```json
[
    {
        "NAME": "ZBAA",
        "DATA": "METAR ZBAA 080200Z 30009MPS 280V340 CAVOK M06/M28 Q1042 NOSIG"
    },
    {
        "NAME": "ZBTJ",
        "DATA": "METAR ZBTJ 080200Z 33007MPS CAVOK M06/M25 Q1042 NOSIG"
    },
    {
        "NAME": "ZBSJ",
        "DATA": "METAR ZBSJ 080200Z 31004MPS CAVOK M04/M21 Q1043 NOSIG"
    },
    {
        "NAME": "ZBHH",
        "DATA": "METAR ZBHH 080200Z 18004MPS CAVOK M18/M26 Q1037 NOSIG"
    },
    {
        "NAME": "ZYCC",
        "DATA": "METAR ZYCC 080200Z 27005MPS 240V300 CAVOK M16/M29 Q1029 NOSIG"
    },
    {
        "NAME": "ZYHB",
        "DATA": "METAR ZYHB 080200Z 24006MPS CAVOK M17/M26 Q1026 NOSIG"
    },
    {
        "NAME": "ZSNJ",
        "DATA": "METAR ZSNJ 080200Z 05003MPS 360V090 CAVOK 01/M09 Q1040 NOSIG"
    },
    {
        "NAME": "ZSOF",
        "DATA": "METAR ZSOF 080200Z 07004MPS 030V090 CAVOK 01/M07 Q1040 NOSIG"
    },
    {
        "NAME": "ZHHH",
        "DATA": "METAR ZHHH 080200Z 04004MPS 9999 -SN NSC 01/M03 Q1037 NOSIG"
    },
    {
        "NAME": "ZHCC",
        "DATA": "METAR ZHCC 080200Z 04004MPS 360V070 CAVOK M03/M13 Q1042 NOSIG"
    }
]
```
这也就是说在最新一次返回的数据中只有10个机场的报文更新了，`updated_metars.json`文件就只保存这10个更新的报文。而`all_metars.json`保存所有机场的报文，若最新一个时次某机场并未更新，则该机场在`all_metars.json`中会保存上一时次的报文。   
爬虫程序将每隔5分钟查询一次，若所有机场的报文都没有更新，则`all_metars.json`，`updated_metars.json`都不会被重写，否则两个文件都会被重写一遍。   
为了平衡数据库入库操作和爬虫时次对比的方便，`all_metars.json`和`updated_metars.json`数据采用不同的保存格式。   

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
`2018-12-05 02:16:59,854:INFO: updated all_metars.json`表示`all_metars.json`文件已更新   
`2018-12-05 02:16:59,855:INFO: archived`表示新文件已归档     
若最新查询结果并无新的变化，则日志将提示   
`2018-12-05 02:22:06,138:INFO: last time is not updated`   
若发生错误信息，则日志会对错误信息做相应的记录
