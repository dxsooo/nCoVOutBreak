import React, { Component } from 'react';
import ReactEcharts from 'echarts-for-react'
import axios from 'axios';
import './App.css';

require('echarts/map/js/province/guangdong.js');

class App extends Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }
  getInitialState = () => ({
    option: this.getOption(),
    isLoaded: false
  });

  componentDidMount(){
    axios.get("/api/v1/provinces/guangdong").then(
      result => {
        const data = result.data
        const option = this.state.option;
        option.title.text = data.province + '新冠肺炎 2019-nCoV 爆发最新疫情情况';
        option.title.subtext = '累计确诊病例:' + data.confirmed + ' 累计死亡病例:' + data.dead + ' 累计治愈病例:' + data.healed;
        option.series[0].mapType = data.province 
        option.series[0].data = data.cities.map(x => { return {'name': x.city, 'value': x.confirmed} })
        this.setState({
          option: option,
          isLoaded: true
        });
      },
      // Note: it's important to handle errors here
      // instead of a catch() block so that we don't swallow
      // exceptions from actual bugs in components.
      error => {
        console.error(error)
      }
      );
  }

  getOption = () => {
    return {
      title: {
        text: '新冠肺炎 2019-nCoV 爆发最新疫情情况',
        subtext: '累计确诊病例:' + 0 + ' 累计死亡病例:' + 0 + ' 累计治愈病例:' + 0,
        left: 'center'
      },
      tooltip: {
        trigger: 'item',
        formatter: function(data){
          return isNaN(data.value)?data.name:
              (data.name + "<br/>" + data.seriesName + ':' + data.value);
        }
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
          mapType: null,
          label: {
            normal: {
              show: true
            },
            emphasis: {
              show: true
            }
          },
          // data: raw.cities.map(x => { return {'name': x.city, 'value':x.confirmed};})
          data: []
        }
      ]
    };
  };

  render(){
    const res = !this.state.isLoaded?<div/>:
     (
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
    return res;
  }
}

export default App;
