import React, {Component} from 'react';
import ReactEcharts from 'echarts-for-react'
import axios from 'axios';
import './App.css';
import {Tabs} from 'antd';

const {TabPane} = Tabs;

require('echarts/map/js/province/beijing.js');
require('echarts/map/js/province/tianjin.js');
require('echarts/map/js/province/hebei.js');
require('echarts/map/js/province/shanxi.js');
require('echarts/map/js/province/neimenggu.js');
require('echarts/map/js/province/liaoning.js');
require('echarts/map/js/province/fujian.js');
require('echarts/map/js/province/guangdong.js');

class Chart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            option:this.getInitialOption(),
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
        if (this.props.loaded) {
            const option = this.state.option;
            option.title.text = this.props.data.province + '新冠肺炎 2019-nCoV 爆发最新疫情情况';
            option.title.subtext = '累计确诊病例:' + this.props.data.confirmed + ' 累计死亡病例:' + this.props.data.dead + ' 累计治愈病例:' + this.props.data.healed;
            option.series[0].mapType = this.props.data.province;
            option.series[0].data = this.props.data.cities.map(x => {
                return {'name': x.city, 'value': x.confirmed}
            });
            return (
                <ReactEcharts
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
            { title: '北京', key: 'beijing', disabled: false, data: {} },
            { title: '天津', key: 'tianjin', disabled: false, data: {} },
            { title: '河北', key: 'hebei' , disabled: false, data: {} },
            { title: '山西', key: 'shanxi', disabled: true, data: {} },
            { title: '内蒙古', key: 'neimenggu' , disabled: false, data: {} },
            { title: '辽宁', key: 'liaoning' , disabled: false, data: {} },
            { title: '吉林', key: 'jilin' , disabled: true, data: {} },
            { title: '黑龙江', key: 'heilongjiang' , disabled: true, data: {} },
            { title: '上海', key: 'shanghai' , disabled: true, data: {} },
            { title: '江苏', key: 'jiangsu' , disabled: true, data: {} },
            { title: '浙江', key: 'zhejiang' , disabled: true, data: {} },
            { title: '安徽', key: 'anhui' , disabled: true, data: {} },
            { title: '福建', key: 'fujian' , disabled: false, data: {} },
            { title: '江西', key: 'jiangxi' , disabled: true, data: {} },
            { title: '山东', key: 'shandong' , disabled: true, data: {} },
            { title: '河南', key: 'henan' , disabled: true, data: {} },
            { title: '湖北', key: 'hubei' , disabled: true, data: {} },
            { title: '湖南', key: 'hunan' , disabled: true, data: {} },
            { title: '广东', key: 'guangdong' , disabled: false, data: {} },
            { title: '广西', key: 'guangxi' , disabled: true, data: {} },
            { title: '海南', key: 'hainan' , disabled: true, data: {} },
            { title: '重庆', key: 'chongqing' , disabled: true, data: {} },
            { title: '四川', key: 'sichuan' , disabled: true, data: {} },
            { title: '贵州', key: 'guizhou' , disabled: true, data: {} },
            { title: '云南', key: 'yunnan' , disabled: true, data: {} },
            { title: '西藏', key: 'xizang' , disabled: true, data: {} },
            { title: '陕西', key: 'shaanxi' , disabled: true, data: {} },
            { title: '甘肃', key: 'gansu' , disabled: true, data: {} },
            { title: '青海', key: 'qinghai' , disabled: true, data: {} },
            { title: '宁夏', key: 'ningxia' , disabled: true, data: {} },
            { title: '新疆', key: 'xinjiang' , disabled: true, data: {} },
            { title: '香港', key: 'hongkong' , disabled: true, data: {} },
            { title: '澳门', key: 'macao' , disabled: true, data: {} },
            { title: '台湾', key: 'taiwan' , disabled: true, data: {} },
        ];
        this.state = {
            activeKey: this.getDefaultKey(panes),
            panes,
            loaded: false
        };
    }

    getDefaultKey(panes) {
        const province = /(.*?)[省市特自]/.exec(window["returnCitySN"].cname)[1];
        const m = panes.filter(x=>{
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
                const panef = panes.filter(x=>{
                    return x.key === key;
                });
                panes[panes.indexOf(panef[0])].data = result.data;
                this.setState({
                    panes:panes,
                    loaded:true,
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
        this.setState({ activeKey, loaded:false });
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
                        <TabPane tab={pane.title} key={pane.key} disabled={pane.disabled} >
                            <Chart data={pane.data} loaded={this.state.loaded}/>
                        </TabPane>
                    ))}
                </Tabs>
            </div>
        )
    }
}

export default App;
