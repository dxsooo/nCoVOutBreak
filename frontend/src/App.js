import React, {Component} from 'react';
import ReactEcharts from 'echarts-for-react'
import axios from 'axios';
import './App.css';
import {Tabs} from 'antd';

const {TabPane} = Tabs;

function callback(key) {
    console.log(key);
}

require('echarts/map/js/province/beijing.js');
require('echarts/map/js/province/hebei.js');
require('echarts/map/js/province/shanxi.js');
require('echarts/map/js/province/neimenggu.js');
require('echarts/map/js/province/liaoning.js');
require('echarts/map/js/province/fujian.js');
require('echarts/map/js/province/guangdong.js');

class Chart extends Component {
    constructor(props) {
        super(props);
        this.state = this.getInitialState();
    }

    getInitialState = () => ({
        option: this.getOption(),
        isLoaded: false
    });

    componentDidMount() {
        axios.get("https://service-r8373tyc-1253891892.gz.apigw.tencentcs.com/api/v1/provinces/" + this.props.province).then(
            result => {
                const data = result.data;
                const option = this.state.option;
                option.title.text = data.province + '新冠肺炎 2019-nCoV 爆发最新疫情情况';
                option.title.subtext = '累计确诊病例:' + data.confirmed + ' 累计死亡病例:' + data.dead + ' 累计治愈病例:' + data.healed;
                option.series[0].mapType = data.province;
                option.series[0].data = data.cities.map(x => {
                    return {'name': x.city, 'value': x.confirmed}
                });
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
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: function (data) {
                    return isNaN(data.value) ? data.name :
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
                    data: []
                }
            ]
        };
    };

    render() {
        return !this.state.isLoaded ? <div/> :
            (
                <ReactEcharts
                    style={{height: '700px', width: '100%'}}
                    notMerge={true}
                    lazyUpdate={true}
                    option={this.state.option || {}}/>
            );
    }
}

class App extends Component {
    render() {
        return (
            <div className="App">
                <Tabs defaultActiveKey="beijing" onChange={callback}>
                    <TabPane tab="北京" key="beijing">
                        <Chart province="beijing"/>
                    </TabPane>
                    <TabPane tab="天津" disabled key="tianjin">
                        Content of Tab Pane 2
                    </TabPane>
                    <TabPane tab="河北" key="hebei">
                        <Chart province="hebei"/>
                    </TabPane>
                    <TabPane tab="山西" disabled key="shanxi">
                        <Chart province="shanxi"/>
                    </TabPane>
                    <TabPane tab="内蒙古" key="neimenggu">
                        <Chart province="neimenggu"/>
                    </TabPane>
                    <TabPane tab="辽宁" key="liaoning">
                        <Chart province="liaoning"/>
                    </TabPane>
                    <TabPane tab="吉林" disabled key="jilin">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="黑龙江" disabled key="heilongjiang">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="上海" disabled key="shanghai">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="江苏" disabled key="jiangsu">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="浙江" disabled key="zhejiang">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="安徽" disabled key="anhui">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="福建" key="fujian">
                        <Chart province="fujian"/>
                    </TabPane>
                    <TabPane tab="江西" disabled key="jiangxi">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="山东" disabled key="shandong">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="河南" disabled key="henan">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="湖北" disabled key="hubei">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="湖南" disabled key="hunan">
                        Content of Tab Pane 3
                    </TabPane>
                    <TabPane tab="广东" key="guangdong">
                        <Chart province="guangdong"/>
                    </TabPane>
                </Tabs>
            </div>
        )
    }
}

export default App;
