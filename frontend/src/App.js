import React, { Component } from 'react';
import ReactEcharts from 'echarts-for-react'
import './App.css';

require('echarts/map/js/province/guangdong.js');

const raw = {
  "province": "广东",
  "id": "guangdong",
  "confirmed": 1131,
  "healed": 128,
  "dead": 1,
  "cities": [
    {
      "city": "深圳市",
      "id": "shenzhen",
      "confirmed": 366,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "广州市",
      "id": "guangzhou",
      "confirmed": 307,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "珠海市",
      "id": "zhuhai",
      "confirmed": 83,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "佛山市",
      "id": "foshan",
      "confirmed": 67,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "东莞市",
      "id": "dongguan",
      "confirmed": 58,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "中山市",
      "id": "zhongshan",
      "confirmed": 51,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "惠州市",
      "id": "huizhou",
      "confirmed": 48,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "汕头市",
      "id": "shantou",
      "confirmed": 25,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "湛江市",
      "id": "zhanjiang",
      "confirmed": 21,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "江门市",
      "id": "jiangmen",
      "confirmed": 19,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "肇庆市",
      "id": "zhaoqing",
      "confirmed": 14,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "阳江市",
      "id": "yangjiang",
      "confirmed": 13,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "梅州市",
      "id": "meizhou",
      "confirmed": 13,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "清远市",
      "id": "qingyuan",
      "confirmed": 10,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "茂名市",
      "id": "maoming",
      "confirmed": 10,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "揭阳市",
      "id": "jieyang",
      "confirmed": 7,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "韶关市",
      "id": "shaoguan",
      "confirmed": 6,
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
      "city": "潮州市",
      "id": "chaozhou",
      "confirmed": 5,
      "healed": 0,
      "dead": 0
    },
    {
      "city": "河源市",
      "id": "heyuan",
      "confirmed": 3,
      "healed": 0,
      "dead": 0
    }
  ]
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }
  timeTicket = null;
  getInitialState = () => ({option: this.getOption()});

  getOption = () => {
    return {
      title: {
        text: '广东省新冠肺炎 2019-nCoV 爆发最新疫情情况',
        subtext: '累计确诊病例:' + raw.confirmed + ' 累计死亡病例:' + raw.dead + ' 累计治愈病例:' + raw.healed,
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      visualMap: {
        min: 0,
        max: 500,
        left: 'left',
        top: 'bottom',
        calculable: true
      },
      toolbox: {
        show: true,
        orient: 'vertical',
        left: 'right',
        top: 'center',
        feature: {
          dataView: {readOnly: false},
          restore: {},
          saveAsImage: {}
        }
      },
      series: [
        {
          name: '确诊',
          type: 'map',
          mapType: '广东',
          label: {
            normal: {
              show: true
            },
            emphasis: {
              show: true
            }
          },
          data: raw.cities.map(x => { return {'name': x.city, 'value':x.confirmed};})
        }
      ]
    };
  };

  render(){
    return (
      <div className="App">
        <header className="App-header">
          <ReactEcharts
            style={{height: '700px', width: '100%'}} 
            notMerge={true}
            lazyUpdate={true}
            option={this.state.option || {}} />
          </header>
      </div>
    );
  }
}

export default App;
