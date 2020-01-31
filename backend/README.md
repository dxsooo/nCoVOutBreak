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
curl http://service-r8373tyc-1253891892.gz.apigw.tencentcs.com/api/v1/provinces/guangdong  
[{"city": "广州市", "id": "guangzhou", "confirmed": 94, "healed": 0, "dead": 0}, {"city": "深圳市", "id": "shenshen", "confirmed": 98, "healed": 0, "dead": 0}, {"city": "珠海市", "id": "zhuhai", "confirmed": 26, "healed": 0, "dead": 0}, {"city": "汕头市", "id": "shantou", "confirmed": 12, "healed": 0, "dead": 0}, {"city": "佛山市", "id": "foshan", "confirmed": 25, "healed": 0, "dead": 0}, {"city": "韶关市", "id": "shaoguan", "confirmed": 4, "healed": 0, "dead": 0}, {"city": "河源市", "id": "heyuan", "confirmed": 1, "healed": 0, "dead": 0}, {"city": "梅州市", "id": "meizhou", "confirmed": 5, "healed": 0, "dead": 0}, {"city": "惠州市", "id": "huizhou", "confirmed": 17, "healed": 0, "dead": 0}, {"city": "汕尾市", "id": "shanwei", "confirmed": 1, "healed": 0, "dead": 0}, {"city": "东莞市", "id": "dongguan", "confirmed": 11, "healed": 0, "dead": 0}, {"city": "中山市", "id": "zhongshan", "confirmed": 18, "healed": 0, "dead": 0}, {"city": "江门市", "id": "jiangmeng", "confirmed": 1, "healed": 0, "dead": 0}, {"city": "阳江市", "id": "yangjiang", "confirmed": 10, "healed": 0, "dead": 0}, {"city": "湛江市", "id": "zhanjiang", "confirmed": 11, "healed": 0, "dead": 0}, {"city": "茂名市", "id": "maoming", "confirmed": 3, "healed": 0, "dead": 0}, {"city": "肇庆市", "id": "zhaoqin", "confirmed": 5, "healed": 0, "dead": 0}, {"city": "清远市", "id": "qingyuan", "confirmed": 6, "healed": 0, "dead": 0}, {"city": "揭阳市", "id": "jieyang", "confirmed": 6, "healed": 0, "dead": 0}]
```
``` bash
curl http://service-r8373tyc-1253891892.gz.apigw.tencentcs.com/api/v1/provinces/guangdong/cities/dongguan
{"city": "东莞市", "id": "dongguan", "confirmed": 11, "healed": 0, "dead": 0}
```

## 补充说明
由于目前各省卫健委仅提供到确诊病例数，治愈和死亡病例数暂处理为0。