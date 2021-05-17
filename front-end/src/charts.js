/* eslint-disable no-useless-constructor */
import React, {Component} from 'react'
import {Row, Col } from 'antd'
import * as echarts from 'echarts'
export default class Charts extends Component{

    constructor(props){
        super(props)
    }

    componentDidMount(){
        this.initEchats('1',"gp_chart")
        this.initEchats('1',"education_chart")
        this.initEchats('1',"population_chart")
        this.initEchats('1',"income_chart")
        this.initEchats('1',"age_chart")
        this.initEchats('1',"homeless_chart")
        this.initAreaEchats()
    }

    initEchats = (relationData, type) =>{
        // const lga_name = relationData.lga_name;
        // const {score, GP_num, education_rank, population_num,averg_income, averg_age, homeless_rate} = relationData.factor;
        var myChart = echarts.init(document.getElementById(type));
        let option;
        option = {
            dackMode: true,
            tooltip: {
                trigger: 'axis',
                axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                    type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            legend: {
                data: ['Emotion', 'GP', 'Education', 'Population', 'Income', 'Age', "Homeless"]
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: [
                {
                    type: 'category',
                    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            series: [
                {
                    name: 'Emotion',
                    type: 'bar',
                    emphasis: {
                        focus: 'series'
                    },
                    data: [320, 332, 301, 334, 390, 330, 320]
                },
                {
                    name: 'GP',
                    type: 'bar',
                    // stack: '广告',
                    emphasis: {
                        focus: 'series'
                    },
                    data: [120, 132, 101, 134, 90, 230, 210]
                },
                {
                    name: 'Education',
                    type: 'bar',
                    // stack: '广告',
                    emphasis: {
                        focus: 'series'
                    },
                    data: [220, 182, 191, 234, 290, 330, 310]
                },
                {
                    name: 'Population',
                    type: 'bar',
                    // stack: '广告',
                    emphasis: {
                        focus: 'series'
                    },
                    data: [150, 232, 201, 154, 190, 330, 410]
                },
                {
                    name: 'Income',
                    type: 'bar',
                    data: [862, 1018, 964, 1026, 1679, 1600, 1570],
                    emphasis: {
                        focus: 'series'
                    },
                    // markLine: {
                    //     lineStyle: {
                    //         type: 'dashed'
                    //     },
                    //     data: [
                    //         [{type: 'min'}, {type: 'max'}]
                    //     ]
                    // }
                },
                {
                    name: 'Age',
                    type: 'bar',
                    barWidth: 5,
                    // stack: '搜索引擎',
                    emphasis: {
                        focus: 'series'
                    },
                    data: [620, 732, 701, 734, 1090, 1130, 1120]
                },
                {
                    name: 'Homeless',
                    type: 'bar',
                    // stack: '搜索引擎',
                    emphasis: {
                        focus: 'series'
                    },
                    data: [120, 132, 101, 134, 290, 230, 220]
                }
            ]
        };
        // 绘制图表
        myChart.setOption(option);
      }

    initAreaEchats = () =>{
        var chartDom = document.getElementById('area_chart');
        var myChart = echarts.init(chartDom);
        var option;

        var data = [{
            name: 'Grandpa',
            children: [{
                name: 'Uncle Leo',
                value: 15,
                children: [{
                    name: 'Cousin Jack',
                    value: 2
                }, {
                    name: 'Cousin Mary',
                    value: 5,
                    children: [{
                        name: 'Jackson',
                        value: 2
                    }]
                }, {
                    name: 'Cousin Ben',
                    value: 4
                }]
            }, {
                name: 'Aunt Jane',
                children: [{
                    name: 'Cousin Kate',
                    value: 4
                }]
            }, {
                name: 'Father',
                value: 10,
                children: [{
                    name: 'Me',
                    value: 5,
                    itemStyle: {
                        color: 'red'
                    }
                }, {
                    name: 'Brother Peter',
                    value: 1
                }]
            }]
        }, {
            name: 'Mike',
            children: [{
                name: 'Uncle Dan',
                children: [{
                    name: 'Cousin Lucy',
                    value: 3
                }, {
                    name: 'Cousin Luck',
                    value: 4,
                    children: [{
                        name: 'Nephew',
                        value: 2
                    }]
                }]
            }]
        }, {
            name: 'Nancy',
            children: [{
                name: 'Uncle Nike',
                children: [{
                    name: 'Cousin Betty',
                    value: 1
                }, {
                    name: 'Cousin Jenny',
                    value: 2
                }]
            }]
        }];

        option = {
            visualMap: {
                type: 'continuous',
                min: 0,
                max: 10,
                inRange: {
                    color: ['#2F93C8', '#AEC48F', '#FFDB5C', '#F98862']
                }
            },
            series: {
                type: 'sunburst',
                data: data,
                radius: [0, '90%'],
                label: {
                    rotate: 'radial'
                }
            }
        };

        option && myChart.setOption(option);
    }
    

    render(){
        return(
            <div>
            <Row>
            <Col span={12}>
              <div style={{maxHeight:'500px',width:'100%'}}>
                <div id="gp_chart" style={{width:'650px',height:'350px'}}></div>
              </div>
            </Col>
            <Col span={12}>
              <div style={{maxHeight:'500px',width:'100%'}}>
                <div id="education_chart" style={{width:'650px',height:'350px'}}></div>
              </div>
            </Col>
          </Row>
          <Row>
            <Col span={12}>
              <div style={{maxHeight:'500px',width:'100%'}}>
                <div id="population_chart" style={{width:'650px',height:'350px'}}></div>
              </div>
            </Col>
            <Col span={12}>
              <div style={{maxHeight:'500px',width:'100%'}}>
                <div id="income_chart" style={{width:'650px',height:'350px'}}></div>
              </div>
            </Col>
          </Row>
          <Row>
            <Col span={12}>
              <div style={{maxHeight:'500px',width:'100%'}}>
                <div id="age_chart" style={{width:'650px',height:'350px'}}></div>
              </div>
            </Col>
            <Col span={12}>
              <div style={{maxHeight:'500px',width:'100%'}}>
                <div id="homeless_chart" style={{width:'650px',height:'350px'}}></div>
              </div>
            </Col>
          </Row>
          <Row>
            <Col span={12}>
              <div style={{maxHeight:'500px',width:'100%'}}>
                <div id="area_chart" style={{width:'650px',height:'350px'}}></div>
              </div>
            </Col>
          </Row>
          </div>
        )
    }

}