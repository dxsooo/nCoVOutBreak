import React, {Component} from 'react';
import ReactEchartsCore from 'echarts-for-react/lib/core'
import echarts from 'echarts/lib/echarts'
import 'echarts/lib/chart/map';
import 'echarts/lib/component/title';
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/visualMap';
import 'echarts/lib/component/toolbox';
import axios from 'axios';
import './App.css';
import {Tabs} from 'antd';

const {TabPane} = Tabs;

require('echarts/map/js/province/beijing.js');
require('echarts/map/js/province/tianjin.js');
require('echarts/map/js/province/hebei.js');
require('echarts/map/js/province/neimenggu.js');
require('echarts/map/js/province/liaoning.js');
require('echarts/map/js/province/jilin.js');
require('echarts/map/js/province/heilongjiang.js');
require('echarts/map/js/province/jiangsu.js');
require('echarts/map/js/province/zhejiang.js');
require('echarts/map/js/province/anhui.js');
require('echarts/map/js/province/fujian.js');
require('echarts/map/js/province/jiangxi.js');
require('echarts/map/js/province/henan.js');
require('echarts/map/js/province/hunan.js');
require('echarts/map/js/province/guangdong.js');
require('echarts/map/js/province/guangxi.js');
require('echarts/map/js/province/hainan.js');
require('echarts/map/js/province/guizhou.js');
require('echarts/map/js/province/yunnan.js');
require('echarts/map/js/province/xizang.js');
require('echarts/map/js/province/shanxi1.js');
require('echarts/map/js/province/qinghai.js');
require('echarts/map/js/province/ningxia.js');
require('echarts/map/js/province/xinjiang.js');

class Chart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            option: this.getInitialOption(),
        };
    }

    getInitialOption = () => {
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
                max: 800,
                left: 'left',
                top: 'bottom',
                calculable: true,
                inRange: {
                    color: ['#f6ea8c', '#f26d5b', '#c03546', '#492540']
                }
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
                    name: '累计确诊',
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
        if (this.props.loaded) {
            const option = this.state.option;
            option.title.text = this.props.data.province + '新冠肺炎 2019-nCoV 爆发最新疫情情况';
            option.title.subtext = '累计确诊病例:' + this.props.data.confirmed + ' 累计死亡病例:' + this.props.data.dead + ' 累计治愈病例:' + this.props.data.healed;
            option.series[0].mapType = this.props.data.province;
            option.series[0].data = this.props.data.cities.map(x => {
                return {'name': x.city, 'value': x.confirmed}
            });
            option.series[0].label.normal.show = this.props.data.province!=="海南";
            return (
                <ReactEchartsCore
                    echarts={echarts}
                    style={{height: '700px', width: '100%'}}
                    notMerge={true}
                    lazyUpdate={true}
                    option={option}/>
            )
        }
        return (<div/>)
    }
}

class App extends Component {
    constructor(props) {
        super(props);
        const panes = [
            {title: '北京', key: 'beijing', disabled: false, data: {}},
            {title: '天津', key: 'tianjin', disabled: false, data: {}},
            {title: '河北', key: 'hebei', disabled: false, data: {}},
            {title: '山西', key: 'shanxi', disabled: true, data: {}},
            {title: '内蒙古', key: 'neimenggu', disabled: false, data: {}},
            {title: '辽宁', key: 'liaoning', disabled: false, data: {}},
            {title: '吉林', key: 'jilin', disabled: false, data: {}},
            {title: '黑龙江', key: 'heilongjiang', disabled: false, data: {}},
            {title: '上海', key: 'shanghai', disabled: true, data: {}},
            {title: '江苏', key: 'jiangsu', disabled: false, data: {}},
            {title: '浙江', key: 'zhejiang', disabled: false, data: {}},
            {title: '安徽', key: 'anhui', disabled: false, data: {}},
            {title: '福建', key: 'fujian', disabled: false, data: {}},
            {title: '江西', key: 'jiangxi', disabled: false, data: {}},
            {title: '山东', key: 'shandong', disabled: true, data: {}},
            {title: '河南', key: 'henan', disabled: false, data: {}},
            {title: '湖北', key: 'hubei', disabled: true, data: {}},
            {title: '湖南', key: 'hunan', disabled: false, data: {}},
            {title: '广东', key: 'guangdong', disabled: false, data: {}},
            {title: '广西', key: 'guangxi', disabled: false, data: {}},
            {title: '海南', key: 'hainan', disabled: false, data: {}},
            {title: '重庆', key: 'chongqing', disabled: true, data: {}},
            {title: '四川', key: 'sichuan', disabled: true, data: {}},
            {title: '贵州', key: 'guizhou', disabled: false, data: {}},
            {title: '云南', key: 'yunnan', disabled: false, data: {}},
            {title: '西藏', key: 'xizang', disabled: false, data: {}},
            {title: '陕西', key: 'shaanxi', disabled: false, data: {}},
            {title: '甘肃', key: 'gansu', disabled: true, data: {}},
            {title: '青海', key: 'qinghai', disabled: false, data: {}},
            {title: '宁夏', key: 'ningxia', disabled: false, data: {}},
            {title: '新疆', key: 'xinjiang', disabled: false, data: {}},
            {title: '香港', key: 'hongkong', disabled: true, data: {}},
            {title: '澳门', key: 'macao', disabled: true, data: {}},
            {title: '台湾', key: 'taiwan', disabled: true, data: {}},
        ];
        this.state = {
            activeKey: this.getDefaultKey(panes),
            panes,
            loaded: false
        };
    }

    getDefaultKey(panes) {
        const province = /(.*?)[省市特自]/.exec(window["returnCitySN"].cname)[1];
        const m = panes.filter(x => {
            return x.title === province && !x.disabled;
        });
        if (m.length > 0)
            return m[0].key;
        return "beijing"
    }

    updateData(key) {
        axios.get("https://service-r8373tyc-1253891892.gz.apigw.tencentcs.com/api/v1/provinces/" + key).then(
            result => {
                const panes = this.state.panes;
                const panef = panes.filter(x => {
                    return x.key === key;
                });
                panes[panes.indexOf(panef[0])].data = result.data;
                this.setState({
                    panes: panes,
                    loaded: true,
                })
            },
            error => {
                console.error(error)
            }
        );
    }

    componentDidMount() {
        this.updateData(this.state.activeKey);
    }

    onChange = activeKey => {
        this.setState({activeKey, loaded: false});
        this.updateData(activeKey);
    };

    render() {
        return (
            <div className="App">
                <Tabs
                    onChange={this.onChange}
                    activeKey={this.state.activeKey}
                >
                    {this.state.panes.map(pane => (
                        <TabPane tab={pane.title} key={pane.key} disabled={pane.disabled}>
                            <Chart data={pane.data} loaded={this.state.loaded}/>
                        </TabPane>
                    ))}
                </Tabs>
            </div>
        )
    }
}

export default App;
