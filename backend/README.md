# 后端
获取最新疫情数据的 API，使用 Python 开发，架构方案是 腾讯云函数+API网关  
由于每个省份的数据信息解析有别，对每个省份单独配置接口和编写入口代码

*API 地址： http://service-r8373tyc-1253891892.gz.apigw.tencentcs.com*

## API 设计
整体符合 RESTful 风格
```
# 获取特定省份数据
GET /api/v1/provinces/{provinceName}

# 获取特定城市数据
GET /api/v1/provinces/{provinceName}/cities/{cityName}
```

## 请求示例
``` bash
curl -s http://service-r8373tyc-1253891892.gz.apigw.tencentcs.com/api/v1/provinces/guangdong | jq                                
{
  "province": "广东",
  "id": "guangdong",
  "confirmed": 683,
  "healed": 14,
  "dead": 0,
  "cities": [
    {
      "city": "深圳市",
      "id": "shenzhen",
      "confirmed": 226,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "广州市",
      "id": "guangzhou",
      "confirmed": 189,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "珠海市",
      "id": "zhuhai",
      "confirmed": 51,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "佛山市",
      "id": "foshan",
      "confirmed": 43,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "东莞市",
      "id": "dongguan",
      "confirmed": 31,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "惠州市",
      "id": "huizhou",
      "confirmed": 28,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "中山市",
      "id": "zhongshan",
      "confirmed": 25,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "汕头市",
      "id": "shantou",
      "confirmed": 17,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "湛江市",
      "id": "zhanjiang",
      "confirmed": 14,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "阳江市",
      "id": "yangjiang",
      "confirmed": 10,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "肇庆市",
      "id": "zhaoqing",
      "confirmed": 7,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "梅州市",
      "id": "meizhou",
      "confirmed": 7,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "清远市",
      "id": "qingyuan",
      "confirmed": 6,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "揭阳市",
      "id": "jieyang",
      "confirmed": 6,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "韶关市",
      "id": "shaoguan",
      "confirmed": 5,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "汕尾市",
      "id": "shanwei",
      "confirmed": 5,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "茂名市",
      "id": "maoming",
      "confirmed": 4,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "江门市",
      "id": "jiangmen",
      "confirmed": 4,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "潮州市",
      "id": "chaozhou",
      "confirmed": 4,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "河源市",
      "id": "heyuan",
      "confirmed": 1,
      "healed": 0,
      "dead": 0
    }
  ]
}
```
``` bash
curl -s http://service-r8373tyc-1253891892.gz.apigw.tencentcs.com/api/v1/provinces/guangdong/cities/dongguan | jq
{
  "city": "东莞市",
  "id": "dongguan",
  "confirmed": 31,
  "healed": 0,
  "dead": 0
}
```

## 支持情况

| 省/直辖市/自治区 | 代码支持 | 功能支持 || 省/直辖市/自治区 | 代码支持 | 功能支持 |
| --- | --- | --- | --- | --- | --- | --- |
| 北京市 | ✅ | ✅ || 湖南省 | ✅ | ✅ |
| 天津市 | ✅ | ✅ || 广东省 | ✅ | ✅ |
| 河北省 | ✅ | ✅ || 广西壮族自治区 | ❌ | ❌ |
| 山西省 | ❌ | ❌ || 海南省 | ❌ | ❌ |
| 内蒙古自治区 | ✅ | ✅ || 重庆市 | ❌ | ❌ |
| 辽宁省 | ✅ | ✅ || 四川省 | ❌ | ❌ |
| 吉林省 | ✅ | ✅ || 贵州省 | ❌ | ❌ |
| 黑龙江省 | ✅ | ✅ || 云南省 | ❌ | ❌ |
| 上海市 | ❌ | ❌ || 西藏自治区 | ✅ | ✅ |
| 江苏省 | ✅ | ✅ || 陕西省 | ❌ | ❌ |
| 浙江省 | ✅ | ✅ || 甘肃省 | ❌ | ❌ |
| 安徽省 | ✅ | ✅ || 青海省 | ❌ | ❌ |
| 福建省 | ✅ | ✅ || 宁夏回族自治区 | ❌ | ❌ |
| 江西省 | ✅ | ✅ || 新疆维吾尔自治区 | ❌ | ❌ |
| 山东省 | ❌ | ❌ || 香港特别行政区 | ❌ | ❌ |
| 河南省 | ✅ | ✅ || 澳门特别行政区 | ❌ | ❌ |
| 湖北省 | ❌ | ❌ || 台湾省 | ❌ | ❌ |

## 补充说明
- 由于目前部分省卫健委在城市级别仅提供到确诊病例数，城市级别治愈和死亡病例数暂处理为0
- 直辖市支持到区级数据
