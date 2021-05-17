import React from 'react';
import * as echarts from 'echarts';


function InfoWindow(props){
    const content = (
        <div style={{maxHeight:'1000px', weight:'250px', minWidth:'250px', textAlign:'center'}}>
            <h4>{props.name}</h4>
            <div>covid_attention</div>
            <div>averg_income</div>
            <div>GP_num</div>
            <div>level_advanced</div>
            <div>Education_rank</div>
            <div id="main" style={{height:'300px',width:'300px'}}></div>
        </div>
    )
    
    return content
}

export default InfoWindow