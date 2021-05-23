/* eslint-disable no-undef */
import './App.css';
import React, { Component } from 'react';
import { mapStyle } from './resource/map-style'
// import { Con } from './resource/const'
import {CityList} from './resource/city_list'
import { Select, DatePicker, Button, Layout,Menu ,Form} from 'antd'
import Charts from './charts'
// import { SearchOutlined } from '@ant-design/icons'
import InfoWindow from './InfoWindow'
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
      endTime:0,
      isShowMap: true,
      emotionData:[],
      relationData:{},
      cityList: []
    }
  }

  componentDidMount(){
    this.initMap();
  }

  initMap = () => {
    new google.maps.Map(document.getElementById('map_canvas'), {
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
    // let marker, i
    // let markers = []
    // let locations = []
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
      let emotion_component = event.feature.getProperty('emotion_component')
      let params = {}
      params.name = event.feature.getProperty('name')
      params.GP_num = event.feature.getProperty('GP_num')
      params.Education = event.feature.getProperty('Education')
      params.covid_attention = event.feature.getProperty('covid_attention')
      params.level_advanced = event.feature.getProperty('level_advanced')
      params.population = event.feature.getProperty('population')

      infowindow.setContent(ReactDOMServer.renderToString(<InfoWindow params={params}/>))
      //infowindow.setPosition(event.feature.getGeometry().getAt(0).getAt(0).getAt(0))
      infowindow.setPosition(event.latLng)
      //infowindow.setOptions({pixelOffset: new google.maps.Size(0,0)})
      infowindow.open(map)

      this.initArea(emotion_component)
      this.initCloudChart(key_words)
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

  initCloudChart = (key_words) => {
    let CloudData = [];
    key_words.forEach((item)=>{
      let obj = {};
      obj.name = item.text;
      obj.value = item.value;
      CloudData.push(obj)
    })

    var myChart = echarts.init(document.getElementById('cloudChart'));
        let option = {
            series: [{
                type: 'wordCloud',
        
                // The shape of the "cloud" to draw. Can be any polar equation represented as a
                // callback function, or a keyword present. Available presents are circle (default),
                // cardioid (apple or heart shape curve, the most known polar equation), diamond (
                // alias of square), triangle-forward, triangle, (alias of triangle-upright, pentagon, and star.
        
                shape: 'circle',
        
                // A silhouette image which the white area will be excluded from drawing texts.
                // The shape option will continue to apply as the shape of the cloud to grow.
        
                // maskImage: maskImage,
        
                // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
                // Default to be put in the center and has 75% x 80% size.
        
                left: 'center',
                top: 'center',
                width: '70%',
                height: '80%',
                right: null,
                bottom: null,
        
                // Text size range which the value in data will be mapped to.
                // Default to have minimum 12px and maximum 60px size.
        
                sizeRange: [12, 60],
        
                // Text rotation range and step in degree. Text will be rotated randomly in range [-90, 90] by rotationStep 45
        
                rotationRange: [-90, 90],
                rotationStep: 45,
        
                // size of the grid in pixels for marking the availability of the canvas
                // the larger the grid size, the bigger the gap between words.
        
                gridSize: 8,
        
                // set to true to allow word being draw partly outside of the canvas.
                // Allow word bigger than the size of the canvas to be drawn
                drawOutOfBound: false,
        
                // If perform layout animation.
                // NOTE disable it will lead to UI blocking when there is lots of words.
                layoutAnimation: true,
        
                // Global text style
                textStyle: {
                    fontFamily: 'sans-serif',
                    fontWeight: 'bold',
                    // Color can be a callback function or a color string
                    color: function () {
                        // Random color
                        return 'rgb(' + [
                            Math.round(Math.random() * 160),
                            Math.round(Math.random() * 160),
                            Math.round(Math.random() * 160)
                        ].join(',') + ')';
                    }
                },
                emphasis: {
                    focus: 'self',
        
                    textStyle: {
                        shadowBlur: 10,
                        shadowColor: '#333'
                    }
                },
        
                // Data is an array. Each array item must have name and value property.
                data: CloudData
            }]
        }
        myChart.setOption(option)
  }

  initArea = (emotions) => {
    var chartDom = document.getElementById('infoChart');
    var myChart = echarts.init(chartDom);
    var option;
    let chatData = [];
    Object.keys(emotions).forEach((key)=>{
      let obj = {};
      obj.name = key;
      obj.value = emotions[key];
      chatData.push(obj)
    })

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

  getFactor = (value) =>{
    console.log(value)
    this.setState({
      searchFactor: value
    })
  }

  getDateTime = (type) => (date, dateString) =>{
    let time = new Date(dateString)
    if(type === 'startTime'){
      this.setState({
        startTime: time.getTime()
      })
    }else if(type==='endTime'){
      this.setState({
        endTime: time.getTime()
      })
    }

  }
  getCity = (value) =>{
    this.setState({
      cityList: value
    })
  }

  search = () =>{
    // let url = "http://0.0.0.0:6100/api/statistics/zone/melbourn?begintime=1616194716000&&endtime=1620601116000"
    let url = `http://localhost:6100/api/statistics/zone/melbourn?begintime=${this.state.startTime}&&endtime=${this.state.endTime}`;
    this.mapBuild(url)
  }
  show = () => {
    if(this.state.isShowMap){
      // this.getEmotionData()
      // this.getRelationData();
      this.setState({
        isShowMap : false
      })
    }else {
      this.setState({
        isShowMap : true
      })
    }

  }
  render(){
    const {Option} = Select;
    return(
      <div>
        <Layout>
          <Layout.Sider style={{backgroundColor:'#f0f2f5'}} width='275'>
            <Menu  mode="inline" defaultOpenKeys={['sub1']} style={{backgroundColor:'#f0f2f5'}}>
            {/* <Menu.SubMenu key="sub1" title="Navigation One" > */}
              <Form
                labelCol={{ span: 4 }}
                wrapperCol={{ span: 14 }}
                layout="horizontal"
              >
                <Form.Item label="factor">
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
                </Form.Item>
                <Form.Item label="city">
                <Select
                  style={{ width: 200 ,maxHeight:100}}
                  placeholder="Select a city"
                  optionFilterProp="children"
                  mode="multiple"
                  onChange={this.getCity}
                  filterOption={(input, option) =>
                    option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
                  }
                >
                  {Object.keys(CityList).map((key)=>{
                    return <Option value={key}>{CityList[key]}</Option>
                  })}
                  <Option value="covid_attention">Covid Attention</Option>
                  <Option value="GP_num">GP Number</Option>
                  <Option value="level_advanced">Level Advanced</Option>
                  <Option value="Education">Education</Option>
                </Select>
                </Form.Item>
                <Form.Item label="beginDate">
                  <DatePicker size={'default'} picker="month" onChange={this.getDateTime('startTime')}/>
                </Form.Item>
                <Form.Item label="endDate">
                  <DatePicker size={'default'} picker="month" onChange={this.getDateTime('endTime')}/>
                </Form.Item>
                <Form.Item>
                  <Button onClick={this.search}>Search</Button>
                </Form.Item>
                <Form.Item>
                <Button onClick={this.show}>{this.state.isShowMap ? 'Show' : 'Back'}</Button>
                </Form.Item>
              </Form>
            {/* </Menu.SubMenu> */}
            </Menu>
          </ Layout.Sider>
          <Layout.Content>
          <div id="gmap">
            {/* <loading :active.sync="visible" :can-cancel="true"></loading> */}
            <div id="map_canvas" style={this.state.isShowMap ? { height:"100vh", width:'100%'}: { height:"0vh", width:'100%'}} ></div>  
          </div>
          {!this.state.isShowMap && <Charts 
                                      emotionData={this.state.emotionData}
                                      relationData={this.state.relationData} 
                                      cityList = {this.state.cityList}
                                      startTime = {this.state.startTime}
                                      endTime = {this.state.endTime}
                                      />}
          </Layout.Content>

          </Layout>
      </div>
    )
  }
}
