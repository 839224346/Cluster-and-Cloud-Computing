import React from 'react';
import { Divider } from 'antd';


function InfoWindow(props){
    let {name,GP_num,Education,covid_attention,level_advanced,population} = props.params
    const content = (
        <div style={{maxHeight:'1000px', weight:'250px', minWidth:'250px', textAlign:'center'}}>
            <h1 style={{color:'#0e4381'}}>{name}</h1>
            <Divider style={{color:'#0e4381'}}>Basic Info</Divider>
            <div>Covid Attention: {covid_attention}</div>
            <div>Population: {population.total}</div>
            <div>GP Number: {GP_num}</div>
            <div>Level Advanced: {level_advanced}</div>
            <div>Education Rank: {Education}</div>
            <Divider style={{color:'#0e4381'}}>Emotion Component</Divider>
            <div id="infoChart" style={{height:'200px',width:'100%'}}></div>
        </div>
    )
    
    return content
}

export default InfoWindow