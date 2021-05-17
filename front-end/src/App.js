/* eslint-disable no-undef */
import './App.css';
import React, { Component } from 'react';
import { mapStyle } from './resource/map-style'
import { Con } from './resource/const'
import { Select, DatePicker, Button, Row, Col } from 'antd'
import Charts from './charts'
import { SearchOutlined } from '@ant-design/icons'
import InfoWindow from './InfoWindow'
import request from "./util/request"
// import axios from 'react-axios'
import * as echarts from 'echarts'
import 'antd/dist/antd.css'
import ReactDOMServer from 'react-dom/server';


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
    // this.initEchats();
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
      let key_words = event.feature.getProperty('key_words')
      let params = {}
      params.name = event.feature.getProperty('name')
      params.GP_num = event.feature.getProperty('GP_num')
      params.Education = event.feature.getProperty('Education')
      params.covid_attention = event.feature.getProperty('covid_attention')
      params.level_advanced = event.feature.getProperty('level_advanced')
      params.population = event.feature.getProperty('population')
      // prepare data
      console.log(params)


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

      infowindow.setContent(ReactDOMServer.renderToString(<InfoWindow params={params}/>))
      //infowindow.setPosition(event.feature.getGeometry().getAt(0).getAt(0).getAt(0))
      infowindow.setPosition(event.latLng)
      //infowindow.setOptions({pixelOffset: new google.maps.Size(0,0)})
      infowindow.open(map)

      this.initArea(key_words)
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

  initArea = (key_words) => {
    var chartDom = document.getElementById('infoChart');
    var myChart = echarts.init(chartDom);
    var option;
    let length = key_words.length;
    let chatData = [];
    key_words.forEach((item)=>{
      let obj = {};
      obj.name = item.text;
      obj.value = item.value;
      chatData.push(obj)
    })
    console.log(chatData)

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
                name: 'Major Emotions',
                type: 'pie',
                radius: ['20%', '50%'],
                avoidLabelOverlap: false,
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: false,
                        fontSize: '40',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: chatData
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
              <Option value="covid_attention">Covid Attention</Option>
              <Option value="GP_num">GP Number</Option>
              <Option value="level_advanced">Level Advanced</Option>
              <Option value="Education">Education</Option>
            </Select>
            <DatePicker.RangePicker style={{marginLeft:'10px'}} onChange={this.getDateTime}/>
            <Button type="primary" style={{marginLeft:'10px'}} onClick={this.search}> Search</Button>
            </div>
          </div>
          <Charts />
      </div>
    )
  }
}