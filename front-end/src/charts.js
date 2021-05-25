/* eslint-disable no-useless-constructor */
import React, {Component} from 'react'
import {Row, Col, Card } from 'antd'
import * as echarts from 'echarts'
import request from "./util/request"
import 'echarts-wordcloud';
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
        // this.initCloudChart()

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
        let {cityList, startTime, endTime} = this.props
        //api/statistics/relationship
        const params = {"begintime":startTime + '',"endtime":endTime+'',"lga_id":cityList}
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
    let {cityList, startTime, endTime} = this.props
    const params = {"begintime":startTime + '',"endtime":endTime+'',"lga_id":cityList}
    request.post("/api/statistics/lgaEmotion",params)
    .then((response)=>{
        console.log(response.data.data)
        this.setState({
        emotionData: response.data.data
        })
        this.initEmotionEchats()
    })
    }

    // initCloudChart = (type) =>{
    //     var myChart = echarts.init(document.getElementById('emotion_component'));
    //     let option = {
    //         series: [{
    //             type: 'wordCloud',
        
    //             // The shape of the "cloud" to draw. Can be any polar equation represented as a
    //             // callback function, or a keyword present. Available presents are circle (default),
    //             // cardioid (apple or heart shape curve, the most known polar equation), diamond (
    //             // alias of square), triangle-forward, triangle, (alias of triangle-upright, pentagon, and star.
        
    //             shape: 'circle',
        
    //             // A silhouette image which the white area will be excluded from drawing texts.
    //             // The shape option will continue to apply as the shape of the cloud to grow.
        
    //             // maskImage: maskImage,
        
    //             // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
    //             // Default to be put in the center and has 75% x 80% size.
        
    //             left: 'center',
    //             top: 'center',
    //             width: '70%',
    //             height: '80%',
    //             right: null,
    //             bottom: null,
        
    //             // Text size range which the value in data will be mapped to.
    //             // Default to have minimum 12px and maximum 60px size.
        
    //             sizeRange: [12, 60],
        
    //             // Text rotation range and step in degree. Text will be rotated randomly in range [-90, 90] by rotationStep 45
        
    //             rotationRange: [-90, 90],
    //             rotationStep: 45,
        
    //             // size of the grid in pixels for marking the availability of the canvas
    //             // the larger the grid size, the bigger the gap between words.
        
    //             gridSize: 8,
        
    //             // set to true to allow word being draw partly outside of the canvas.
    //             // Allow word bigger than the size of the canvas to be drawn
    //             drawOutOfBound: false,
        
    //             // If perform layout animation.
    //             // NOTE disable it will lead to UI blocking when there is lots of words.
    //             layoutAnimation: true,
        
    //             // Global text style
    //             textStyle: {
    //                 fontFamily: 'sans-serif',
    //                 fontWeight: 'bold',
    //                 // Color can be a callback function or a color string
    //                 color: function () {
    //                     // Random color
    //                     return 'rgb(' + [
    //                         Math.round(Math.random() * 160),
    //                         Math.round(Math.random() * 160),
    //                         Math.round(Math.random() * 160)
    //                     ].join(',') + ')';
    //                 }
    //             },
    //             emphasis: {
    //                 focus: 'self',
        
    //                 textStyle: {
    //                     shadowBlur: 10,
    //                     shadowColor: '#333'
    //                 }
    //             },
        
    //             // Data is an array. Each array item must have name and value property.
    //             data: [{
    //                 name: 'Farrah Abraham',
    //                 value: 366,
    //             },                {
    //                 name: 'Express',
    //                 value: 1112
    //             },
    //             {
    //                 name: 'Home',
    //                 value: 965
    //             },
    //             {
    //                 name: 'Johnny Depp',
    //                 value: 847
    //             },
    //             {
    //                 name: 'Lena Dunham',
    //                 value: 582
    //             },
    //             {
    //                 name: 'Lewis Hamilton',
    //                 value: 555
    //             },
    //             {
    //                 name: 'KXAN',
    //                 value: 550
    //             },]
    //         }]
    //     }
    //     myChart.setOption(option)
    // }


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
                    data: this.state.relationData.emotion_score
                },
                {
                    name: 'Tweet Number',
                    type: 'bar',
                    emphasis: {
                        focus: 'series'
                    },
                    data: this.state.relationData.tweet_num
                },
                {
                    name: type,
                    type: 'bar',
                    emphasis: {
                        focus: 'series'
                    },
                    data: this.state.relationData.type
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

        // var data = [{"name": "melb", "children": [{"name": "Banyule", "value": 10, "children": [{"name": "positive", "value": 3,
        // "children": [{"name": "subjective", "value":2}, {"name": "objective", "value": 5}]}, {"name": "neutral", "value": 20,
        // "children": [{"name": "subjective", "value": 5}, {"name": "objective", "value": 6}]}, {"name": "negative", "value": 0,
        // "children": [{"name": "subjective", "value": 0}, {"name": "objective", "value": 0}]}]}, {"name": "Frankston", "value":
        // 20, "children": [{"name": "positive", "value": 0, "children": [{"name": "subjective", "value": 0}, {"name": "objective",
        // "value": 0}]}, {"name": "neutral", "value": 0, "children": [{"name": "subjective", "value": 0}, {"name": "objective",
        // "value": 0}]}, {"name": "negative", "value": 0, "children": [{"name": "subjective", "value": 0}, {"name": "objective",
        // "value": 0}]}]}, {"name": "Greater Dandenong", "value": 0, "children": [{"name": "positive", "value": 0, "children":
        // [{"name": "subjective", "value": 0}, {"name": "objective", "value": 0}]}, {"name": "neutral", "value": 0, "children":
        // [{"name": "subjective", "value": 0}, {"name": "objective", "value": 0}]}, {"name": "negative", "value": 0, "children":
        // [{"name": "subjective", "value": 0}, {"name": "objective", "value": 0}]}]}]}]

        var data = this.state.emotionData;

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
            <Col span={12}>
            <Card size="small" title=" " >
                <div id="emotion_component" style={{width:'550px',height:'350px'}}></div>
              </Card>
            </Col>
          </Row>
          </div>
        )
    }

}