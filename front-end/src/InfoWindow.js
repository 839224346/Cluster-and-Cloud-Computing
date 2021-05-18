import React from 'react';
import { Divider, Col, Row } from 'antd';


function InfoWindow(props){
    let {name,GP_num,Education,covid_attention,level_advanced,population} = props.params
    const content = (
        <div style={{maxHeight:'1000px', weight:'250px', minWidth:'500px', textAlign:'center'}}>
            <h1 style={{color:'#0e4381'}}>{name}</h1>
            <Row>
            <Col span={8}>
            <Divider style={{color:'#0e4381'}}>Basic Info</Divider>
            <div>Covid Attention: {covid_attention}</div>
            <div>Population: {population.total}</div>
            <div>GP Number: {GP_num}</div>
            <div>Level Advanced: {level_advanced}</div>
            <div>Education Rank: {Education}</div>
            </Col>
            <Col span={8}>
            <Divider style={{color:'#0e4381'}}>Emotion Component</Divider>
            <div id="infoChart" style={{height:'200px',width:'100%'}}></div>
            </Col>
            <Col span={8}>
            <Divider style={{color:'#0e4381'}}>Emotion Component</Divider>
            <div id="cloudChart" style={{height:'200px',width:'100%'}}></div>
            </Col>
            </Row>
        </div>
    )
    
    return content
}

export default InfoWindow