/* eslint-disable no-undef */
import './App.css';
import React, { Component } from 'react';
import { mapStyle } from './resource/map-style'
import { Con } from './resource/const'
import { Select, DatePicker, Button } from 'antd'
import { SearchOutlined } from '@ant-design/icons'
import InfoWindow from './InfoWindow'
import request from "./util/request"
// import axios from 'react-axios'
import * as echarts from 'echarts'
import 'antd/dist/antd.css'
import ReactDOMServer from 'react-dom/server';


const InfoContent = (
  <div>
    dsadsadasdsadas
  </div>
)

// const axios = require('axios');
export default class Map extends Component{

  barData = []
  barDataLabel= []
  constructor(props) {
    super(props)
    this.state = {
      searchContent: "",
      searchFactor:'',
      startTime:0,
      endTime:0
    }
  }

  componentDidMount(){
    this.initMap();
    // this.getRelationData();
    this.initEchats();
  }

  initEchats = (relationData) =>{
    // const lga_name = relationData.lga_name;
    // const {score, GP_num, education_rank, population_num,averg_income, averg_age, homeless_rate} = relationData.factor;
    var myChart = echarts.init(document.getElementById('forms'));
    let option;
    option = {
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

  initMap = () => {
    let map = new google.maps.Map(document.getElementById('map_canvas'), {
      zoom: 13,
      center:  {lat: -37.7998, lng: 144.9460},
      disableDefaultUI: true,
      styles: mapStyle
    })
  }

  rgbToHex =(r, g, b)=> {
    var hex = ((r<<16) | (g<<8) | b).toString(16);
    return "#" + new Array(Math.abs(hex.length-7)).join("0") + hex;
  }

  hexToRgb =(hex) =>{
    var rgb = [];
    for(var i=1; i<7; i+=2){
      rgb.push(parseInt("0x" + hex.slice(i,i+2)));
    }
    return rgb;
  }

  gradient =(startColor,endColor,step)=> {
    var sColor = this.hexToRgb(startColor),
        eColor = this.hexToRgb(endColor);

    var rStep = (eColor[0] - sColor[0]) / step,
        gStep = (eColor[1] - sColor[1]) / step,
        bStep = (eColor[2] - sColor[2]) / step;

    var gradientColorArr = [];
    for(var i=0;i<step;i++){
        gradientColorArr.push(this.rgbToHex(parseInt(rStep*i+sColor[0]),parseInt(gStep*i+sColor[1]),parseInt(bStep*i+sColor[2])));
    }
    return gradientColorArr;
  }

  mapBuild = (url) =>{
    let map = new google.maps.Map(document.getElementById('map_canvas'), {
      zoom: 9,
      center:  {lat: -37.7998, lng: 144.9460},
      disableDefaultUI: true,
      styles: mapStyle
    })

    let infowindow = new google.maps.InfoWindow({
      content : ''
    })
    let marker, i
    let markers = []
    let locations = []
    let colors = this.gradient('#ffffff','#ff9900',7)
   

    this.barDataLabel.length=0
    this.barData.length=0

    // set style for each region

    map.data.loadGeoJson(url)

    map.data.setStyle((feature) => {

      console.log('feature',feature)
      let total = feature.getProperty(this.state.searchFactor)
      let name = feature.getProperty('name')

      if (!this.barDataLabel.includes(name)){
        this.barDataLabel.push(name)
        this.barData.push(total)
      }
      let color = '#000000'
      if (total > 1)
        color = colors[0]
      if (total > 100)
        color = colors[1]
      if (total > 300)
        color = colors[2]
      if (total > 500)
        color = colors[3]
      if (total > 1000)
        color = colors[4]
      if (total > 1500)
        color = colors[5]
      if (total > 2000)
        color = colors[6]  

      return {
        fillColor: color,
        fillOpacity: 0.7,
        strokeWeight: 1
      }
    })
    // setup bar data
    this.barDatacollection = {
      labels: this.barDataLabel,
      datasets: [
        {
          label: 'Total Sins',
          backgroundColor: '#ff9900',
          data: this.barData
        }
      ]
    }

    // mouse click event: show grid info
    map.data.addListener('click', (event) => {
      console.log('sd',event)
      // prepare data
      let name = event.feature.getProperty("name")
      // let statistics = event.feature.getProperty("statistcs")

      // let infoPieDataSentiment = [] 
      // let infoPieNameSentiment = []
      // let infoPieData = []
      // let infoPieName = []
      // let temp = 'sentiment'

      // for (const [key, value] of Object.entries(statistics.sentiment)) {
      //   infoPieNameSentiment.push(key)
      //   infoPieDataSentiment.push(value)
      // }

      // for (const [key, value] of Object.entries(statistics)) {
      //   if (key != temp){
      //     for(const [inner_key, inner_value] of Object.entries(value)) {
      //       infoPieName.push(inner_key)
      //       infoPieData.push(inner_value)
      //     }
      //   }
      // }

      // // set all chart data here
      // let pieDatacollection_sentiment = {
      //   labels: infoPieNameSentiment,
      //   datasets: [
      //     {
      //       label: 'Sentiment',
      //       backgroundColor: this.gradient('#F5F5F5','ff9900',infoPieDataSentiment.length) ,
      //       data: infoPieDataSentiment
      //     }
      //   ]
      // }

      // let pieDatacollection = {
      //   labels: infoPieName,
      //   datasets: [
      //     {
      //       label: 'Sin',
      //       backgroundColor: this.gradient('#F5F5F5','ff9900',infoPieData.length) ,
      //       data: infoPieData
      //     }
      //   ]
      // }

      infowindow.setContent(ReactDOMServer.renderToString(<InfoWindow name={name}/>))
      //infowindow.setPosition(event.feature.getGeometry().getAt(0).getAt(0).getAt(0))
      infowindow.setPosition(event.latLng)
      //infowindow.setOptions({pixelOffset: new google.maps.Size(0,0)})
      infowindow.open(map)
      this.initArea()
    })
    
    // mouse over event: highlight color
    map.data.addListener('mouseover', (event) => {
      map.data.overrideStyle(event.feature, {fillColor: 'black'})
    })

    // mouse our event: reset color/info-window
    map.data.addListener('mouseout', (event) => {
      map.data.revertStyle()
      infowindow.close()
    })
  }

  initArea = () => {
    var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;

option = {
    tooltip: {
        trigger: 'item'
    },
    legend: {
        top: '5%',
        left: 'center'
    },
    series: [
        {
            name: '访问来源',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '40',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: [
                {value: 1048, name: '搜索引擎'},
                {value: 735, name: '直接访问'},
                {value: 580, name: '邮件营销'},
                {value: 484, name: '联盟广告'},
                {value: 300, name: '视频广告'}
            ]
        }
    ]
};

option && myChart.setOption(option);
  }

  getRelationData = (url) => {

    //api/statistics/relationship
    const params = {"begintime":"1616194716000","endtime":"1620601116000","lga_id":[20660,22170,22670]}
    request.post("/api/statistics/relationship", params)
    .then((response)=>{
      console.log(response.data)
    })
  }

  getFactor = (value) =>{
    console.log(value)
    this.setState({
      searchFactor: value
    })
  }

  getDateTime = (date, dateString) =>{
    let startTime = new Date(dateString[0])
    let endTime = new Date(dateString[1])
    this.setState({
      startTime: startTime.getTime(),
      endTime: endTime.getTime()
    })
  }

  search = () =>{
    let url = "http://0.0.0.0:6100/api/statistics/zone/melbourn?begintime=1616194716000&&endtime=1620601116000"
    // let url = `api/statistics/zone/melbourn/begintime=${this.state.startTime}/endtime=${this.state.endTime}`;
    this.getRelationData(url)
    this.mapBuild(url)
  }

  render(){
    const {Option} = Select;
    return(
      <div>
          <div id="gmap">
            {/* <loading :active.sync="visible" :can-cancel="true"></loading> */}
            <div id="map_canvas" style={{height:"90vh", width:'100%'}} ></div>  
            <div id="searchBar"> 
            <Select
              style={{ width: 200 }}
              placeholder="Select a factor"
              optionFilterProp="children"
              onChange={this.getFactor}
              filterOption={(input, option) =>
                option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
              }
            >
              <Option value="covid_attention">Covid_Attention</Option>
              <Option value="GP_num">GP_num</Option>
              <Option value="level_advanced">level_advanced</Option>
              <Option value="Education">Education</Option>
            </Select>
            <DatePicker.RangePicker style={{marginLeft:'10px'}} onChange={this.getDateTime}/>
            <Button type="primary" style={{marginLeft:'10px'}} icon={<SearchOutlined />} onClick={this.search}> Search</Button>
            </div>
          </div>
          <div style={{height:'500px',width:'100%'}}>
            <div id="forms" style={{width:'650px',height:'350px'}}></div>
          </div>

      </div>
    )
  }
}