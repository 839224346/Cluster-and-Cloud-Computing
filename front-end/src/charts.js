/* eslint-disable no-useless-constructor */
import React, {Component} from 'react'
import {Row, Col, Card } from 'antd'
import * as echarts from 'echarts'
import request from "./util/request"
export default class Charts extends Component{

    constructor(props){
        super(props)
        this.state = {
            emotionData:[],
            relationData:{}
        }
    }

    componentDidMount(){

        this.getRelationData()
        this.getEmotionData()

    }

    initRelationCharts = () => {
        this.initEchats("gp_chart")
        this.initEchats("education_chart")
        this.initEchats("population_chart")
        this.initEchats("income_chart")
        this.initEchats("age_chart")
        this.initEchats("homeless_chart")
    }

    getRelationData = (url) => {

        //api/statistics/relationship
        const params = {"begintime":"1616194716000","endtime":"1620601116000","lga_id":[20660,22170,22670]}
        request.post("/api/statistics/relationship", params)
        .then((response)=>{
          console.log('response.data', response.data)
          this.setState({
            relationData: response.data.data
          })
          this.initRelationCharts()
        })
      }
    
    getEmotionData = () => {
    const params = {"begintime":"1616194716000","endtime":"1620601116000","lga_id":[20660,22170,22670]}
    request.post("/api/statistics/lgaEmotion",params)
    .then((response)=>{
        console.log(response.data.data)
        this.setState({
        emotionData: response.data.data
        })
        this.initEmotionEchats()
    })
    }

    initEchats = (type) =>{
        
        const cityList = this.state.relationData.lga_name
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
                data: ['Emotion Score','Tweet Number', type]
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
                    data: cityList
                }
            ],
            yAxis: [
                {
                    type: 'value'
                }
            ],
            series: [
                {
                    name: 'Emotion Score',
                    type: 'bar',
                    emphasis: {
                        focus: 'series'
                    },
                    data: [320, 332, 301]
                },
                {
                    name: 'Tweet Number',
                    type: 'bar',
                    emphasis: {
                        focus: 'series'
                    },
                    data: [120, 132, 101]
                },
                {
                    name: type,
                    type: 'bar',
                    emphasis: {
                        focus: 'series'
                    },
                    data: [220, 182, 191]
                }
            ]
        };
        // 绘制图表
        myChart.setOption(option);
      }

    initEmotionEchats = () =>{
        var chartDom = document.getElementById('area_chart');
        var myChart = echarts.init(chartDom);
        var option;

        var data = [{"name": "melb", "children": [{"name": "Banyule", "value": 10, "children": [{"name": "positive", "value": 3,
        "children": [{"name": "subjective", "value":2}, {"name": "objective", "value": 5}]}, {"name": "neutral", "value": 20,
        "children": [{"name": "subjective", "value": 5}, {"name": "objective", "value": 6}]}, {"name": "negative", "value": 0,
        "children": [{"name": "subjective", "value": 0}, {"name": "objective", "value": 0}]}]}, {"name": "Frankston", "value":
        20, "children": [{"name": "positive", "value": 0, "children": [{"name": "subjective", "value": 0}, {"name": "objective",
        "value": 0}]}, {"name": "neutral", "value": 0, "children": [{"name": "subjective", "value": 0}, {"name": "objective",
        "value": 0}]}, {"name": "negative", "value": 0, "children": [{"name": "subjective", "value": 0}, {"name": "objective",
        "value": 0}]}]}, {"name": "Greater Dandenong", "value": 0, "children": [{"name": "positive", "value": 0, "children":
        [{"name": "subjective", "value": 0}, {"name": "objective", "value": 0}]}, {"name": "neutral", "value": 0, "children":
        [{"name": "subjective", "value": 0}, {"name": "objective", "value": 0}]}, {"name": "negative", "value": 0, "children":
        [{"name": "subjective", "value": 0}, {"name": "objective", "value": 0}]}]}]}]

        // var data = this.state.emotionData;

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
                <Card size="small" title="GP Number" >
                    <div id="gp_chart" style={{width:'550px',height:'350px'}}></div>
                </Card>
            </Col>
            <Col span={12}>
                <Card size="small" title="Education" >
                    <div id="education_chart" style={{width:'550px',height:'350px'}}></div>
                </Card>
            </Col>
          </Row>
          <Row>
            <Col span={12}>
            <Card size="small" title="Population" >
                <div id="population_chart" style={{width:'550px',height:'350px'}}></div>
             </Card>
            </Col>
            <Col span={12}>
            <Card size="small" title="Income" >
                <div id="income_chart" style={{width:'550px',height:'350px'}}></div>
              </Card>
            </Col>
          </Row>
          <Row>
            <Col span={12}>
            <Card size="small" title="Age" >
                <div id="age_chart" style={{width:'550px',height:'350px'}}></div>
             </Card>
            </Col>
            <Col span={12}>
            <Card size="small" title="Homeless Rate" >
                <div id="homeless_chart" style={{width:'550px',height:'350px'}}></div>
             </Card>
            </Col>
          </Row>
          <Row>
            <Col span={12}>
            <Card size="small" title="Emotion Component" >
                <div id="area_chart" style={{width:'550px',height:'350px'}}></div>
              </Card>
            </Col>
          </Row>
          </div>
        )
    }

}