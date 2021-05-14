/* eslint-disable no-undef */
import './App.css';
import React, { Component } from 'react';
import { mapStyle } from './resource/map-style'
import { Con } from './resource/const'
import { Select } from 'antd'
import InfoWindow from './InfoWindow'

import * as echarts from 'echarts'


export default class Map extends Component{

  constructor(props) {
    super(props)
    this.state = {
      searchContent: "",
    }
  }

  componentDidMount(){
    this.initMap();
    this.initEchats();
  }

  initEchats = () =>{
    var myChart = echarts.init(document.getElementById('forms'));
    // 绘制图表
    myChart.setOption({   
        title: {
            text: 'DEMO'
        },
        tooltip: {},
        legend: {
            data:['销量1','销量2']
        },
        xAxis: {
            data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
        },
        yAxis: {},
        series: [
            {
            name: '销量1',
            type: 'bar',
            data: [5, 20, 36, 10, 10, 20]
            },
            {
                name: '销量2',
                type: 'line',
                data: [15, 30, 46, 46, 46, 30]
            }
        ]
    });
  }

  initMap = () => {
    let map = new google.maps.Map(document.getElementById('map_canvas'), {
      zoom: 13,
      center:  {lat: -37.7998, lng: 144.9460},
      disableDefaultUI: true,
      styles: mapStyle
    })
    
    let infowindow = new google.maps.InfoWindow()

    // ========================Icon examples=========================
    let icon = {
      path: Con.svg_lust,
      fillColor: '#ff9900',
      fillOpacity: 1,
      anchor: new google.maps.Point(250,250),
      strokeWeight: 0, 
      scale: .1
    }
          
    let icon2 = {
      path: Con.svg_gluttony,
      fillColor: '#ff9900',
      fillOpacity: 1,
      anchor: new google.maps.Point(250,250),
      strokeWeight: 0, 
      scale: .1
    }

    let icon3 = {
      path: Con.svg_neutral,
      fillColor: '#ff9900',
      fillOpacity: 1,
      anchor: new google.maps.Point(250,250),
      strokeWeight: 0, 
      scale: .1
    }
          
    let icon4 = {
      path: Con.svg_positive,
      fillColor: '#ff9900',
      fillOpacity: 1,
      anchor: new google.maps.Point(250,250),
      strokeWeight: 0, 
      scale: .1
    }

    let icon5 = {
      path: Con.svg_negative,
      fillColor: '#ff9900',
      fillOpacity: 1,
      anchor: new google.maps.Point(250,250),
      strokeWeight: 0, 
      scale: .1
    }

    let myFoodMark = {lat: -37.8036, lng: 144.9631}
    let myLustMark = {lat: -37.8136, lng: 144.9631}
    let myNormalMark = {lat: -37.8036, lng: 144.9531}
    let myPositiveMark = {lat: -37.8136, lng: 144.9731}
    let myNegativeMark = {lat: -37.8236, lng: 144.9631}

    let foodMark = new google.maps.Marker({
      position: myFoodMark,
      map: map,
      animation: google.maps.Animation.BOUNCE,
      title: 'Hello Food!',
      icon: icon2
    })

    let lustMark = new google.maps.Marker({
      position: myLustMark,
      map: map,
      animation: google.maps.Animation.BOUNCE,
      title: 'Hello Lust!',
      icon: icon
    })

    let warthMark = new google.maps.Marker({
      position: myNormalMark,
      map: map,
      animation: google.maps.Animation.BOUNCE,
      title: 'Hello Normal!',
      icon: icon3
    })

    let positiveMark = new google.maps.Marker({
      position: myPositiveMark,
      map: map,
      animation: google.maps.Animation.BOUNCE,
      title: 'Hello Positive!',
      icon: icon4
    })

    let negativeMark = new google.maps.Marker({
      position: myNegativeMark,
      map: map,
      animation: google.maps.Animation.BOUNCE,
      title: 'Hello Negative!',
      icon: icon5
    })

    positiveMark.addListener('click', function() {
      let content = '<div id="content" style="min-width:150px;">'+
                    '<p>Tags</p>'+
                    '<button class="btn btn-primary btn-dark">positive</button>'+
                    '<button class="btn btn-primary btn-warning">positive</button>'+
                    '<button class="btn btn-primary">positive</button>'+
                    '</div>';
      
      infowindow.setContent(content)
      infowindow.open(map, positiveMark)
    })
  }

  mapBuild = (type) =>{
    let map = new google.maps.Map(document.getElementById('map_canvas'), {
      zoom: 12,
      center:  {lat: -37.7998, lng: 144.9460},
      disableDefaultUI: true,
      styles: mapStyle
    })

    let infowindow = new google.maps.InfoWindow()
    let marker, i
    let markers = []
    let locations = []
    let colors = this.gradient('#ffffff','#ff9900',7)
   

    this.barDataLabel.length=0
    this.barData.length=0

    // set style for each region

    map.data.loadGeoJson(this.melb_geo)

    map.data.setStyle((feature) => {
      let total = feature.getProperty(type)
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
        fillColor: "#ff9900",
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
      let statistics = event.feature.getProperty("statistcs")

      let infoPieDataSentiment = [] 
      let infoPieNameSentiment = []
      let infoPieData = []
      let infoPieName = []
      let temp = 'sentiment'

      for (const [key, value] of Object.entries(statistics.sentiment)) {
        infoPieNameSentiment.push(key)
        infoPieDataSentiment.push(value)
      }

      for (const [key, value] of Object.entries(statistics)) {
        if (key != temp){
          for(const [inner_key, inner_value] of Object.entries(value)) {
            infoPieName.push(inner_key)
            infoPieData.push(inner_value)
          }
        }
      }

      // set all chart data here
      let pieDatacollection_sentiment = {
        labels: infoPieNameSentiment,
        datasets: [
          {
            label: 'Sentiment',
            backgroundColor: this.gradient('#F5F5F5','ff9900',infoPieDataSentiment.length) ,
            data: infoPieDataSentiment
          }
        ]
      }

      let pieDatacollection = {
        labels: infoPieName,
        datasets: [
          {
            label: 'Sin',
            backgroundColor: this.gradient('#F5F5F5','ff9900',infoPieData.length) ,
            data: infoPieData
          }
        ]
      }

      infowindow.setContent(<InfoWindow />)
      //infowindow.setPosition(event.feature.getGeometry().getAt(0).getAt(0).getAt(0))
      infowindow.setPosition(event.latLng)
      //infowindow.setOptions({pixelOffset: new google.maps.Size(0,0)})
      infowindow.open(map)
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

  render(){
    const {Option} = Select;
    return(
      <div>
          <div id="gmap">
            {/* <loading :active.sync="visible" :can-cancel="true"></loading> */}
            <div id="map_canvas" style={{height:"90vh", width:'100%'}} ></div>  
            <div id="searchBar"> 
              <h2>General Search</h2>
            </div>
          </div>
          <div style={{height:'500px',width:'100%'}}>
            <div id="forms" style={{width:'650px',height:'350px'}}></div>
          </div>
      </div>
    )
  }
}